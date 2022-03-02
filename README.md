# challenge-collecting-data
Becode challenge to train scrapping

## Date
28/02/2022 - 02/03/2022

## The Mission
The real estate company "ImmoEliza" wants to create a machine learning model to make price predictions on real estate sales in Belgium. You must therefore create a dataset that holds the following columns :

Locality Type of property (House/apartment) Subtype of property (Bungalow, Chalet, Mansion, ...) Price Type of sale (Exclusion of life sales) Number of rooms Area Fully equipped kitchen (Yes/No) Furnished (Yes/No) Open fire (Yes/No) Terrace (Yes/No) If yes: Area Garden (Yes/No) If yes: Area Surface of the land Surface area of the plot of land Number of facades Swimming pool (Yes/No) State of the building (New, to be renovated, ...) You must save everything in a csv file.

This data set should contain at least 10.000 input for all Belgium.

## Part one
The script "url file" search for links in a list page showing all of their houses. The goal here was to scrape into that dynamic list and take each house's link reference. 

Wouter can be explain more. 
 
## Part two
We have to create a data scraping code which should work on each url/page of advertisement.

Sebastián can be explain more. 

## Used libraries:
I think , it will be good idea to write Used libraries 's list.

import requests
import pandas as pd
from bs4 import BeautifulSoup
