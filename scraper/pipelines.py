# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from dataclasses import asdict
import pymongo
from scrapy.utils.project import get_project_settings
from .items import RepoInfoItem
import logging
import pymongo

settings = get_project_settings()

# class MongoDBPipeline:
#     """Pipeline to save data to MongoDB."""
#     def __init__(self):
#         conn = pymongo.MongoClient(
#             settings.get('MONGO_HOST'),
#             settings.get('MONGO_PORT')
#         )
#         db = conn[settings.get('MONGO_DB_NAME')]
#         self.collection = db[settings['MONGO_COLLECTION_NAME']]

#     def process_item(self, item, spider):
#         if isinstance(item, RepoInfoItem):
#             self.collection.update(item, upsert=True)
#         else:
#             pass
#             # comments = []
#             # for comment in item.get("comments"):
#             #     comments.append(asdict(comment))
#             # self.collection.update({"_id": item.get("article_id")}, {"$set": {"comments": comments} }, upsert=True)

#         return item


class MongoDBPipeline:
    """Pipeline that save scraped repo data to a MongoDB database."""

    collection_name = "repos"

    def __init__(self):
        """Initialize the pipeline."""
        self.settings = get_project_settings()
        self.mongo_uri = self.settings.get("MONGO_URI")
        self.mongo_database_name = self.settings.get("MONGO_DATABASE_NAME")
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
