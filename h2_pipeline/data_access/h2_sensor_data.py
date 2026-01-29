"""
Data access layer for hydrogen pipeline sensor data
"""
import sys
from typing import Optional
from pymongo.collection import Collection
from h2_pipeline.configuration.mongo_db_connection import MongoDBConnection
from h2_pipeline.constants import DATABASE_NAME, COLLECTION_NAME
from h2_pipeline.exception import H2PipelineException


class H2SensorDataRepository:
    """Repository for accessing hydrogen sensor data from MongoDB"""

    def __init__(self):
        """Initialize the data repository"""
        try:
            self.db_connection = MongoDBConnection()
            self.client = self.db_connection.client
            self.database = self.client[DATABASE_NAME]
            self.collection: Collection = self.database[COLLECTION_NAME]
        except Exception as e:
            raise H2PipelineException(e, sys)

    def find_all(self):
        """Find all sensor readings"""
        try:
            return list(self.collection.find())
        except Exception as e:
            raise H2PipelineException(e, sys)

    def find_by_id(self, sensor_id: str):
        """Find sensor reading by ID"""
        try:
            from bson import ObjectId
            return self.collection.find_one({"_id": ObjectId(sensor_id)})
        except Exception as e:
            raise H2PipelineException(e, sys)

    def insert_one(self, data: dict):
        """Insert a single sensor reading"""
        try:
            result = self.collection.insert_one(data)
            return result.inserted_id
        except Exception as e:
            raise H2PipelineException(e, sys)

    def insert_many(self, data_list: list):
        """Insert multiple sensor readings"""
        try:
            result = self.collection.insert_many(data_list)
            return result.inserted_ids
        except Exception as e:
            raise H2PipelineException(e, sys)

    def find_by_query(self, query: dict):
        """Find sensor readings matching query"""
        try:
            return list(self.collection.find(query))
        except Exception as e:
            raise H2PipelineException(e, sys)

    def update_one(self, sensor_id: str, update_data: dict):
        """Update a single sensor reading"""
        try:
            from bson import ObjectId
            result = self.collection.update_one(
                {"_id": ObjectId(sensor_id)},
                {"$set": update_data}
            )
            return result.modified_count
        except Exception as e:
            raise H2PipelineException(e, sys)

    def delete_one(self, sensor_id: str):
        """Delete a sensor reading"""
        try:
            from bson import ObjectId
            result = self.collection.delete_one({"_id": ObjectId(sensor_id)})
            return result.deleted_count
        except Exception as e:
            raise H2PipelineException(e, sys)

    def count_documents(self) -> int:
        """Count total sensor readings"""
        try:
            return self.collection.count_documents({})
        except Exception as e:
            raise H2PipelineException(e, sys)
