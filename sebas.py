import requests
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://www.immoweb.be/en/classified/house/for-sale/merelbeke/9820/9768055?searchId=621c8a1b690a0'
r= requests.get(url)

soup = BeautifulSoup(r.text, 'html.parser')
table = soup.findAll('table', {'class':'classified-table'})
#This is type property --> Normally this should be house or appartment only
type_property = soup.find("h1", { 'class': 'classified__title'}).text.strip().replace("\n","").split()[0]

subtype_property = type_property

price = soup.find("span", { 'class': 'sr-only'}).text.strip().replace("€","")

#We limit type_property to house or appartment
if(type_property.lower() not in ["house", "appartment"]):
    type_property = "House"

print(type_property)
print(subtype_property)
print("price" + str(price))
headers_df = ["Locality","Type of property", "Subtype of property", "Price", "Type of sale",
"Number of rooms", "Area", "Fully equipped kitchen","Furnished", "Open fire", "Terrace", "Garden", "Surface of the land", "Surface area of the plot of land", "Number of facades", "Swimming pool", "State of the building"]

df = pd.DataFrame(columns = headers_df)

#names on the website
#Type of sale= Tenement building
#Number of rooms = bedrooms


#dictionary containing the scraped data
my_dict = {}
for table_item in table: 
    
    for row in table_item.find_all('tr', class_='classified-table__row'):
    
        if row is not None:
            
            header_row = row.find('th',class_='classified-table__header', text = True)
            data_row = row.find('td', class_='classified-table__data', text = True)

            if header_row is not None and data_row is not None:
                header_name = str(header_row.string).strip()
                column_name = str(data_row.string).strip()
                
                my_dict[header_name] = column_name

df["Locality"]= my_dict["Neighbourhood or locality"]
df["Price"] = price
df["Type of property"] = type_property
df["Subtype of property"] = subtype_property
df["Type of sale"] = my_dict['Tenement building']
df["Number of rooms"] = my_dict['Bedrooms']
df["Area"] = ""

if (my_dict['Tenement building']=="Installed"):
    df["Fully equipped kitchen"] = 1
else:
    df["Fully equipped kitchen"] = 0

df["Furnished"] = my_dict['Furnished']
#No info on immoweb about that
df["Open fire"] = "No"
df["Terrace"] = my_dict["Terrace"]
#No confirmation on garden on the page but it does have garden surface, so maybe we could use that to confirm that garden exists
df["Garden"] = ""
df["Surface of the land"] = ""
df["Terrace"] = my_dict["Terrace"]
df["Surface area of the plot of land"]= ""
df["Number of facades"] = my_dict["Number of frontages"]
df["Swimming pool"] = ""
df["State of the building"]= my_dict["Building condition"]

# TODO Turn later all Yes to 1 and No to 0 and also check if a value exists in a dictionary, otherwise leave it empty
df["Furnished"].map(lambda x: 1 if x == 'Yes' else 0)
df["Terrace"].map(lambda x: 1 if x == 'Yes' else 0)

print(df["Furnished"])

df.head()
