# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

def extract_repo_name(repo_url: str) -> str:
    'Extract repo name from its url.'
    return repo_url.split('/')[-1]

def remove_whitespace(text: str) -> str:
    """Removes whitespace from a string."""
    


class RepoInfo(scrapy.Item):
    """Item encapsulating repository data."""
    account = Field()
    repo_name = Field(
        input_processor=extract_repo_name
    )
    about = Field()
    website_link = Field()
    stars = Field()
    forks = Field()
    watching = Field()
    main_branch_info = Field()
    release_count = Field()
    latest_release = Field()