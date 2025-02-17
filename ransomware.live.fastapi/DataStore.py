# Data storage
from typing import Dict, List, Optional
import asyncio
from datetime import datetime, timedelta

from fastapi import HTTPException
import requests

from Schemas import GroupInfo, VictimData

# from api_server import POSTS_URL, HEADERS, GROUPS_URL
POSTS_URL = "https://data.ransomware.live/victims.json"
GROUPS_URL = "https://data.ransomware.live/groups.json"
CYBERATTACKS_URL = "https://raw.githubusercontent.com/Casualtek/Cyberwatch/main/cyberattacks.json"
SCREENSHOT_PATH = "/var/www/ransomware-ng/docs/screenshots/posts/"
SCREENSHOT_URL = "https://images.ransomware.live/screenshots/posts/"

HEADERS = {
    'User-Agent': 'Ransomware.live API v0.2'
}

# class DataStore:
#     def __init__(self):
#         self.victims_data: List[VictimData] = []
#         self.groups_data: List[GroupInfo] = []
#         self.last_update: Optional[datetime] = None
#         self.update_lock = asyncio.Lock()

#     def parse_datetime(value: str) -> Optional[datetime]:
#         """Helper function to parse datetime fields safely."""
#         if value:
#             try:
#                 return datetime.fromisoformat(value)
#             except ValueError:
#                 print(f"Invalid datetime format: {value}")
#         return None

#     async def update_data(self) -> None:
#         """Fetch and update the data if it's older than 1 hour"""
#         async with self.update_lock:
#             current_time = datetime.now()
#             if (self.last_update is None or 
#                 current_time - self.last_update > timedelta(hours=1)):
#                 try:
#                     # Fetch victims data
#                     victims_response = requests.get(POSTS_URL, headers=HEADERS)
#                     victims_response.raise_for_status()
#                     victims_raw = victims_response.json()
                    
#                     print("Victims Data: ", datetime.strptime(victims_raw[0].get("published"), '%Y-%m-%d %H:%M:%S.%f') )
                    
#                     for victim in victims_raw:
#                         self.victims_data.append(VictimData(
#                             victim=victim.get("victim", ""),
#                             activity=victim.get("activity"),
#                             # attackdate=datetime.fromisoformat(victim.get("published")).strftime("%Y-%m-%d %H:%M:%S.%f"),
#                             claim_url=victim.get("claim_url"),
#                             country=victim.get("country", ""),
#                             description=victim.get("description"),
#                             # discovered=victim.get("discovered"),
#                             domain=victim.get("domain"),
#                             duplicates=victim.get("duplicates", []),
#                             group=victim.get("group", ""),
#                             infostealer=victim.get("infostealer"),  # Ensure this maps correctly
#                             press=victim.get("press"),  # Ensure this maps correctly
#                             screenshot=victim.get("screenshot"),
#                             url=victim.get("url"),
#                         ))
                    
#                     # Convert raw victims data to VictimData models
#                     # self.victims_data = [
#                     #     VictimData(
#                     #         victim=victim.get("victim", ""),
#                     #         activity=victim.get("activity"),
#                     #         attackdate=parse_datetime(victim.get("attackdate")),
#                     #         claim_url=victim.get("claim_url"),
#                     #         country=victim.get("country", ""),
#                     #         description=victim.get("description"),
#                     #         discovered=parse_datetime(victim.get("discovered")),
#                     #         domain=victim.get("domain"),
#                     #         duplicates=victim.get("duplicates", []),
#                     #         group=victim.get("group", ""),
#                     #         infostealer=victim.get("infostealer"),  # Ensure this maps correctly
#                     #         press=victim.get("press"),  # Ensure this maps correctly
#                     #         screenshot=victim.get("screenshot"),
#                     #         url=victim.get("url"),
#                     #     )
#                     #     for victim_data in victims_raw
#                     # ]
                    



