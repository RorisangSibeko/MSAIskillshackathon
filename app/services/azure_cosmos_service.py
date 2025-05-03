"""
Azure Cosmos DB service for SafeWayAI application.
This module provides functionality to interact with Azure Cosmos DB.
"""

import logging
import json
import uuid
from datetime import datetime
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
from app.config.azure_config import COSMOS_DB_CONFIG

logger = logging.getLogger(__name__)

class AzureCosmosService:
    """Service for interacting with Azure Cosmos DB."""
    
    def __init__(self):
        """Initialize the Azure Cosmos DB service."""
        self.endpoint = COSMOS_DB_CONFIG["endpoint"]
        self.key = COSMOS_DB_CONFIG["key"]
        self.database_id = COSMOS_DB_CONFIG["database_id"]
        self.container_id = COSMOS_DB_CONFIG["container_id"]
        
        # Initialize the Cosmos client
        self.client = cosmos_client.CosmosClient(
            self.endpoint, 
            {'masterKey': self.key}
        )
        
        # Initialize database and container
        self._init_database()
        self._init_container()
        
        logger.info("Azure Cosmos DB service initialized")
    
    def _init_database(self):
        """Initialize the database."""
        try:
            # Try to get the database
            self.database = self.client.get_database_client(self.database_id)
            # Check if it exists by reading its properties
            self.database.read()
            logger.info(f"Database '{self.database_id}' already exists")
        except exceptions.CosmosResourceNotFoundError:
            # Create the database if it doesn't exist
            self.database = self.client.create_database(self.database_id)
            logger.info(f"Database '{self.database_id}' created")
    
    def _init_container(self):
        """Initialize the container."""
        try:
            # Try to get the container
            self.container = self.database.get_container_client(self.container_id)
            # Check if it exists by reading its properties
            self.container.read()
            logger.info(f"Container '{self.container_id}' already exists")
        except exceptions.CosmosResourceNotFoundError:
            # Create the container if it doesn't exist
            self.container = self.database.create_container(
                id=self.container_id,
                partition_key=PartitionKey(path="/type"),
                offer_throughput=400
            )
            logger.info(f"Container '{self.container_id}' created")
    
    def create_incident(self, incident_data):
        """
        Create a new incident record in the database.
        
        Args:
            incident_data (dict): The incident data
            
        Returns:
            dict: The created incident record
        """
        try:
            # Ensure required fields
            if "type" not in incident_data:
                incident_data["type"] = "incident"
            
            # Add system fields
            incident_data["id"] = str(uuid.uuid4())
            incident_data["created_at"] = datetime.utcnow().isoformat()
            incident_data["updated_at"] = incident_data["created_at"]
            
            # Create the item
            created_item = self.container.create_item(body=incident_data)
            logger.info(f"Incident created with ID: {created_item['id']}")
            
            return created_item
            
        except exceptions.CosmosHttpResponseError as e:
            logger.error(f"Error creating incident in Cosmos DB: {e}")
            return {"error": str(e)}
    
    def get_incident(self, incident_id):
        """
        Get an incident by ID.
        
        Args:
            incident_id (str): The incident ID
            
        Returns:
            dict: The incident record
        """
        try:
            # Query for the item
            query = f"SELECT * FROM c WHERE c.id = '{incident_id}'"
            items = list(self.container.query_items(
                query=query,
                enable_cross_partition_query=True
            ))
            
            if items:
                return items[0]
            else:
                logger.warning(f"Incident with ID {incident_id} not found")
                return None
                
        except exceptions.CosmosHttpResponseError as e:
            logger.error(f"Error getting incident from Cosmos DB: {e}")
            return {"error": str(e)}
    
    def update_incident(self, incident_id, update_data):
        """
        Update an existing incident.
        
        Args:
            incident_id (str): The incident ID
            update_data (dict): The data to update
            
        Returns:
            dict: The updated incident record
        """
        try:
            # Get the current item
            current_item = self.get_incident(incident_id)
            
            if not current_item or "error" in current_item:
                logger.warning(f"Cannot update incident {incident_id}: not found")
                return {"error": "Incident not found"}
            
            # Update the fields
            for key, value in update_data.items():
                current_item[key] = value
            
            # Update the timestamp
            current_item["updated_at"] = datetime.utcnow().isoformat()
            
            # Replace the item
            updated_item = self.container.replace_item(
                item=current_item["id"],
                body=current_item
            )
            
            logger.info(f"Incident {incident_id} updated")
            return updated_item
            
        except exceptions.CosmosHttpResponseError as e:
            logger.error(f"Error updating incident in Cosmos DB: {e}")
            return {"error": str(e)}
    
    def delete_incident(self, incident_id):
        """
        Delete an incident.
        
        Args:
            incident_id (str): The incident ID
            
        Returns:
            bool: True if deleted successfully, False otherwise
        """
        try:
            # Get the current item to get its partition key
            current_item = self.get_incident(incident_id)
            
            if not current_item or "error" in current_item:
                logger.warning(f"Cannot delete incident {incident_id}: not found")
                return False
            
            # Delete the item
            self.container.delete_item(
                item=incident_id,
                partition_key=current_item["type"]
            )
            
            logger.info(f"Incident {incident_id} deleted")
            return True
            
        except exceptions.CosmosHttpResponseError as e:
            logger.error(f"Error deleting incident from Cosmos DB: {e}")
            return False
    
    def query_incidents(self, query_params=None, max_items=100):
        """
        Query incidents based on parameters.
        
        Args:
            query_params (dict, optional): Query parameters
            max_items (int, optional): Maximum number of items to return
            
        Returns:
            list: List of incident records
        """
        try:
            # Build the query
            query = "SELECT * FROM c WHERE c.type = 'incident'"
            
            if query_params:
                # Add filters based on query parameters
                for key, value in query_params.items():
                    if key == "start_date":
                        query += f" AND c.created_at >= '{value}'"
                    elif key == "end_date":
                        query += f" AND c.created_at <= '{value}'"
                    elif key == "status":
                        query += f" AND c.status = '{value}'"
                    elif key == "severity":
                        query += f" AND c.severity = '{value}'"
                    elif key == "location":
                        # For location, we might want to do a proximity search
                        # This is a simplified version
                        lat, lon = value
                        query += f" AND c.latitude BETWEEN {lat-0.1} AND {lat+0.1}"
                        query += f" AND c.longitude BETWEEN {lon-0.1} AND {lon+0.1}"
            
            # Add order by
            query += " ORDER BY c.created_at DESC"
            
            # Execute the query
            items = list(self.container.query_items(
                query=query,
                enable_cross_partition_query=True,
                max_item_count=max_items
            ))
            
            logger.info(f"Query returned {len(items)} incidents")
            return items
            
        except exceptions.CosmosHttpResponseError as e:
            logger.error(f"Error querying incidents from Cosmos DB: {e}")
            return {"error": str(e)}
    
    def get_incidents_by_location(self, latitude, longitude, radius_km=1.0, max_items=100):
        """
        Get incidents near a specific location.
        
        Args:
            latitude (float): The latitude
            longitude (float): The longitude
            radius_km (float, optional): The radius in kilometers
            max_items (int, optional): Maximum number of items to return
            
        Returns:
            list: List of incident records
        """
        try:
            # This is a simplified approach - in a production system,
            # you would use a spatial index or a more sophisticated
            # proximity calculation
            
            # Convert radius to approximate latitude/longitude range
            # This is a rough approximation and works best near the equator
            lat_range = radius_km / 111.0  # 1 degree latitude is about 111 km
            lon_range = radius_km / (111.0 * abs(math.cos(math.radians(latitude))))
            
            # Build the query
            query = f"""
            SELECT * FROM c 
            WHERE c.type = 'incident'
            AND c.latitude BETWEEN {latitude - lat_range} AND {latitude + lat_range}
            AND c.longitude BETWEEN {longitude - lon_range} AND {longitude + lon_range}
            ORDER BY c.created_at DESC
            """
            
            # Execute the query
            items = list(self.container.query_items(
                query=query,
                enable_cross_partition_query=True,
                max_item_count=max_items
            ))
            
            # Further filter the results by calculating the actual distance
            filtered_items = []
            for item in items:
                # Calculate the actual distance
                distance = self._calculate_distance(
                    latitude, longitude,
                    item["latitude"], item["longitude"]
                )
                
                # Add the distance to the item
                item["distance_km"] = distance
                
                # Include only items within the radius
                if distance <= radius_km:
                    filtered_items.append(item)
            
            logger.info(f"Query returned {len(filtered_items)} incidents within {radius_km} km")
            return filtered_items
            
        except exceptions.CosmosHttpResponseError as e:
            logger.error(f"Error querying incidents by location from Cosmos DB: {e}")
            return {"error": str(e)}
    
    def _calculate_distance(self, lat1, lon1, lat2, lon2):
        """
        Calculate the distance between two points using the Haversine formula.
        
        Args:
            lat1 (float): Latitude of point 1
            lon1 (float): Longitude of point 1
            lat2 (float): Latitude of point 2
            lon2 (float): Longitude of point 2
            
        Returns:
            float: Distance in kilometers
        """
        import math
        
        # Convert latitude and longitude from degrees to radians
        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)
        
        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        r = 6371  # Radius of Earth in kilometers
        
        return c * r
