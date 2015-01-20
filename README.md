# Crawler for Google Scholar

### Prerequsites

- Scrapy
- pymongo

### Usage

#### Mode 1: Crawl profiles on Google Scholar via bfs

`./run.sh 1 start_url target_database`

start_url is the start point of the bfs;
and target_database is the collection in the MongoDB.

#### Mode 2: Crawl the publications of the corresponding profiles

`./run.sh 2 profile_database`

profile_database is the database crawled in the first step

#### Mode 3: Crawl the publications via the titles directly

To be updated~
