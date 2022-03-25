# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
from scrapy.loader import ItemLoader
from scraper.items import RepoInfoItem, MainBranchItem
import copy


class ScraperSpider(scrapy.Spider):
    """Spider to crawl github accounts and collect data on repos."""

    name = "scraper"
    # allowed_domains = 'github.com'

    def start_requests(self):
        """Start requests on the given url."""
        start_urls = ["https://github.com/ubuntu"]
        for url in start_urls:
            loader = ItemLoader(item=RepoInfoItem())
            loader.add_value("account", url)
            yield scrapy.Request(
                url, callback=self.parse_account_page, meta={"loader": loader}
            )

    def parse_account_page(self, response) -> None:
        """Parse the GitHUb account page to extract the link to repos."""
        loader = response.meta["loader"]
        repos_url = response.css("a.UnderlineNav-item::attr(href)").re(
            ".*repositories.*"
        )[0]
        yield response.follow(
            repos_url, callback=self.parse_repos_page, meta={"loader": loader}
        )

    def parse_repos_page(self, response):
        """Parse repos page to extract links to each repository."""
        loader = response.meta["loader"]
        repo_urls = response.css(
            '[data-hovercard-type="repository"]::attr(href)'
        ).getall()

        if not repo_urls:  # handle empty accounts
            yield loader.load_item()

        for url in repo_urls:
            yield response.follow(
                url, callback=self.parse_repo_info, meta={"loader": loader}
            )

        next_page_url = response.css("a.next_page::attr(href)").get()
        # set DOWNLOAD_DELAY = 0.5 in settings.py to avoid making too many requests (429 response code)

        if next_page_url:  # handle empty accounts
            yield response.follow(
                next_page_url, callback=self.parse_repos_page, meta={"loader": loader}
            )

    def parse_repo_info(self, response):
        """Parse data for a specific repo page."""

        # copy to avoid using the same item across repos
        loader = copy.deepcopy(response.meta["loader"])

        # assign current repsonse to the loader's selector attribute to use ccs and xpath
        loader.selector = response
        loader.add_css('repo_name', 'a[data-pjax="#repo-content-pjax-container"]::attr(href)')
        loader.add_css('about', '[class="f4 my-3"]::text')
        loader.add_css('website_link', 'a[role="link"]::attr(href)')
        loader.add_css('stars', 'span[id="repo-stars-counter-star"]::attr(title)')
        loader.add_css('forks', 'span[id="repo-network-counter"]::attr(title)')
        # can't parse the exact watcher count when logged out
        loader.add_css('watching', 'a[href$="watchers"] > strong::text')
        loader.add_css('release_count', 'a[href$="/releases"] span::attr(title)')
        
        releases_url = response.css('a[href$="/releases"]::attr(href)').get()

        # NOTE only the main branch commits are available from the repo page
        main_branch_loader = ItemLoader(item=MainBranchItem(), selector=response)
        main_branch_commits_url = response.css('a[href*="commits"]::attr(href)').get()
        if main_branch_commits_url:  # handle empty repos
            # use the desendant selector (' '), instead of the child selector ('>')
            main_branch_loader.add_css('commit_count', 'a[href*="commits"] strong::text')     
            yield response.follow(
                main_branch_commits_url,
                callback=self.parse_commits_page,
                meta={  # pass as a dict to avoid attaching technical details about the response to meta
                    "loader": loader,
                    "releases_url": releases_url,
                    "main_branch_loader": main_branch_loader
                },
            )
        else:
            yield (item := loader.load_item())

    def parse_commits_page(self, response):
        """Parse the main branch commits page for info on the latest commit."""
        loader = response.meta["loader"]

        main_branch_loader = response.meta["main_branch_loader"]
        main_branch_loader.selector = response
        main_branch_loader.add_css('latest_commit_author', 'a[class*="commit-author"]::text')
        main_branch_loader.add_css('latest_commit_datetime', "relative-time::attr(datetime)")
        
        latest_commit_url = response.css('a[href*="/commit/"]::attr(href)').get()

        yield response.follow(
            latest_commit_url,
            callback=self.parse_commit_message,
            meta={
                "loader": loader,
                "releases_url": response.meta["releases_url"],
                "main_branch_loader": main_branch_loader,
            }
        )

    def parse_commit_message(self, response):
        """Parse commit page for message."""
        loader = response.meta["loader"]
        loader.selector = response
        
        main_branch_loader = response.meta["main_branch_loader"]
        main_branch_loader.selector = response
        main_branch_loader.add_xpath('latest_commit_message', '//div[@class="commit-title markdown-title"]//text()')
        
        loader.add_value('main_branch', main_branch_loader.load_item())
        yield loader.load_item()

        # yield response.follow(
        #     response.meta["releases_url"],
        #     callback=self.parse_releases_page,
        #     meta={"item": item},
        # )

    # def parse_releases_page(self, response):
    #     """Parse releases page to extract data about the latest release."""
    #     item = response.meta["item"]
    #     releases = response.css("a::attr(href)").re(".*releases/tag.*")
    #     if releases:
    #         yield response.follow(
    #             releases[0],
    #             callback=self.parse_latest_release_info,
    #             meta={"item": item},
    #         )
    #     else:
    #         yield item

    # def parse_latest_release_info(self, response):
    #     """Parse info about the latest release."""
    #     item = response.meta["item"]

    #     tag = response.css('h1[class="d-inline mr-3"]::text').get()
    #     item["latest_release"]["tag"] = tag

    #     changelog = response.xpath(
    #         '//div[@data-test-selector="body-content"]//text()'
    #     ).getall()
    #     item["latest_release"]["changelog"] = changelog

    #     datetime = response.css("[datetime]::attr(datetime)").get()
    #     item["latest_release"]["datetime"] = datetime

    #     yield item
