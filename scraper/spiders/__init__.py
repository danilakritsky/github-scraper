# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy

class ScraperSpider(scrapy.Spider):
    """Spider to crawl github accounts and collect data on repos."""
    name = 'scraper'

    
    def start_requests(self):
        """Start requests on the given url."""
        start_urls = [
            'https://github.com/scrapy'
            ]
        for url in start_urls:
            yield scrapy.Request(url, callback=self.parse_account_page)


    def parse_account_page(self, response) -> None:
        """Parse the GitHUb account page to extract the link to repos."""
        repos_url = response.css('a.UnderlineNav-item::attr(href)').re('.*repositories.*')[0]
        self.logger.info(repos_url)
        yield response.follow(repos_url, callback=self.parse_repos_page)      


    def parse_repos_page(self, response):
        """Parse repos page to extract links to each repository."""
        repo_urls = response.css('[data-hovercard-type="repository"]::attr(href)').getall()
        self.logger.info(repo_urls)
        for url in repo_urls:
            yield response.follow(url, callback=self.parse_repo_info)

        next_page_url = response.css('a.next_page::attr(href)').get()
        self.logger.info(next_page_url)
        if next_page_url:
            yield response.follow(next_page_url, callback=self.parse_repos_page)


    def parse_repo_info(self, response):
        """Parse data for a specific repo page."""

        repo_name = response.css('a[data-pjax="#repo-content-pjax-container"]::attr(href)').getall()[0] # split by / and get the last item
        about = response.css('[class="f4 my-3"]::text').getall()  ## remove newlines and spaces
        website_link = response.css('a[role="link"]::attr(href)').get()
        stars = response.css('span[id="repo-stars-counter-star"]::attr(title)').get()
        forks = response.css('span[id="repo-network-counter"]::attr(title)').get()     
        watching = response.css('a[href$="watchers"]').css('strong::text').get()
        # !!! only the main branch commits are available from the repo page
        main_branch_info = dict()
        main_branch_info['commit_count'] = response.css('a[href*="commits"]').css('strong::text').get()
        main_branch_info['last_commit_author'] = response.css('a[class*="commit-author"]::text').get() # returns None from time to time
        main_branch_info['last_commit_time'] = response.css('relative-time::attr(datetime)').get()
        item = {
                'repo_name': repo_name,
                'about': about,
                'website_link': website_link,
                'stars': stars,
                'forks': forks,
                'watching': watching,
                'main_branch_info': main_branch_info
        }
        self.logger.info(item)

        releases_url = response.css('a::attr(href)').re('.*releases.*')[0]
        self.logger.info(releases_url)
        yield response.follow(
            releases_url,
            callback=self.parse_releases_page,
            meta=item)

    
    def parse_releases_page(self, response):
        """Parse releases page to extract data about the latest release."""
        item = response.meta
        self.logger.info(item)
        releases = response.css('a::attr(href)').re('.*releases/tag.*')
        
        if releases:
            self.logger.info(latest_release_tage:=releases[0])
            item['latest_release']['tag'] = latest_release
            yield response.follow(latest_release, callback=self.parse_latest_release_info, meta=item)

    
    def parse_latest_release_info(self, response):
        """Parse info about the latest release."""
        item = response.meta
        changelog = response.xpath('//div[@data-test-selector="body-content"]//text()').getall()
        item['latest_release']['changelog'] = changelog
        self.logger.info(changelog)





