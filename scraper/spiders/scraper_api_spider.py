"""This module contains the spider for crawling and parsing repo data."""

import re
import copy

import scrapy
from scrapy.loader import ItemLoader

from scraper.items import RepoInfoItem, MainBranchItem, LatestReleaseItem
from .scraper_spider import ScraperSpider

class ScraperApiSpider(ScraperSpider):
    """Spider to crawl github accounts and collect data on repos."""

    name = "scraper_api"
    allowed_domains = ["github.com"]
    custom_settings = {
    'ITEM_PIPELINES': {"scraper.pipelines.APIPipeline": 100}
    }

