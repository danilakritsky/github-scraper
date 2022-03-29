"""This module container pipelines for processing parsed items."""

import logging

import pymongo
import scrapy
from scrapy.utils.project import get_project_settings
import json

from .items import RepoInfoItem
from itemadapter import ItemAdapter
from scrapy.http import FormRequest
import requests

settings = get_project_settings()


class MongoDBPipeline:
    """Pipeline that save scraped repo data to a MongoDB database."""

    collection_name = "repos"

    def __init__(self):
        """Initialize the pipeline."""
        self.mongo_uri = settings.get("MONGO_URI")
        self.mongo_database_name = settings.get("MONGO_DATABASE_NAME")
        self.mongo_client: pymongo.MongoClient
        self.mongo_db: pymongo.database.Database

    def open_spider(self, _):
        """Open connection to the MongoDB database when starting the spider."""
        self.mongo_client = pymongo.MongoClient(self.mongo_uri)
        self.mongo_db = self.mongo_client[self.mongo_database_name]

    def close_spider(self, _):
        """Close connection to the MongoDB database when closing the spider."""
        self.mongo_client.close()

    def process_item(self, item, _):
        """Process each item and save it to the database."""
        collection = self.mongo_db[self.collection_name]
        if isinstance(item, RepoInfoItem):
            stored_repo = collection.find_one(
                {
                    "account": (account := item.get("account")),
                    "repo": (repo := item.get("repo")),
                }
            )
            if stored_repo:  # rewrite data
                collection.delete_one({"_id": stored_repo["_id"]})
                logging.info(f"Rewriting existing repo data for '{account}/{repo}'.")
            collection.insert_one(dict(item))
            logging.info(f"Info on '{account}/{repo}' added to MongoDB.")
            return item


class APIPipeline:
    """Pipeline that save scraped repo data to a MongoDB database."""

    def process_item(self, item, _):
        """Process each item and save it to the database."""
        requests.post(
            'http://127.0.0.1:8000/create/',
            data=json.dumps(ItemAdapter(item).asdict()),
            headers={
                'Content-type':'application/json', 
                'Accept':'application/json'
            }
        )
        return item

