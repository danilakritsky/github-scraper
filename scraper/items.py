# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from datetime import datetime
import scrapy
from scrapy import Field
from itemloaders.processors import Identity, TakeFirst, Join


def parse_utc_string(datestr: str) -> datetime:
    """Parse string containing UTC timestamp an return a corresponding datetime object."""
    return datetime.strptime(datestr, "%Y-%m-%dT%H:%M:%SZ")


def strip_whitespace(text: str) -> str:
    """Strip both leading and trailing whitespace."""
    return text.rstrip().lstrip()


def remove_thousand_separator(int_as_str: str) -> str:
    """Removes thousand separator from a number stored as string."""
    return int_as_str.replace(",", "")

class RepoInfoItem(scrapy.Item):
    """Item encapsulating repository data."""

    account = Field(
        input_processor=Identity(), output_processor=TakeFirst()
    )
    repo = Field(
        input_processor=lambda x: x[0].split("/")[-1], output_processor=TakeFirst()
    )
    about = Field(
        input_processor=Identity(), output_processor=lambda x: strip_whitespace(x[0])
    )
    website_link = Field(input_processor=Identity(), output_processor=TakeFirst())
    stars = Field(
        input_processor=lambda x: int(remove_thousand_separator(x[0])),
        output_processor=TakeFirst(),
    )
    forks = Field(
        input_processor=lambda x: int(remove_thousand_separator(x[0])),
        output_processor=TakeFirst(),
    )
    watching = Field(input_processor=Identity(), output_processor=TakeFirst())
    release_count = Field(
        # return empty list to skip returning empty field
        input_processor=lambda x: int(remove_thousand_separator(x[0])) if x else [],
        output_processor=TakeFirst(),
    )

    main_branch_commit_count = Field(
        input_processor=lambda x: int(remove_thousand_separator(x[0])),
        output_processor=TakeFirst(),
    )
    main_branch_latest_commit_author = Field(
        input_processor=Identity(), output_processor=TakeFirst()
    )
    main_branch_latest_commit_datetime = Field(
        input_processor=Identity(), output_processor=TakeFirst()
    )
    main_branch_latest_commit_message = Field(
        input_processor=Join(), output_processor=lambda x: strip_whitespace(x[0])
    )
    latest_release_tag = Field(input_processor=Identity(), output_processor=TakeFirst())
    latest_release_datetime = Field(
        input_processor=Identity(), output_processor=TakeFirst()
    )
    latest_release_changelog = Field(
        input_processor=Join(), output_processor=lambda x: strip_whitespace(x[0])
    )