import urllib
import urllib.request
import json
import pandas as pd


iso_code_dict = {
    "OWID_KOS": "KOS"
}

covid_data_link = r"https://covid.ourworldindata.org/data/owid-covid-data.csv"
# with urllib.request.urlopen(covid_data_link) as ourl:
    # covid_data = json.loads(ourl.read().decode())
    # covid_data = pandas.read_csv(ourl.read().decode())

covid_data = pd.read_csv(covid_data_link)

covid_data = covid_data[covid_data['continent'].notna()]
covid_data = covid_data.replace({"iso_code": iso_code_dict})

print(covid_data.dtypes)