## How to run
Navigate to the directory `./cardata/cardata/spiders` and open a terminal.

To execute the webscraping script, type:
`scrapy crawl cars`. The output csv will be in the main directory.

I read this file into postgres, then used pg_dump to create a sql file of the information.

# Proposal
This project will combine data on used Toyotas from a [used car dataset](https://www.kaggle.com/nileshtiwari7/1000-used-car-price-data), as well as 
data scraped from [www.cars.com](cars.com) on used Toyotas.

Cars.com will be scraped using [Scrapy](https://scrapy.org).

This data will be cleaned using Pandas and then joined into the dataset from Kaggle.

### Extract
Data was scraped from cars.com using an unlimited search distance and 
no maximum price. A spider was created using Scrapy, and the HTML was scraped using Xpath expressions.

Data scraped included year of manufacture, model, condition (new or used), mileage, and price.

### Transform
The data scraped had the car's year, make, and model scraped into a single column. Using Pandas,
this data was broken up so that each parameter was in its own column.

When parsing the HTML, Scrapy's `getall()` method was used to minimize `GET` requests to cars.com.
When trying to get each individual entry one at a time, my requests would often get
blocked by cars.com's servers. This problem was solved by getting all the data in each column
from the site with a single request.

The columns were combined into meaningful data using Python's `zip()` method. From this, a 
Pandas dataframe was created. This dataframe was then combined with the data from Kaggle using
Pandas's `pandas.concat()` method, only keeping shared columns between the two datasets.

### Load
The combined dataframe was saved to a CSV file. The CSV file was loaded into PostgreSQL using
the import feature in pgAdmin. 

The final database contained 1,101 entries. It was exported as an SQL
table using the export feature in pgAdmin.
