# challenge-collecting-data
Becode challenge to train scrapping

## Date
28/02/2022 - 02/03/2022

## Team members
https://github.com/WoutervdVijver

https://github.com/sebasGarcia

https://github.com/mahboubehfaghih

## The Mission
The real estate company "ImmoEliza" wants to create a machine learning model to make price predictions on real estate sales in Belgium. You must therefore create a dataset that holds the following columns :

Locality Type of property (House/apartment) Subtype of property (Bungalow, Chalet, Mansion, ...) Price Type of sale (Exclusion of life sales) Number of rooms Area Fully equipped kitchen (Yes/No) Furnished (Yes/No) Open fire (Yes/No) Terrace (Yes/No) If yes: Area Garden (Yes/No) If yes: Area Surface of the land Surface area of the plot of land Number of facades Swimming pool (Yes/No) State of the building (New, to be renovated, ...) You must save everything in a csv file.

This data set should contain at least 10.000 input for all Belgium.

We decided to scrape "Immoweb": https://www.immoweb.be/en .


## Part one
In the map url files the script 'Wouter_scrape' searches for links in a list page showing all of their houses. The goal here was to scrape into that list and take each house's link reference. For each type of house a file was created of all url links in the map 'url files'. Some threading was included to speed up the process though very minimally.
 
## Part two
We have to create a data scraping code which should work on each url/page of advertisement. This is done with the script 'scrape_data_saveCsv.py'
It was not easy to work on Immoweb with BeautifulSoup because of the dynamic nature of website. A  number of traits needed selenium to be obtained but we decided against due to time pressure.

For each of the types of properties a property_type file was made in the map 'property_files'. Combined this gives data for more than 10000 houses.



## Used libraries:
the libraries used are

- requests
- pandas
- from bs4: BeautifulSoup
