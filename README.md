ghubscraper
============

A small dockerized service that scrapes GitHub account pages, collecting info on accounts' repos and their stats.


### Architecture
**ghubscraper** consists of 6 dockerized services that are run together with `docker-compose`.
1. ***scraper*** - contains `scrapy` project and spiders that crawl and parse GitHub account pages for data. Two spiders are defined:
    - *scraper_mongo_spider* - scrapes data and saves them to a MongoDB instance running on ***mongo*** container
    - *scraper_api_spider* - scrapes the same data as the previous spider, but saves it to a PostgreSQL instance by making requests to a specialized web app running on the ***api*** container

    The main task of this service is to deploy these spiders to a remote `scrapyd` server running on ***scrapyd*** container to allow remote scheduling of spiders via sending post requests

2. ***api*** - a dockerized Django Rest Framework app connected to a Postgres database running on ***postgres*** container. API supports adding new repo items to the database, listing all accounts that have been scraped, starting remote jobs on ***scrapyd*** server and getting summary statistics on stored data

3. ***scrapyd*** - server that allow remote scheduling of `scrapy` spiders. Spiders defined in ***scraper*** are deployed here.

4. ***scrapydweb*** - app that provides web UI to the ***scrapyd*** service for easier spider scheduling and logging.

`scraper` - a `scrapy` project.  
- `./scraper/spiders/scraper_spider.py` - defines a `scraper` spider that does the crawling. 
- `./scraper/items.py` - defines several `Item` objects that are used to process crawled data.
- `./scraper/pipelines.py` - defines a pipeline that stores processed items in a MongoDB database instance.
- `./scraper/settings.py` - stores project settings.

### Deployment
Clone the projects' repo and `cd` into it:
> `git clone https://github.com/danilakritsky/ghubscraper`
>
> `cd ghubscraper`
>
**`docker` must be installed on your system.**  
App is deployed via `docker` CLI using the `Dockerfile` and `docker-compose.yml` files provided in the project's directory.  
These files define two containers - one for the `ghubscraper` project itself and another one for the MongoDB database that will be used to store the scraped data.  
To build and start both containers in detached mode run the following command:
> ```docker-compose up -d```

### Example usage

After both containers are started up you can begin scraping.
First, login in into the `ghubscraper` container by running:
> `docker exec -it ghubscraper sh`  
>
When logged in use the following command to scrape *specific account*:
> `scrapy crawl scraper -a start_urls=https://github.com/{ACCOUNT_TO_SCRAPE}`
>
Example:
> `scrapy crawl scraper -a start_urls=https://github.com/danilakritsky`
>
To scrape *multiple accounts* pass a comma delimited list of urls to the `start_urls` parameter:
> `scrapy crawl scraper -a start_urls=https://github.com/danilakritsky,https://github.com/scrapy`
>

To scrape accounts *without logging* into the `ghubscraper` container use:
>`docker exec ghubscraper sh -c 'scrapy crawl scraper -a start_urls=https://github.com/danilakritsky,https://github.com/scrapy'`
>
To examine the stored data login into the `mongo` container's shell by running:
> `docker exec -it mongo sh`  
>
Then use the following command to open the mongo shell:
> `mongosh --username ghubscraper --password ghubscraper`
>
Or skip logging into the container's shell and login to `mongosh` directly from host by running:
> `docker exec -it mongo sh -c 'mongosh --username ghubscraper --password ghubscraper'`
>
After logging in you can examine the stored data by running the following commands:
> `use ghubscraper` 
>
>`db.repos.find()`
>
To stop containers run:
> `docker-compose down`
>
All the data that has been saved to the database will persist in the `./mongodata` directory in the repo's project directory after containers are stopped.

