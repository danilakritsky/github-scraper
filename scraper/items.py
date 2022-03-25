# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field
from itemloaders.processors import Identity, TakeFirst, MapCompose, Join


class LatestReleaseItem(scrapy.Item):
    """Item encapsulating the latest release data."""
    tag = Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )
    datetime = Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )
    changelog = Field(
        input_processor=Join(),
        output_processor=lambda x: x[0].rstrip().lstrip()
    )

    
class MainBranchItem(scrapy.Item):
    """Item encapsulating main branch data."""
    commit_count = Field(
        input_processor=lambda x: x[0].replace(',', ''),  # remove the thousands separator
        output_processor=lambda x: int(x[0])
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
        input_processor=Join(),
        output_processor=lambda x: x[0].rstrip().lstrip()
    )

class RepoInfoItem(scrapy.Item):
    """Item encapsulating repository data."""
    account = Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )
    repo_name = Field(
        input_processor=lambda x: x[0].split('/')[-1],
        output_processor=lambda x: x[-1]
    )
    about = Field(
        input_processor=Identity(),
        output_processor=lambda x: x[0].rstrip().lstrip()
    )

    website_link = Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

    stars = Field(
        input_processor=lambda x: x[0].replace(',', ''),  # remove the thousands separator
        output_processor=lambda x: int(x[0])
    )

    forks = Field(
        input_processor=lambda x: x[0].replace(',', ''),
        output_processor=lambda x: int(x[0])
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
        # return empty list to skip returning empty field
        input_processor=lambda x: int(x[0].replace(',', '')) if x else [],
        output_processor=TakeFirst()
    )

    latest_release = Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )