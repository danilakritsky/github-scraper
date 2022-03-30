"""This module contains the spider for crawling and parsing repo data."""

import copy
import re

import scrapy
from scrapy.loader import ItemLoader

from scraper.items import RepoInfoItem


class ScraperMongoSpider(scrapy.Spider):
    """Spider to crawl github accounts and collect data on repos."""

    name = "scraper_mongo"
    allowed_domains = ["github.com"]

    custom_settings = {"ITEM_PIPELINES": {"scraper.pipelines.MongoDBPipeline": 100}}

    def start_requests(self):
        """Start making requests to the given URLs."""
        start_urls = []
        for url in self.start_urls.split(","):
            # ignore any domain other than github.com
            if re.search(
                r"^https?://github.com/[a-z0-9](?:[a-z\d]|-(?=[a-z\d])){0,38}/?$", url
            ):
                url = url.replace("http:", "https:")
                if url[-1] == "/":
                    url = url[:-1]
                start_urls.append(url)
            else:
                self.logger.warning(f"Ignoring {url} - not a valid GitHub subdomain!")

        if start_urls:
            for url in start_urls:
                loader = ItemLoader(item=RepoInfoItem())
                loader.add_value("account", url)
                yield scrapy.Request(
                    url, callback=self.parse_account_page, meta={"loader": loader}
                )
        # else:
        #     return

    def parse_account_page(self, response) -> None:
        """Parse a GitHUb account page to extract a link to account's repos."""
        loader = response.meta["loader"]
        repos_url = response.css("[href]::attr(href)").re(".*repositories.*")[0]
        yield response.follow(
            repos_url, callback=self.parse_repos_page, meta={"loader": loader}
        )

    def parse_repos_page(self, response):
        """Parse repos page to extract links to each repository."""
        loader = response.meta["loader"]
        repo_urls = response.css(
            '[itemprop="name codeRepository"]::attr(href)'
        ).getall()

        if not repo_urls:  # handle empty accounts
            yield loader.load_item()

        for url in repo_urls:
            yield response.follow(
                url, callback=self.parse_repo_info, meta={"loader": loader}
            )

        next_page_url = response.css("a.next_page::attr(href)").get()
        # set DOWNLOAD_DELAY = 0.5 in settings.py
        # to avoid making too many requests (429 response code)

        if next_page_url:  # handle empty accounts
            yield response.follow(
                next_page_url, callback=self.parse_repos_page, meta={"loader": loader}
            )

    def parse_repo_info(self, response):
        """Parse data for a specific repo page."""

        # copy to avoid passing the same item across different repo parsers
        loader = copy.deepcopy(response.meta["loader"])

        # assign current repsonse to the loader's selector attribute to use ccs and xpath
        loader.selector = response
        loader.add_css(
            "repo", 'a[data-pjax="#repo-content-pjax-container"]::attr(href)'
        )
        loader.add_css("about", '[class="f4 my-3"]::text')
        loader.add_css("website_link", 'a[role="link"]::attr(href)')
        loader.add_css("stars", 'span[id="repo-stars-counter-star"]::attr(title)')
        loader.add_css("forks", 'span[id="repo-network-counter"]::attr(title)')
        # NOTE the exact watcher count is impossible to parse when logged out
        loader.add_css("watching", 'a[href$="watchers"] > strong::text')
        loader.add_css("release_count", 'a[href$="/releases"] span::attr(title)')

        releases_url = response.css('a[href$="/releases"]::attr(href)').get()

        # NOTE only the main branch commits are available to parse from the repo page
        #  main_branch_loader = ItemLoader(item=MainBranchItem(), selector=response)
        main_branch_commits_url = response.css('a[href*="commits"]::attr(href)').get()
        if main_branch_commits_url:  # handle empty repos
            # use the desendant selector (' '), instead of the child selector ('>')
            loader.add_css(
                "main_branch_commit_count", 'a[href*="commits"] strong::text'
            )
            yield response.follow(
                main_branch_commits_url,
                callback=self.parse_commits_page,
                # pass as a dict to avoid attaching technical details about the response to meta
                meta={
                    "loader": loader,
                    "releases_url": releases_url,
                },
            )
        else:
            yield loader.load_item()

    def parse_commits_page(self, response):
        """Parse the main branch commits page for info on the latest commit."""
        loader = response.meta["loader"]

        # main_branch_loader = response.meta["main_branch_loader"]
        loader.selector = response
        loader.add_css(
            "main_branch_latest_commit_author", 'a[class*="commit-author"]::text'
        )
        loader.add_css(
            "main_branch_latest_commit_datetime", "relative-time::attr(datetime)"
        )

        latest_commit_url = response.css('a[href*="/commit/"]::attr(href)').get()

        yield response.follow(
            latest_commit_url,
            callback=self.parse_commit_message,
            meta={
                "loader": loader,
                "releases_url": response.meta["releases_url"],
            },
        )

    def parse_commit_message(self, response):
        """Parse commit page for message."""
        loader = response.meta["loader"]
        loader.selector = response

        loader.add_xpath(
            "main_branch_latest_commit_message",
            '//div[@class="commit-title markdown-title"]//text()',
        )

        yield response.follow(
            response.meta["releases_url"],
            callback=self.parse_releases_page,
            meta={"loader": loader},
        )

    def parse_releases_page(self, response):
        """Parse releases page to extract data about the latest release."""
        loader = response.meta["loader"]
        releases = response.css("a::attr(href)").re(".*releases/tag.*")
        if releases:
            yield response.follow(
                releases[0],
                callback=self.parse_latest_release_info,
                meta={"loader": loader},
            )
        else:
            yield loader.load_item()

    def parse_latest_release_info(self, response):
        """Parse info about the latest release."""
        loader = response.meta["loader"]
        loader.add_value(
            "latest_release_tag", response.css('span[class="ml-1"]::text').get().strip()
        )

        # support parsing changelogs written in both markdown and plain text
        loader.add_xpath(
            "latest_release_changelog",
            '//div[@data-cstest-selector="body-content"]//text()',
        )
        loader.add_css("latest_release_changelog", "[data-test-selector]::text")

        loader.add_css("latest_release_datetime", "[datetime]::attr(datetime)")

        yield loader.load_item()
