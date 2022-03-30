"""This module contains the spider for crawling and parsing repo data."""

from .scraper_mongo_spider import ScraperMongoSpider


class ScraperApiSpider(ScraperMongoSpider):
    """Spider to crawl github accounts and collect data on repos.
        Data is saved making requests to an API service, that saved parsed data
        to a postgres database.
    """

    name = "scraper_api"
    custom_settings = {"ITEM_PIPELINES": {"scraper.pipelines.APIPipeline": 100}}
