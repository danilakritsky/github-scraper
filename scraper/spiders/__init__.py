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
            'https://github.com/ubuntu'
            ]
        for url in start_urls:
            yield scrapy.Request(url, callback=self.parse_account_page)


    def parse_account_page(self, response) -> None:
        """Parse the GitHUb account page to extract the link to repos."""
        repos_url = response.css('a.UnderlineNav-item::attr(href)').re('.*repositories.*')[0]
        yield response.follow(repos_url, callback=self.parse_repos_page)      


    def parse_repos_page(self, response):
        """Parse repos page to extract links to each repository."""
        repo_urls = response.css('[data-hovercard-type="repository"]::attr(href)').getall()
        for url in repo_urls:
            yield response.follow(url, callback=self.parse_repo_info)

        next_page_url = response.css('a.next_page::attr(href)').get()
        # set DOWNLOAD_DELAY = 0.5 in settings.py to avoid making too many requests (429 response code)
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
        main_branch_info = {}
        commit_count = response.css('a[href*="commits"]').css('strong::text').get()     
        if commit_count:  # handle empty repos
            main_branch_info['commit_count'] = commit_count
        main_branch_commits_url = response.css('a[href*="commits"]::attr(href)').get()       
        
        release_count = response.css('a[href$="/releases"]').css('span::attr(title)').get()
        releases_url = response.css('a[href$="/releases"]::attr(href)').get()
        item = {
                'repo_name': repo_name,
                'about': about,
                'website_link': website_link,
                'stars': stars,
                'forks': forks,
                'watching': watching,
                'main_branch_info': main_branch_info,
                'release_count': release_count,
                'latest_release': {}
        }
        if main_branch_commits_url:  # handle empty repos
            yield response.follow(
                main_branch_commits_url,
                callback=self.parse_commits_page,
                meta={  # pass as a dict to avoid attaching technical details about the response to meta
                    'item': item,
                    'releases_url': releases_url
                })  
        else:
            yield item


    def parse_commits_page(self, response):
        """Parse the main branch commits page for info on the latest commit."""
        item = response.meta['item']
        item['main_branch_info']['latest_commit_author'] = response.css('a[class*="commit-author"]::text').get() # returns None from time to time
        item['main_branch_info']['latest_commit_datetime'] = response.css('relative-time::attr(datetime)').get()
        
        latest_commit_url = response.css('a[href*="/commit/"]::attr(href)').get()

        yield response.follow(
            latest_commit_url,
                callback=self.parse_commit_message,
                meta={
                    'item': item,
                    'releases_url': response.meta['releases_url']
                })
        
    def parse_commit_message(self, response):
        """Parse commit page for message."""
        item = response.meta['item']
        item['main_branch_info']['latest_commit_message'] = response.xpath('//div[@class="commit-title markdown-title"]//text()').getall()
        yield response.follow(
            response.meta['releases_url'],
            callback=self.parse_releases_page,
            meta={'item': item}
        )
        


    def parse_releases_page(self, response):
        """Parse releases page to extract data about the latest release."""
        item = response.meta['item']
        releases = response.css('a::attr(href)').re('.*releases/tag.*') 
        if releases:
            yield response.follow(
                releases[0],
                callback=self.parse_latest_release_info,
                meta={'item': item})
        else:
            yield item
        

    
    def parse_latest_release_info(self, response):
        """Parse info about the latest release."""
        item = response.meta['item']
        
        tag = response.css('h1[class="d-inline mr-3"]::text').get()
        item['latest_release']['tag'] = tag
        
        changelog = response.xpath('//div[@data-test-selector="body-content"]//text()').getall()
        item['latest_release']['changelog'] = changelog
        
        datetime = response.css('[datetime]::attr(datetime)').get()
        item['latest_release']['datetime'] = datetime
        
        yield item





