import sys
import os
import pymongo
import certifi
from typing import Optional

from us_visa.exception import USvisaException
from us_visa.logger import logging
from us_visa.constants import DATABASE_NAME, MONGODB_URL_KEY

ca = certifi.where()


class MongoDBClient:
    """
    MongoDB connection manager with connection pooling
    Singleton pattern to ensure single database connection
    
    Attributes:
        client: MongoDB client with connection pooling
        database: Database instance
    """
    
    client: Optional[pymongo.MongoClient] = None
    _instance: Optional['MongoDBClient'] = None

    def __new__(cls, database_name: str = DATABASE_NAME) -> 'MongoDBClient':
        """Implement singleton pattern"""
        if cls._instance is None:
            cls._instance = super(MongoDBClient, cls).__new__(cls)
        return cls._instance

    def __init__(self, database_name: str = DATABASE_NAME) -> None:
        """
        Initialize MongoDB connection with connection pooling
        
        Args:
            database_name: Name of the database to use
            
        Raises:
            USvisaException: If connection fails or environment variable is not set
        """
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY)
                if mongo_db_url is None:
                    raise Exception(
                        f"Environment key: {MONGODB_URL_KEY} is not set."
                    )
                
                # Connection pooling configuration
                MongoDBClient.client = pymongo.MongoClient(
                    mongo_db_url,
                    tlsCAFile=ca,
                    maxPoolSize=50,  # Maximum connections in pool
                    minPoolSize=10,  # Minimum connections in pool
                    maxIdleTimeMS=45000,  # Close connections after 45 seconds
                    connectTimeoutMS=10000,  # Connection timeout
                    serverSelectionTimeoutMS=5000,  # Server selection timeout
                    retryWrites=True,  # Enable retryable writes
                    retryReads=True,  # Enable retryable reads
                )
                
                # Test connection
                MongoDBClient.client.admin.command('ping')
                logging.info("MongoDB connection successful with connection pooling")
            
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            
        except Exception as e:
            logging.error(f"Failed to connect to MongoDB: {str(e)}")
            raise USvisaException(e, sys)

    def close_connection(self) -> None:
        """Close MongoDB connection"""
        try:
            if MongoDBClient.client is not None:
                MongoDBClient.client.close()
                MongoDBClient.client = None
                logging.info("MongoDB connection closed")
        except Exception as e:
            logging.error(f"Error closing MongoDB connection: {str(e)}")
            raise USvisaException(e, sys)