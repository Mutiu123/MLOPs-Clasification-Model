import os
import pymongo
from h2_pipeline.constants import MONGODB_URL_KEY


class MongoDBConnection:
    """MongoDB connection management"""
    
    client = None

    def __init__(self):
        """Initialize MongoDB connection"""
        if MongoDBConnection.client is None:
            mongo_db_url = os.getenv(MONGODB_URL_KEY)
            if not mongo_db_url:
                raise Exception(f"Environment variable: {MONGODB_URL_KEY} is not set.")
            
            MongoDBConnection.client = pymongo.MongoClient(mongo_db_url)
        
        self.client = MongoDBConnection.client

    def __del__(self):
        """Close MongoDB connection"""
        if MongoDBConnection.client is not None:
            MongoDBConnection.client.close()
