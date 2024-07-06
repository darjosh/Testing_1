from typing import Any
import os
import pandas as pd
import pymongo
import json
from ensure import ensure_annotations

class mongo_operation:
    """
    A single call to MongoDB operation.
    
    PARAMS:
    client_url: The client url that you get from mongodb webpage.
    database_name: The database one wants to connect to.
    collection_name: The name of the collection you want to connect to.
    """
    
    _collection = None  # a variable that will be storing the collection name
    
    def __init__(self, client_url: str, database_name: str, collection_name: str = None):
        self.client_url = client_url
        self.database_name = database_name
        self.collection_name = collection_name
    
    @property
    def _create_mongo_client(self):
        """
        To create a MongoClient instance
        
        Returns:
        client: mongodb client instance
        """
        client = pymongo.MongoClient(self.client_url)
        return client

class DatabaseHandler:
    def __init__(self, db_name):
        self.client = MongoClient()
        self.db = self.client[db_name]
        self.__connect_collection = None

    def set_collection(self, collection_name):
        self.__connect_collection = self.db[collection_name]

    def insert_from_file(self, path):
        if path.endswith('.csv'):
            dataframe = pd.read_csv(path, encoding='utf8')
        elif path.endswith('.xlsx'):
            dataframe = pd.read_excel(path, encoding='utf8')
        data_json = json.loads(dataframe.to_json(orient='records'))
        self.__connect_collection.insert_many(data_json)

    @ensure_annotations
    def find(self, collection_name: str = None, query: dict = {}):
        """
        To find data in mongo database
        Returns dataframe of the searched data.
        
        PARAMS:
        query: dict, default : {} which will be fetching all data from the collection
            query to find the data in mongo database
            example of query -- {"name":"sourav"}
        """
        if collection_name:
            self.set_collection(collection_name)
        if collection_name not in self.db.list_collection_names():
            raise NameError(f"Collection '{collection_name}' not found in mongo database. Following collections are available: {self.db.list_collection_names()}")
        cursor = self.__connect_collection.find(query)
        data = pd.DataFrame(list(cursor))
        return data

    @ensure_annotations
    def update(self, where_condition: dict, update_query: dict, update_all_data=False):
        """
        To update data in mongo database

        where_condition: dict,
            to find the data in mongo database -- example of query
        update_query : dict,
            query to update the data in mongo database -- example of query
        update_all : Bool,
            If True, update all data in mongo database
        """
        if update_all_data:
            self.__connect_collection.update_many(where_condition, {'$set': update_query})
        else:
            self.__connect_collection.update_one(where_condition, {'$set': update_query})


    @ensure_annotations
    def set_new_collection(self, collection_name: str):
        """
        To set a new collection name for mongo operation

        Args:
        collection_name (str): pass new collection name that is going to be used
        """
        self.__connect_collection = self.db[collection_name]

    @ensure_annotations
    def insert_record(self, record: dict, collection_name: str) -> Any:
        """
        Insert one record into MongoDB
        
        Params:
        record: dict,
            the data to insert into MongoDB.
        collection_name: str
            the collection to insert the record into.
        """
        self.set_new_collection(collection_name)
        self.__connect_collection.insert_one(record)

    def get_collection(self):
        """
        Get the current collection
        """
        if self.__connect_collection is None:
            raise ValueError("No collection selected. Use set_collection() to select a collection.")
        return self.__connect_collection
    
    @ensure_annotations
    def delete_record(self, where_condition: dict, delete_all=False):
        """
        Summary: 
        Args:
        where_condition (dict):
            column name and value upon which the delete operation will be performed should be passed as dictionary.
            example: {'name': 'Rahul Roy'} -- here column name is 'name' and value is 'Rahul Roy'
        delete_all (bool, optional):
            If multiple records are to be deleted, value would be True
            Default: False.
        """
        if delete_all:
            self.__connect_collection.delete_many(where_condition)
        else:
            self.__connect_collection.delete_one(where_condition)
