# narratives
A fanworks recommender system. Pulls data from Archive of Our Own, including named kudos for works, to create an implicit, item-to-item recommendation. Currently only a sub-network of works have been scraped.  See web page for details.

Elements of architecture:
* Scrapes a list of all fandoms (not currently used for scraping meta-data, but future releases will use this list for determining what to scrape next)
* Scrapes meta-data for each individual work, given a fandom
* Inserts meta-data into a PostgreSQL database.
* Scrapes the names of kudos for each work in the database.
* matrix.py generates a recommender model based on implicit library and data in the database at the time.
* A Flask App does the web-based inference when given a fanworks AO3 ID number, returning a list of 10 IDs (plus meta-data). 

### Known Issues
* 