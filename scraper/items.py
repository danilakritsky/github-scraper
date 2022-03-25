# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field
from itemloaders.processors import Identity, TakeFirst


def extract_repo_name(repo_url: str) -> str:
    'Extract repo name from its url.'
    return repo_url.split('/')[-1]

def remove_whitespace(text: str) -> str:
    """Removes whitespace from a string."""
    
class MainBranchItem(scrapy.Item):
    commit_count = Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )
    latest_commit_author = Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

    latest_commit_datetime = Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

    latest_commit_message = Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

class RepoInfoItem(scrapy.Item):
    """Item encapsulating repository data."""
    account = Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )
    repo_name = Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )
    about = Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )
    website_link = Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )
    stars = Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )
    forks = Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )
    watching = Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )
    main_branch = Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )
    release_count = Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )
    latest_release = Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )