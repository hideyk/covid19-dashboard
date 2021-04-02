import yaml
import pandas as pd
import json
from elasticsearch import Elasticsearch, helpers
from datetime import datetime
import pytz

# Obtain configurations from config.yml
config = r"config.yml"
with open(config, 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    host, port, index, columns = config['es_host'], config['es_port'], config['es_index'], config['columns']


# Set-up and clear Elasticsearch index
es = Elasticsearch([{'host': host, 'port': port}])
es.indices.delete(index=index, ignore=[400, 404])


# Pull relevant data from OWID and convert to json
data_url = config['data_url']
df = pd.read_csv(data_url)
df = df[columns]
df['_index'] = index
df.fillna(0, inplace=True)
data_json = json.loads(df.to_json(orient='records'))


# Convert date field to datetime format
for i in range(len(data_json)):
    yyyy, mm, dd = data_json[i]['date'].split("-")
    data_json[i]['date'] = datetime(year=int(yyyy), month=int(mm), day=int(dd)).replace(tzinfo=pytz.utc)
    

# Bulk load records into Elasticsearch
if es.indices.exists(index=index):
    es.indices.refresh(index=index)
    old_docs = es.cat.count(index=index, params={"format": "json"})
    
    backup_index = f"{index}_backup"
    helpers.reindex(client=es, source_index=index, target_index=backup_index, chunk_size=1000)
    helpers.bulk(client=es, actions=data_json, chunk_size=1000, request_timeout=200)

    es.indices.refresh(index=backup_index)
    old_docs = es.cat.count(index=backup_index, params={"format": "json"})
    es.indices.refresh(index=index)
    new_docs = es.cat.count(index=index, params={"format": "json"})

    if new_docs >= old_docs:
        es.indices.delete(index=backup_index, ignore=[400, 404])
    else:
        es.indices.delete(index=index, ignore=[400, 404])
        helpers.reindex(client=es, source_index=backup_index, target_index=index, chunk_size=1000)

else:
    helpers.bulk(client=es, actions=data_json, chunk_size=1000, request_timeout=200)
