"""This module contains the spider for crawling and parsing repo data."""

import re
import copy

import scrapy
from scrapy.loader import ItemLoader

from scraper.items import RepoInfoItem
from .scraper_mongo_spider import ScraperMongoSpider


class ScraperApiSpider(ScraperMongoSpider):
    """Spider to crawl github accounts and collect data on repos."""

    name = "scraper_api"
    custom_settings = {"ITEM_PIPELINES": {"scraper.pipelines.APIPipeline": 100}}
