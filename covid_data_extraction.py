import urllib
import urllib.request
import json
import pandas as pd
from elasticsearch import Elasticsearch as es

iso_code_dict = {
    "OWID_KOS": "KOS"
}

covid_data_link = r"https://covid.ourworldindata.org/data/owid-covid-data.csv"
covid_data = pd.read_csv(covid_data_link)

covid_data = covid_data[covid_data['continent'].notna()]
covid_data = covid_data.replace({"iso_code": iso_code_dict})
covid_data.rename(columns={"location": "country"}, inplace=True)
covid_data["date"] = pd.to_datetime(covid_data["date"], format="%Y-%m-%d")
print(covid_data.dtypes)
# documents = covid_data.to_dict(orient='records')