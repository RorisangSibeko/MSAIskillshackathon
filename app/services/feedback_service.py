"""
Feedback Service for SafeWayAI application.
This module provides functionality for user feedback and safety reports.
"""

import logging
import time
import json
import os
import random
from datetime import datetime
from app.config.azure_config import COSMOS_DB_CONFIG

logger = logging.getLogger(__name__)

class FeedbackService:
    """Service for handling user feedback and safety reports."""
    
    _instance = None
    
    def __new__(cls):
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super(FeedbackService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the feedback service."""
        if self._initialized:
            return
            
        logger.info("Initializing feedback service")
        
        # Initialize configuration
        self.cosmos_config = COSMOS_DB_CONFIG
        
        # Initialize feedback storage
        self.feedback_data = []
        self.safety_reports = []
        self.community_alerts = []
        
        # Load existing data
        self._load_data()
        
        self._initialized = True
    
    def _load_data(self):
        """Load feedback data from storage."""
        try:
            # In a real implementation, this would load from Cosmos DB
            # For now, we'll load from local files if available
            
            # Check for feedback data file
            feedback_file = os.path.join("data", "feedback.json")
            if os.path.exists(feedback_file):
                with open(feedback_file, 'r') as f:
                    self.feedback_data = json.load(f)
                logger.info(f"Loaded {len(self.feedback_data)} feedback items")
            
            # Check for safety reports file
            reports_file = os.path.join("data", "safety_reports.json")
            if os.path.exists(reports_file):
                with open(reports_file, 'r') as f:
                    self.safety_reports = json.load(f)
                logger.info(f"Loaded {len(self.safety_reports)} safety reports")
            
            # Check for community alerts file
            alerts_file = os.path.join("data", "community_alerts.json")
            if os.path.exists(alerts_file):
                with open(alerts_file, 'r') as f:
                    self.community_alerts = json.load(f)
                logger.info(f"Loaded {len(self.community_alerts)} community alerts")
            
            # If no data was loaded, generate some sample data
            if not self.feedback_data and not self.safety_reports and not self.community_alerts:
                self._generate_sample_data()
                
        except Exception as e:
            logger.error(f"Error loading feedback data: {e}")
            # Generate sample data as fallback
            self._generate_sample_data()
    
    def _save_data(self):
        """Save feedback data to storage."""
        try:
            # In a real implementation, this would save to Cosmos DB
            # For now, we'll save to local files
            
            # Create data directory if it doesn't exist
            os.makedirs("data", exist_ok=True)
            
            # Save feedback data
            with open(os.path.join("data", "feedback.json"), 'w') as f:
                json.dump(self.feedback_data, f, indent=2)
            
            # Save safety reports
            with open(os.path.join("data", "safety_reports.json"), 'w') as f:
                json.dump(self.safety_reports, f, indent=2)
            
            # Save community alerts
            with open(os.path.join("data", "community_alerts.json"), 'w') as f:
                json.dump(self.community_alerts, f, indent=2)
                
            logger.info("Feedback data saved successfully")
            
        except Exception as e:
            logger.error(f"Error saving feedback data: {e}")
    
    def _generate_sample_data(self):
        """Generate sample feedback data for testing."""
        logger.info("Generating sample feedback data")
        
        # Generate sample feedback
        feedback_types = ["app", "route", "safety", "feature"]
        feedback_sentiments = ["positive", "negative", "neutral", "suggestion"]
        
        for i in range(10):
            feedback = {
                "id": f"feedback_{i}",
                "user_id": f"user_{random.randint(1, 100)}",
                "type": random.choice(feedback_types),
                "sentiment": random.choice(feedback_sentiments),
                "content": self._generate_sample_feedback(),
                "rating": random.randint(1, 5),
                "timestamp": self._random_past_date(),
                "status": random.choice(["new", "reviewed", "addressed"])
            }
            self.feedback_data.append(feedback)
        
        # Generate sample safety reports
        report_types = ["crime", "hazard", "lighting", "infrastructure"]
        severity_levels = ["low", "medium", "high", "critical"]
        
        for i in range(20):
            # Generate random coordinates in Johannesburg area
            lat = -26.2041 + (random.random() * 0.1 - 0.05)
            lon = 28.0473 + (random.random() * 0.1 - 0.05)
            
            report = {
                "id": f"report_{i}",
                "user_id": f"user_{random.randint(1, 100)}",
                "type": random.choice(report_types),
                "severity": random.choice(severity_levels),
                "description": self._generate_sample_report(report_types[i % len(report_types)]),
                "location": {
                    "latitude": lat,
                    "longitude": lon,
                    "address": f"Sample Address {i}, Johannesburg"
                },
                "timestamp": self._random_past_date(),
                "status": random.choice(["pending", "verified", "resolved"]),
                "verification_count": random.randint(0, 10)
            }
            self.safety_reports.append(report)
        
        # Generate sample community alerts
        alert_types = ["crime_pattern", "safety_tip", "community_event", "emergency"]
        
        for i in range(5):
            # Generate random coordinates in Johannesburg area
            lat = -26.2041 + (random.random() * 0.1 - 0.05)
            lon = 28.0473 + (random.random() * 0.1 - 0.05)
            
            alert = {
                "id": f"alert_{i}",
                "type": random.choice(alert_types),
                "title": f"Sample Alert {i}",
                "description": self._generate_sample_alert(alert_types[i % len(alert_types)]),
                "location": {
                    "latitude": lat,
                    "longitude": lon,
                    "radius": random.randint(1, 5),  # km
                    "address": f"Sample Area {i}, Johannesburg"
                },
                "start_time": self._random_past_date(),
                "end_time": self._random_future_date(),
                "severity": random.choice(severity_levels),
                "source": random.choice(["community", "police", "system", "verified_user"]),
                "active": random.choice([True, False])
            }
            self.community_alerts.append(alert)
        
        # Save the generated data
        self._save_data()
    
    def _random_past_date(self):
        """Generate a random date in the past 30 days."""
        days_ago = random.randint(0, 30)
        seconds_ago = random.randint(0, 86400)
        timestamp = time.time() - (days_ago * 86400) - seconds_ago
        return datetime.fromtimestamp(timestamp).isoformat()
    
    def _random_future_date(self):
        """Generate a random date in the next 30 days."""
        days_ahead = random.randint(0, 30)
        seconds_ahead = random.randint(0, 86400)
        timestamp = time.time() + (days_ahead * 86400) + seconds_ahead
        return datetime.fromtimestamp(timestamp).isoformat()
    
    def _generate_sample_feedback(self):
        """Generate sample feedback content."""
        feedback_templates = [
            "I love this app! It's helped me feel much safer when walking home.",
            "The route suggestions are good, but sometimes take me on longer paths than necessary.",
            "Would be great if you could add more transportation options like bikes and scooters.",
            "The safety alerts are really helpful, especially at night.",
            "App crashes sometimes when I try to share my route with friends.",
            "Would love to see integration with ride-sharing services for late night travel.",
            "The emergency button feature gives me peace of mind.",
            "Sometimes the app is slow to load the map.",
            "Great concept, but needs more accurate crime data in my area.",
            "The UI is intuitive and easy to use."
        ]
        return random.choice(feedback_templates)
    
    def _generate_sample_report(self, report_type):
        """Generate sample safety report description based on type."""
        if report_type == "crime":
            templates = [
                "Witnessed a mugging at this location around 8pm.",
                "My car was broken into while parked here.",
                "Several people in the area warned me about pickpockets here.",
                "Saw suspicious activity that looked like drug dealing.",
                "Was followed by someone for several blocks in this area."
            ]
        elif report_type == "hazard":
            templates = [
                "Large pothole in the middle of the road.",
                "Fallen tree blocking part of the sidewalk.",
                "Construction site with inadequate barriers.",
                "Broken glass scattered across the walking path.",
                "Flooding after rain makes this area impassable."
            ]
        elif report_type == "lighting":
            templates = [
                "Street lights are out on this entire block.",
                "This alley has no lighting at all.",
                "The park is completely dark after sunset.",
                "Lights are flickering and unreliable in this area.",
                "The underpass is poorly lit and feels unsafe."
            ]
        elif report_type == "infrastructure":
            templates = [
                "Sidewalk is completely broken and unwalkable.",
                "No pedestrian crossing despite heavy traffic.",
                "Bridge feels unstable and unsafe to cross.",
                "No wheelchair accessibility in this area.",
                "Narrow path forces pedestrians to walk in the road."
            ]
        else:
            templates = [
                "General safety concern in this area.",
                "Doesn't feel safe to walk here, especially at night.",
                "Area seems neglected and potentially dangerous.",
                "Multiple safety issues observed here.",
                "Would not recommend walking through this area."
            ]
        
        return random.choice(templates)
    
    def _generate_sample_alert(self, alert_type):
        """Generate sample community alert description based on type."""
        if alert_type == "crime_pattern":
            templates = [
                "Multiple car break-ins reported in this area over the past week.",
                "Series of smartphone thefts reported at this location.",
                "Increase in home burglaries in this neighborhood.",
                "Several reports of pickpocketing near the train station.",
                "Pattern of robberies targeting people leaving the ATM."
            ]
        elif alert_type == "safety_tip":
            templates = [
                "Avoid walking alone in this area after dark.",
                "Keep valuables out of sight when walking through this neighborhood.",
                "Use well-lit main roads rather than shortcuts through this area.",
                "Be extra vigilant around the market area during busy periods.",
                "Consider ride-sharing instead of walking in this area at night."
            ]
        elif alert_type == "community_event":
            templates = [
                "Community safety walk scheduled for this Saturday at 10am.",
                "Neighborhood watch meeting at the community center this Thursday.",
                "Safety awareness workshop being held at the local library.",
                "Police community outreach event this weekend.",
                "Street lighting improvement project starting next week."
            ]
        elif alert_type == "emergency":
            templates = [
                "Avoid this area due to ongoing police activity.",
                "Flash flooding reported in this location - seek alternative routes.",
                "Gas leak reported - authorities have cordoned off the area.",
                "Major traffic accident blocking all lanes - area congested.",
                "Fire at commercial building - emergency services on scene."
            ]
        else:
            templates = [
                "General safety alert for this area.",
                "Exercise caution when traveling through this location.",
                "Temporary safety concern in this neighborhood.",
                "Reported issues affecting safety in this area.",
                "Community members have flagged this location as concerning."
            ]
        
        return random.choice(templates)
    
    def add_feedback(self, user_id, feedback_type, content, rating=None):
        """
        Add new user feedback.
        
        Args:
            user_id (str): User identifier
            feedback_type (str): Type of feedback (app, route, safety, feature)
            content (str): Feedback content
            rating (int, optional): Rating (1-5)
            
        Returns:
            str: Feedback ID
        """
        try:
            # Generate feedback ID
            feedback_id = f"feedback_{int(time.time())}_{user_id}"
            
            # Determine sentiment (in a real implementation, this would use AI)
            sentiment = "neutral"
            if rating:
                if rating >= 4:
                    sentiment = "positive"
                elif rating <= 2:
                    sentiment = "negative"
            
            # Create feedback item
            feedback = {
                "id": feedback_id,
                "user_id": user_id,
                "type": feedback_type,
                "sentiment": sentiment,
                "content": content,
                "rating": rating,
                "timestamp": datetime.now().isoformat(),
                "status": "new"
            }
            
            # Add to feedback data
            self.feedback_data.append(feedback)
            
            # Save data
            self._save_data()
            
            logger.info(f"Added new feedback: {feedback_id}")
            return feedback_id
            
        except Exception as e:
            logger.error(f"Error adding feedback: {e}")
            return None
    
    def add_safety_report(self, user_id, report_type, description, latitude, longitude, address=None, severity=None):
        """
        Add a new safety report.
        
        Args:
            user_id (str): User identifier
            report_type (str): Type of report (crime, hazard, lighting, infrastructure)
            description (str): Report description
            latitude (float): Location latitude
            longitude (float): Location longitude
            address (str, optional): Location address
            severity (str, optional): Severity level (low, medium, high, critical)
            
        Returns:
            str: Report ID
        """
        try:
            # Generate report ID
            report_id = f"report_{int(time.time())}_{user_id}"
            
            # Default severity if not provided
            if not severity:
                severity = "medium"
            
            # Create report item
            report = {
                "id": report_id,
                "user_id": user_id,
                "type": report_type,
                "severity": severity,
                "description": description,
                "location": {
                    "latitude": latitude,
                    "longitude": longitude,
                    "address": address or f"Location at {latitude:.4f}, {longitude:.4f}"
                },
                "timestamp": datetime.now().isoformat(),
                "status": "pending",
                "verification_count": 0
            }
            
            # Add to safety reports
            self.safety_reports.append(report)
            
            # Check if this should generate a community alert
            self._check_for_alert_generation(report)
            
            # Save data
            self._save_data()
            
            logger.info(f"Added new safety report: {report_id}")
            return report_id
            
        except Exception as e:
            logger.error(f"Error adding safety report: {e}")
            return None
    
    def _check_for_alert_generation(self, new_report):
        """
        Check if a new report should generate a community alert.
        
        Args:
            new_report (dict): The new safety report
            
        Returns:
            bool: Whether an alert was generated
        """
        try:
            # In a real implementation, this would use more sophisticated logic
            # For now, we'll use some simple rules
            
            # Check for critical severity
            if new_report["severity"] == "critical":
                self._generate_alert_from_report(new_report)
                return True
            
            # Check for multiple reports in the same area
            similar_reports = []
            for report in self.safety_reports:
                # Skip the new report itself
                if report["id"] == new_report["id"]:
                    continue
                
                # Check if report is in the same area (within ~500m)
                if self._are_locations_close(
                    report["location"]["latitude"], 
                    report["location"]["longitude"],
                    new_report["location"]["latitude"],
                    new_report["location"]["longitude"],
                    0.005  # Approximately 500m
                ):
                    # Check if it's the same type and recent (within 7 days)
                    if (report["type"] == new_report["type"] and 
                        self._is_recent(report["timestamp"], 7)):
                        similar_reports.append(report)
            
            # If we have 3 or more similar reports, generate an alert
            if len(similar_reports) >= 2:
                self._generate_alert_from_multiple_reports(new_report, similar_reports)
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking for alert generation: {e}")
            return False
    
    def _generate_alert_from_report(self, report):
        """
        Generate a community alert from a single report.
        
        Args:
            report (dict): The safety report
            
        Returns:
            str: Alert ID
        """
        try:
            # Generate alert ID
            alert_id = f"alert_{int(time.time())}"
            
            # Map report type to alert type
            alert_type_map = {
                "crime": "crime_pattern",
                "hazard": "safety_tip",
                "lighting": "safety_tip",
                "infrastructure": "safety_tip"
            }
            alert_type = alert_type_map.get(report["type"], "safety_tip")
            
            # Create alert
            alert = {
                "id": alert_id,
                "type": alert_type,
                "title": f"Safety Alert: {report['type'].capitalize()} Reported",
                "description": f"ALERT: {report['description']} Please exercise caution in this area.",
                "location": {
                    "latitude": report["location"]["latitude"],
                    "longitude": report["location"]["longitude"],
                    "radius": 1,  # 1km radius
                    "address": report["location"]["address"]
                },
                "start_time": datetime.now().isoformat(),
                "end_time": self._get_future_date(3),  # 3 days in the future
                "severity": report["severity"],
                "source": "verified_user",
                "active": True
            }
            
            # Add to community alerts
            self.community_alerts.append(alert)
            
            # Save data
            self._save_data()
            
            logger.info(f"Generated community alert from report: {alert_id}")
            return alert_id
            
        except Exception as e:
            logger.error(f"Error generating alert from report: {e}")
            return None
    
    def _generate_alert_from_multiple_reports(self, new_report, similar_reports):
        """
        Generate a community alert from multiple similar reports.
        
        Args:
            new_report (dict): The new safety report
            similar_reports (list): List of similar reports
            
        Returns:
            str: Alert ID
        """
        try:
            # Generate alert ID
            alert_id = f"alert_{int(time.time())}"
            
            # Calculate average location
            lat_sum = new_report["location"]["latitude"]
            lon_sum = new_report["location"]["longitude"]
            for report in similar_reports:
                lat_sum += report["location"]["latitude"]
                lon_sum += report["location"]["longitude"]
            
            avg_lat = lat_sum / (len(similar_reports) + 1)
            avg_lon = lon_sum / (len(similar_reports) + 1)
            
            # Determine maximum severity
            all_reports = similar_reports + [new_report]
            severity_levels = {"low": 1, "medium": 2, "high": 3, "critical": 4}
            max_severity = "low"
            
            for report in all_reports:
                if severity_levels.get(report["severity"], 0) > severity_levels.get(max_severity, 0):
                    max_severity = report["severity"]
            
            # Create alert
            alert = {
                "id": alert_id,
                "type": "crime_pattern" if new_report["type"] == "crime" else "safety_tip",
                "title": f"Multiple {new_report['type'].capitalize()} Reports in Area",
                "description": f"COMMUNITY ALERT: Multiple reports of {new_report['type']} in this area. {new_report['description']} Please be vigilant.",
                "location": {
                    "latitude": avg_lat,
                    "longitude": avg_lon,
                    "radius": 2,  # 2km radius
                    "address": f"Area around {new_report['location']['address']}"
                },
                "start_time": datetime.now().isoformat(),
                "end_time": self._get_future_date(7),  # 7 days in the future
                "severity": max_severity,
                "source": "community",
                "active": True
            }
            
            # Add to community alerts
            self.community_alerts.append(alert)
            
            # Save data
            self._save_data()
            
            logger.info(f"Generated community alert from multiple reports: {alert_id}")
            return alert_id
            
        except Exception as e:
            logger.error(f"Error generating alert from multiple reports: {e}")
            return None
    
    def verify_report(self, report_id, user_id):
        """
        Verify a safety report.
        
        Args:
            report_id (str): Report identifier
            user_id (str): User identifier
            
        Returns:
            bool: Success status
        """
        try:
            # Find the report
            for report in self.safety_reports:
                if report["id"] == report_id:
                    # Increment verification count
                    report["verification_count"] += 1
                    
                    # Update status if enough verifications
                    if report["verification_count"] >= 3:
                        report["status"] = "verified"
                        
                        # Check if this should generate a community alert
                        if report["status"] != "verified":
                            self._check_for_alert_generation(report)
                    
                    # Save data
                    self._save_data()
                    
                    logger.info(f"Verified report {report_id} by user {user_id}")
                    return True
            
            logger.warning(f"Report not found: {report_id}")
            return False
            
        except Exception as e:
            logger.error(f"Error verifying report: {e}")
            return False
    
    def get_feedback(self, feedback_id=None):
        """
        Get feedback data.
        
        Args:
            feedback_id (str, optional): Specific feedback ID to retrieve
            
        Returns:
            dict or list: Feedback data
        """
        try:
            if feedback_id:
                # Find specific feedback
                for feedback in self.feedback_data:
                    if feedback["id"] == feedback_id:
                        return feedback
                return None
            else:
                # Return all feedback
                return self.feedback_data
                
        except Exception as e:
            logger.error(f"Error getting feedback: {e}")
            return None
    
    def get_safety_reports(self, report_id=None, area=None, report_type=None, recent_days=None):
        """
        Get safety reports.
        
        Args:
            report_id (str, optional): Specific report ID to retrieve
            area (dict, optional): Area to filter by (center and radius)
            report_type (str, optional): Type of reports to filter by
            recent_days (int, optional): Only return reports from the last N days
            
        Returns:
            dict or list: Safety report data
        """
        try:
            if report_id:
                # Find specific report
                for report in self.safety_reports:
                    if report["id"] == report_id:
                        return report
                return None
            
            # Filter reports
            filtered_reports = self.safety_reports
            
            # Filter by area
            if area and "latitude" in area and "longitude" in area and "radius" in area:
                filtered_reports = [
                    report for report in filtered_reports
                    if self._are_locations_close(
                        report["location"]["latitude"],
                        report["location"]["longitude"],
                        area["latitude"],
                        area["longitude"],
                        area["radius"] / 111  # Convert km to degrees (approximate)
                    )
                ]
            
            # Filter by type
            if report_type:
                filtered_reports = [
                    report for report in filtered_reports
                    if report["type"] == report_type
                ]
            
            # Filter by recency
            if recent_days:
                filtered_reports = [
                    report for report in filtered_reports
                    if self._is_recent(report["timestamp"], recent_days)
                ]
            
            return filtered_reports
                
        except Exception as e:
            logger.error(f"Error getting safety reports: {e}")
            return None
    
    def get_community_alerts(self, alert_id=None, area=None, active_only=False):
        """
        Get community alerts.
        
        Args:
            alert_id (str, optional): Specific alert ID to retrieve
            area (dict, optional): Area to filter by (center and radius)
            active_only (bool, optional): Only return active alerts
            
        Returns:
            dict or list: Community alert data
        """
        try:
            if alert_id:
                # Find specific alert
                for alert in self.community_alerts:
                    if alert["id"] == alert_id:
                        return alert
                return None
            
            # Filter alerts
            filtered_alerts = self.community_alerts
            
            # Filter by active status
            if active_only:
                filtered_alerts = [
                    alert for alert in filtered_alerts
                    if alert["active"]
                ]
            
            # Filter by area
            if area and "latitude" in area and "longitude" in area and "radius" in area:
                filtered_alerts = [
                    alert for alert in filtered_alerts
                    if self._are_locations_close(
                        alert["location"]["latitude"],
                        alert["location"]["longitude"],
                        area["latitude"],
                        area["longitude"],
                        (area["radius"] + alert["location"].get("radius", 0)) / 111  # Convert km to degrees (approximate)
                    )
                ]
            
            return filtered_alerts
                
        except Exception as e:
            logger.error(f"Error getting community alerts: {e}")
            return None
    
    def _are_locations_close(self, lat1, lon1, lat2, lon2, threshold):
        """
        Check if two locations are within a threshold distance.
        
        Args:
            lat1 (float): First latitude
            lon1 (float): First longitude
            lat2 (float): Second latitude
            lon2 (float): Second longitude
            threshold (float): Distance threshold in degrees
            
        Returns:
            bool: Whether locations are close
        """
        # Simple Euclidean distance (approximate)
        distance = ((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2) ** 0.5
        return distance <= threshold
    
    def _is_recent(self, timestamp_str, days):
        """
        Check if a timestamp is within the last N days.
        
        Args:
            timestamp_str (str): ISO format timestamp
            days (int): Number of days
            
        Returns:
            bool: Whether the timestamp is recent
        """
        try:
            timestamp = datetime.fromisoformat(timestamp_str)
            now = datetime.now()
            delta = now - timestamp
            return delta.days <= days
        except:
            return False
    
    def _get_future_date(self, days):
        """
        Get a date N days in the future.
        
        Args:
            days (int): Number of days
            
        Returns:
            str: ISO format timestamp
        """
        future = datetime.now().timestamp() + (days * 86400)
        return datetime.fromtimestamp(future).isoformat()
