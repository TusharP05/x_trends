from pymongo import MongoClient
from datetime import datetime
import uuid
from config.config import MONGODB_URI, DB_NAME, COLLECTION_NAME

class DatabaseManager:
    def __init__(self):
        try:
            self.client = MongoClient(MONGODB_URI, 
                                    tlsAllowInvalidCertificates=True,
                                    ssl=True)
            # Create database and collection if they don't exist
            self.db = self.client[DB_NAME]
            if COLLECTION_NAME not in self.db.list_collection_names():
                self.db.create_collection(COLLECTION_NAME)
            self.collection = self.db[COLLECTION_NAME]
            print("Database and collection ready")
        except Exception as e:
            print(f"Database setup error: {e}")
            raise

    def save_trends(self, trends, ip_address):
        """
        Save trending topics to MongoDB
        Returns the saved record
        """
        try:
            # Create record
            record = {
                "_id": str(uuid.uuid4()),
                "timestamp": datetime.now(),
                "ip_address": ip_address,
                "total_trends": len(trends)
            }
            
            # Add trends to record
            for i, trend in enumerate(trends, 1):
                record[f"nameoftrend{i}"] = trend

            # Insert into MongoDB
            self.collection.insert_one(record)
            print(f"Saved record with ID: {record['_id']}")
            
            # Return record without MongoDB-specific objects
            record['timestamp'] = record['timestamp'].isoformat()
            return record
            
        except Exception as e:
            print(f"Error saving to database: {e}")
            return None

    def get_latest_trends(self):
        """Get most recent trends"""
        try:
            record = self.collection.find_one(
                sort=[("timestamp", -1)]
            )
            if record:
                record['timestamp'] = record['timestamp'].isoformat()
            return record
        except Exception as e:
            print(f"Error retrieving from database: {e}")
            return None

    def get_all_trends(self, limit=10):
        """Get all trend records with limit"""
        try:
            cursor = self.collection.find().sort("timestamp", -1).limit(limit)
            records = []
            for record in cursor:
                record['timestamp'] = record['timestamp'].isoformat()
                records.append(record)
            return records
        except Exception as e:
            print(f"Error retrieving trends: {e}")
            return []

    def close_connection(self):
        """Close MongoDB connection"""
        try:
            if hasattr(self, 'client'):
                self.client.close()
                print("Database connection closed")
        except Exception as e:
            print(f"Error closing database connection: {e}")