#                     # Fetch groups data
#                     groups_response = requests.get(GROUPS_URL, headers=HEADERS)
#                     groups_response.raise_for_status()
#                     groups_raw = groups_response.json()
                    
#                     # Convert raw groups data to GroupInfo models
#                     self.groups_data = [
#                         GroupInfo(**group_data)
#                         for group_data in groups_raw
#                     ]

#                     self.last_update = current_time
#                     print(f"Data updated at {self.last_update}")
                
#                 except ValueError as ve:
#                     print(f"Data validation error: {str(ve)}")
#                     raise HTTPException(
#                         status_code=500,
#                         detail="Error validating fetched data"
#                     )
#                 except Exception as e:
#                     print(f"Error updating data: {str(e)}")
#                     if not self.victims_data or not self.groups_data:
#                         raise HTTPException(
#                             status_code=503,
#                             detail="Unable to fetch data and no cached data available"
#                         )

#     def get_victims(self) -> List[VictimData]:
#         """
#         Get the list of victims with proper typing.
        
#         Returns:
#             List[VictimData]: List of victim data objects
#         """
#         return self.victims_data

#     def get_groups(self) -> List[GroupInfo]:
#         """
#         Get the list of groups with proper typing.
        
#         Returns:
#             List[GroupInfo]: List of group info objects
#         """
#         return self.groups_data

#     def get_group_by_name(self, group_name: str) -> Optional[GroupInfo]:
#         """
#         Get a specific group by name.
        
#         Args:
#             group_name: Name of the group to find
            
#         Returns:
#             Optional[GroupInfo]: Group info if found, None otherwise
#         """
#         return next(
#             (group for group in self.groups_data if group.name == group_name),
#             None
#         )

#     def get_victims_by_country(self, country_code: str) -> List[VictimData]:
#         """
#         Get all victims for a specific country.
        
#         Args:
#             country_code: Two-letter country code
            
#         Returns:
#             List[VictimData]: List of victims from the specified country
#         """
#         return [
#             victim for victim in self.victims_data 
#             if victim.country.upper() == country_code.upper()
#         ]

#     def get_victims_by_group(self, group_name: str) -> List[VictimData]:
#         """
#         Get all victims for a specific group.
        
#         Args:
#             group_name: Name of the group
            
#         Returns:
#             List[VictimData]: List of victims attacked by the specified group
#         """
#         return [
#             victim for victim in self.victims_data 
#             if victim.group == group_name
#         ]


# Data storage
class DataStore:
    def __init__(self):
        self.victims_data: List[Dict] = []
        self.groups_data: List[Dict] = []
        self.last_update: Optional[datetime] = None
        self.update_lock = asyncio.Lock()

    async def update_data(self) -> None:
        """Fetch and update the data if it's older than 1 hour"""
        async with self.update_lock:
            current_time = datetime.now()
            if (self.last_update is None or 
                current_time - self.last_update > timedelta(hours=1)):
                try:
                    # Fetch victims data
                    victims_response = requests.get(POSTS_URL, headers=HEADERS)
                    victims_response.raise_for_status()
                    self.victims_data = victims_response.json()

                    # Fetch groups data
                    groups_response = requests.get(GROUPS_URL, headers=HEADERS)
                    groups_response.raise_for_status()
                    self.groups_data = groups_response.json()

                    self.last_update = current_time
                    print(f"Data updated at {self.last_update}")
                except Exception as e:
                    print(f"Error updating data: {str(e)}")
                    if not self.victims_data or not self.groups_data:
                        raise HTTPException(
                            status_code=503,
                            detail="Unable to fetch data and no cached data available"
                        )

    def get_victims(self) -> List[Dict]:
        return self.victims_data

    def get_groups(self) -> List[Dict]:
        return self.groups_data

    def get_attacks_by_country(self, country: str) -> List[Dict]:
        victims = []
        for victim in self.victims_data:
            if (victim.get("country") == country):
                victims.append(victim)              

        return victims

