import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
 
url = "https://www.immoweb.be/en/classified/house/for-sale/merelbeke/9820/9768055?searchId=621c8a1b690a0"
r = requests.get(url)

soup = BeautifulSoup(r.text, "html.parser")
table = soup.findAll("table", {"class": "classified-table"})

type_property = (
            soup.find("h1", {"class": "classified__title"})
            .text.strip()
            .replace("\n", "")
            .split()[0]
        )

subtype_property = type_property

price = soup.find("span", {"class": "sr-only"}).text.strip().replace("€", "")

price = "None" if price == None else price

 # We limit type_property to house or appartment
if type_property.lower() not in ["house", "appartment"]:
        type_property = "House"

headers_df = [
        "Locality",
        "Type of property",
        "Subtype of property",
        "Price",
        "Type of sale",
        "Number of rooms",
        "Area",
        "Fully equipped kitchen",
        "Furnished",
        "Open fire",
        "Terrace",
        "Garden",
        "Surface of the land",
        "Surface area of the plot of land",
        "Number of facades",
        "Swimming pool",
        "State of the building",
    ]

df = pd.DataFrame(columns=headers_df)

    # dictionary containing the scraped data
my_dict = {}
for table_item in table:

        for row in table_item.find_all("tr", class_="classified-table__row"):

            if row is not None:

                header_row = row.find(
                    "th", class_="classified-table__header", text=True
                )
                data_row = row.find("td", class_="classified-table__data", text=True)

                if header_row is not None and data_row is not None:
                    header_name = str(header_row.string).strip()
                    column_name = str(data_row.string).strip()

                    my_dict[header_name] = column_name

locality = (
        "None"
        if my_dict["Neighbourhood or locality"] == None
        else my_dict["Neighbourhood or locality"]
    )
type_sale = (
        "None" if my_dict["Tenement building"] == None else my_dict["Tenement building"]
    )
numbers_rooms = "None" if my_dict["Bedrooms"] == None else my_dict["Bedrooms"]
area = ""
if my_dict["Kitchen type"] == "Installed":

        kitchen = 1
else:

        kitchen = 0

furnished = "None" if my_dict["Furnished"] == None else my_dict["Furnished"]
    # No info on immoweb about that
open_fire = ""
    # No confirmation on garden on the page but it does have garden surface, so maybe we could use that to confirm that garden exists
garden = ""
surface_of_land = ""
terrace = "None" if my_dict["Terrace"] == None else my_dict["Terrace"]
surface_plot_land = ""
number_facades = (
        "None"
        if my_dict["Number of frontages"] == None
        else my_dict["Number of frontages"]
    )
swimming_pool = ""
state_building = (
        "None"
        if my_dict["Building condition"] == None
        else my_dict["Building condition"]
    )

my_list = [
        locality,
        type_property,
        subtype_property,
        price,
        type_sale,
        numbers_rooms,
        area,
        kitchen,
        furnished,
        open_fire,
        terrace,
        garden,
        surface_of_land,
        surface_plot_land,
        number_facades,
        swimming_pool,
        state_building,
    ]

    # Create new dictionary from headers_df and my_list
new_row = dict(zip(headers_df, my_list))

df = df.append(new_row, ignore_index=True)
    # Replaces Yes and No for 1/0

df["Furnished"] = df["Furnished"].replace({"No": 0, "Yes": 1}).astype(int)
df["Terrace"] = df["Terrace"].replace({"No": 0, "Yes": 1}).astype(int)

    # Convert all empty strings to None
df = df.replace(r"^\s*$", "None", regex=True)
df.head()
print(df.head())

    # return df


