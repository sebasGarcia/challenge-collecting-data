import pandas as pd
import numpy as np
import requests

from bs4 import BeautifulSoup
from typing import List


# Work in progress: try to get the missing data, Locality also not showing, just like area, swimming pool..
# Note: Some data is set as default empty because for now I haven't found a way to get that data, I will try..


def getDataFrame(my_urls: List[str]):
    """
    Function that takes list of urls and scrapes the needed data from the given list of urls.

    :params my_urls as list of str
    """

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

    for my_url in my_urls:
        url = my_url
        r = requests.get(url)

        soup = BeautifulSoup(r.text, "html.parser")

        area = None
        more_info = soup.find("p", attrs={"class": "classified__information--property"})
        if more_info != None:
            if len(more_info.text.split()) > 3:
                area = more_info.text.split()[3]

        table = soup.findAll("table", {"class": "classified-table"})

        pre_type_property = soup.find("h1", {"class": "classified__title"})
        if pre_type_property:
            type_property = pre_type_property.text.strip().replace("\n", "").split()[0]
        else:
            type_property = None

        subtype_property = type_property

        price = soup.find("span", {"class": "sr-only"})

        price = "None" if price == None else price.text.strip().replace("€", "")

        # We limit type_property to house or appartment
        if type_property:
            if type_property.lower() not in ["house", "appartment"]:
                type_property = "House"

        # dictionary containing the scraped data
        my_dict = {}
        for table_item in table:

            for row in table_item.find_all("tr", class_="classified-table__row"):

                if row is not None:

                    header_row = row.find(
                        "th", class_="classified-table__header", text=True
                    )
                    data_row = row.find(
                        "td", class_="classified-table__data", text=True
                    )

                    if header_row is not None and data_row is not None:
                        header_name = str(header_row.string).strip()
                        column_name = str(data_row.string).strip()

                        my_dict[header_name] = column_name

        locality = my_dict.get("Neighbourhood or locality")
        type_sale = my_dict.get("Tenement building")
        numbers_rooms = my_dict.get("Bedrooms")

        if my_dict.get("Kitchen type") == "Installed":

            kitchen = 1
        else:

            kitchen = 0

        furnished = my_dict.get("Furnished")
        # No info on immoweb about that
        open_fire = ""
        # No confirmation on garden on the page but it does have garden surface, so maybe we could use that to confirm that garden exists
        garden = ""
        surface_of_land = ""
        terrace = my_dict.get("Terrace")
        surface_plot_land = ""
        number_facades = my_dict.get("Number of frontages")
        swimming_pool = ""
        state_building = my_dict.get("Building condition")
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
        df["Terrace"] = np.where(df["Terrace"] == "Yes", "1", df["Terrace"])
        df["Terrace"] = np.where(df["Terrace"] == "No", "0", df["Terrace"])
        df["Furnished"] = np.where(df["Furnished"] == "Yes", "1", df["Furnished"])
        df["Furnished"] = np.where(df["Furnished"] == "No", "0", df["Furnished"])

        # Convert all empty strings to None
        df = df.replace(r"^\s*$", "None", regex=True)

    df
    df.head()
    # print(df.head())

    return df
    # list of urls to test


# my_url_list = [
#     "https://www.immoweb.be/en/classified/house/for-sale/merelbeke/9820/9768055?searchId=621c8a1b690a0",
#     "https://www.immoweb.be/en/classified/apartment-block/for-sale/aarschot/3200/9781041?searchId=621e8012c1135",
#     "https://www.immoweb.be/en/classified/house/for-sale/de-panne/8660/9781188?searchId=621e8012c1135",
#     "https://www.immoweb.be/en/classified/house/for-sale/brasschaat/2930/9781340?searchId=621e8012c1135",
#     "https://www.immoweb.be/en/classified/house/for-sale/hoogstraten/2320/9780998?searchId=621e81bd33bc2",
# ]


def get_url_list(name: str) -> List[str]:
    """
    Function that takes a name and returns a list of urls form the file with that name

    :params name as str
    """
    prop = pd.read_csv(f"url files/urls_{name}")
    return np.array(prop).reshape((prop.size))[1::2]


def create_new_csv(name: str):
    """
    Function that takes a name refering to one of the url files and creates a .csv file with the related data
    """
    my_url_list = get_url_list(name)
    df = getDataFrame(my_url_list)
    df.to_csv(f"property_files/property_{name}.csv")


create_new_csv("other-property")
