# Import Elasticsearch package 
from elasticsearch import Elasticsearch 
import params

database=params.get('Elasticsearch','database')
port=params.get('Elasticsearch','port')

#Create index lora by 
#http://localhost:9200/lora


# Connect to the elastic cluster
def connect():
    es=Elasticsearch([{'host':database,'port':port}])
    #print(es)
    return es

# Insert
def insert(es , data,indexName = "lora"):
    #print(data)
    #Now let's store this document in Elasticsearch 
    res = es.index(index=indexName,doc_type="lora",body=data)
    return res