"""
# list of urls to test

my_url_list = [
    "https://www.immoweb.be/en/classified/house/for-sale/merelbeke/9820/9768055?searchId=621c8a1b690a0",
    "https://www.immoweb.be/en/classified/apartment-block/for-sale/aarschot/3200/9781041?searchId=621e8012c1135",
    "https://www.immoweb.be/en/classified/house/for-sale/de-panne/8660/9781188?searchId=621e8012c1135",
    "https://www.immoweb.be/en/classified/house/for-sale/brasschaat/2930/9781340?searchId=621e8012c1135",
    "https://www.immoweb.be/en/classified/house/for-sale/hoogstraten/2320/9780998?searchId=621e81bd33bc2",
]


def getDataFrame(my_urls):
    for my_url in my_urls:
        url = my_url
        r = requests.get(url)

        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.findAll("table", {"class": "classified-table"})

        type_property = (
            soup.find("h1", {"class": "classified__title"})
            .text.strip()
            .replace("\n", "")
            .split()[0]
        )

    subtype_property = type_property

    price = soup.find("span", {"class": "sr-only"}).text.strip().replace("€", "")

    price = "None" if price == None else price

    # We limit type_property to house or appartment
    if type_property.lower() not in ["house", "appartment"]:
        type_property = "House"

    headers_df = [
        "Locality",
        "Type of property",
        "Subtype of property",
        "Price",
        "Type of sale",
        "Number of rooms",
        "Area",
        "Fully equipped kitchen",
        "Furnished",
        "Open fire",
        "Terrace",
        "Garden",
        "Surface of the land",
        "Surface area of the plot of land",
        "Number of facades",
        "Swimming pool",
        "State of the building",
    ]

    df = pd.DataFrame(columns=headers_df)

    # dictionary containing the scraped data
    my_dict = {}
    for table_item in table:

        for row in table_item.find_all("tr", class_="classified-table__row"):

            if row is not None:

                header_row = row.find(
                    "th", class_="classified-table__header", text=True
                )
                data_row = row.find("td", class_="classified-table__data", text=True)

                if header_row is not None and data_row is not None:
                    header_name = str(header_row.string).strip()
                    column_name = str(data_row.string).strip()

                    my_dict[header_name] = column_name

    locality = (
        "None"
        if my_dict["Neighbourhood or locality"] == None
        else my_dict["Neighbourhood or locality"]
    )
    type_sale = (
        "None" if my_dict["Tenement building"] == None else my_dict["Tenement building"]
    )
    numbers_rooms = "None" if my_dict["Bedrooms"] == None else my_dict["Bedrooms"]
    area = ""
    if my_dict["Kitchen type"] == "Installed":

        kitchen = 1
    else:

        kitchen = 0

    furnished = "None" if my_dict["Furnished"] == None else my_dict["Furnished"]
    # No info on immoweb about that
    open_fire = ""
    # No confirmation on garden on the page but it does have garden surface, so maybe we could use that to confirm that garden exists
    garden = ""
    surface_of_land = ""
    terrace = "None" if my_dict["Terrace"] == None else my_dict["Terrace"]
    surface_plot_land = ""
    number_facades = (
        "None"
        if my_dict["Number of frontages"] == None
        else my_dict["Number of frontages"]
    )
    swimming_pool = ""
    state_building = (
        "None"
        if my_dict["Building condition"] == None
        else my_dict["Building condition"]
    )

    my_list = [
        locality,
        type_property,
        subtype_property,
        price,
        type_sale,
        numbers_rooms,
        area,
        kitchen,
        furnished,
        open_fire,
        terrace,
        garden,
        surface_of_land,
        surface_plot_land,
        number_facades,
        swimming_pool,
        state_building,
    ]

    # Create new dictionary from headers_df and my_list
    new_row = dict(zip(headers_df, my_list))

    df = df.append(new_row, ignore_index=True)
    # Replaces Yes and No for 1/0

    df["Furnished"] = df["Furnished"].replace({"No": 0, "Yes": 1}).astype(int)
    df["Terrace"] = df["Terrace"].replace({"No": 0, "Yes": 1}).astype(int)

    # Convert all empty strings to None
    df = df.replace(r"^\s*$", "None", regex=True)
    df.head()
    print(df.head())

    # return df


getDataFrame()
"""