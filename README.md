ghubscraper
============

A small `scrapy` project that scrapes GitHub account pages, collecting info on accounts' repos and their stats.  
Scraped items are stored in a MongoDB database.
### Services
`scraper` - a `scrapy` project.  
- `./scraper/spiders/scraper_spider.py` - defines a `scraper` spider that does the crawling. 
- `./scraper/items.py` - defines several `Item` objects that are used to process crawled data.
- `./scraper/pipelines.py` - defines a pipeline that stores processed items in a MongoDB database instance.
- `./scraper/settings.py` - stores project settings.

### Deployment

**`docker` must be installed on your system.**  
App is deployed via `docker` CLI using the `Dockerfile` and `docker-compose.yml` files provided in the project's directory.  
These files define two containers - one for the `ghubscraper` project itself and another one for the MongoDB database that will be used to store the scraped data.  
To start both containers in detached mode run the following command:
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
> `docker exec -it mongo sh -c 'mongosh --username ghubscraper --password ghubscraper`
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

