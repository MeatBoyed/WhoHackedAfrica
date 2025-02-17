#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
API Server for Ransomware.live 
Converted to FastAPI
Original by Julien Mousqueton
'''
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.openapi.utils import get_openapi
from typing import Optional, List, Dict, Any
import json
import datetime
import hashlib
import os.path
from pydantic import BaseModel
import requests
import asyncio
from datetime import datetime, timedelta
from functools import lru_cache

from DataStore import DataStore
from Schemas import InfostealerData, PressInfo

# Constants
POSTS_URL = "https://data.ransomware.live/victims.json"
GROUPS_URL = "https://data.ransomware.live/groups.json"
CYBERATTACKS_URL = "https://raw.githubusercontent.com/Casualtek/Cyberwatch/main/cyberattacks.json"
SCREENSHOT_PATH = "/var/www/ransomware-ng/docs/screenshots/posts/"
SCREENSHOT_URL = "https://images.ransomware.live/screenshots/posts/"

HEADERS = {
    'User-Agent': 'Ransomware.live API v0.2'
}


# Initialize FastAPI and DataStore
app = FastAPI(
    title='Ransomware.live API',
    description='API to query Ransomware.live data.',
    version='1.1',
)

data_store = DataStore()

# Startup Event
@app.on_event("startup")
async def startup_event():
    """Initialize data when the application starts"""
    await data_store.update_data()

# Background Tasks
async def periodic_update():
    """Periodically update the data"""
    while True:
        await data_store.update_data()
        await asyncio.sleep(3600)  # Sleep for 1 hour

@app.on_event("startup")
async def start_periodic_update():
    """Start the periodic update task"""
    asyncio.create_task(periodic_update())

# Helper Functions
def add_screenshot_info(post: Dict[str, Any]) -> Dict[str, Any]:
    post['screenshot'] = ''
    if post['post_url'] is not None:
        post_url_bytes = post["post_url"].encode('utf-8')
        post_md5 = hashlib.md5(post_url_bytes).hexdigest()
        screenshot_file = f"{SCREENSHOT_PATH}{post_md5}.png"
        if os.path.exists(screenshot_file):
            post['screenshot'] = f"{SCREENSHOT_URL}{post_md5}.png"
    return post

# Endpoints
@app.get("/recentvictims", response_model=List[Dict[str, Any]])
async def get_recent_posts():
    """Retrieve the 100 most recent posts."""
    await data_store.update_data()  # This will only update if needed
    posts_data = data_store.get_victims()
    
    for post in posts_data:
        post = add_screenshot_info(post)
    
    sorted_posts = sorted(posts_data[-100:], key=lambda post: post['published'], reverse=True)
    return sorted_posts

@app.get("/groups", response_model=List[Dict[str, Any]])
async def get_all_groups():
    """Retrieve all groups."""
    await data_store.update_data()  # This will only update if needed
    return data_store.get_groups()

@app.get("/group/{group_name}", response_model=Dict[str, Any])
async def get_specific_group(group_name: str):
    """Retrieve a specific group by its name."""
    await data_store.update_data()  # This will only update if needed
    groups_data = data_store.get_groups()
    
    for group in groups_data:
        if group['name'] == group_name:
            return group
            
    raise HTTPException(status_code=404, detail="Group not found")

@app.get("/victims/{year}/{month}", response_model=List[Dict[str, Any]])
@app.get("/victims/{year}", response_model=List[Dict[str, Any]])
async def get_victims(year: int, month: Optional[int] = None):
    """Retrieve posts where year and month match the 'discovered' field."""
    await data_store.update_data()  # This will only update if needed
    posts_data = data_store.get_victims()
    
    for post in posts_data:
        post['discovered'] = str(post['discovered'])
    
    if month:
        month_str = str(month).zfill(2)
        matching_posts = [post for post in posts_data if post['discovered'].startswith(f"{str(year)}-{month_str}")]
    else:
        matching_posts = [post for post in posts_data if post['discovered'].startswith(f"{str(year)}-")]
    
    for post in matching_posts:
        post = add_screenshot_info(post)
    
    return matching_posts

@app.get("/groupvictims/{group_name}", response_model=List[Dict[str, Any]])
async def get_group_victims(group_name: str):
    """Retrieve posts where group_name matches the 'group_name' field."""
    await data_store.update_data()  # This will only update if needed
    posts_data = data_store.get_victims()
    matching_posts = [post for post in posts_data if post['group_name'] == group_name]
    
    for post in matching_posts:
        post = add_screenshot_info(post)
    
    return matching_posts

@app.get("/recentcyberattacks", response_model=List[Dict[str, Any]])
async def get_recent_cyberattacks():
    """Retrieve the last 100 entries from the cyberattacks.json file sorted by date."""
    response = requests.get(CYBERATTACKS_URL)
    if response.status_code == 200:
        cyberattacks_data = response.json()
        sorted_cyberattacks = sorted(cyberattacks_data, key=lambda x: x['date'], reverse=True)
        return sorted_cyberattacks[:100]
    raise HTTPException(status_code=response.status_code, detail="Failed to fetch data from the source")

@app.get("/allcyberattacks", response_model=List[Dict[str, Any]])
async def get_all_cyberattacks():
    """Retrieve all entries from the cyberattacks.json file sorted by date."""
    response = requests.get(CYBERATTACKS_URL)
    if response.status_code == 200:
        cyberattacks_data = response.json()
        return sorted(cyberattacks_data, key=lambda x: x['date'], reverse=True)
    raise HTTPException(status_code=response.status_code, detail="Failed to fetch data from the source")



class GroupInfo(BaseModel):
    name: str
    url: Optional[str]
    description: Optional[str]
    status: Optional[str]

class AttackDetails(BaseModel):
    # Victim information
    victim: str
    activity: Optional[str]
    attackdate: Optional[datetime]
    claim_url: Optional[str]
    country: str
    description: Optional[str]
    discovered: Optional[datetime]
    domain: Optional[str]
    duplicates: List[str] = []
    group: str
    
    # Additional data
    infostealer: Optional[InfostealerData]
    press: Optional[PressInfo]
    screenshot: Optional[str]
    url: Optional[str]
    
    # Group information
    group_info: Optional[GroupInfo]

@app.get("/attacks/{country_code}", response_model=List[AttackDetails])
async def get_country_attacks(country_code: str):
    """
    Retrieve all attacks for a specific country with detailed victim and group information.
    
    Args:
        country_code: Two-letter country code (e.g., 'ZA', 'US')
    
    Returns:
        List of attacks with comprehensive victim, group, and attack information
    """
    # Ensure data is up to date
    await data_store.update_data()
    
    # Get all data
    # victims_data = data_store.get_victims()
    groups_data = data_store.get_groups()
    attacks_data = data_store.get_attacks_by_country(country_code)
    # print("Attacks: ", attacks_data)

    print("GROUP DATA: ", groups_data[0])

    return []
    
    rawVi = {
        'type': 'missing', 
        'loc': ('response', 60, 'group_info'), 
        'msg': 'Field required', 
        'input': {
            'post_title': 'weathersa.co.za', 
            'group_name': 'ransomhub', 
            'discovered': '2025-02-12 10:14:05.794490', 
            'description': "[AI generated] Weathersa.co.za is South Africa's national weather service, providing the most up-to-date weather forecasts, warnings, and observations to the public. The service covers all regions of South Africa, offering detailed reports including temperature, rainfall, wind speed, humidity, and more. The company uses advanced meteorological technology to deliver accurate data useful for various sectors such as agriculture, tourism, and disaster management.", 
            'website': 'weathersa.co.za', 
            'published': '2025-02-12 08:29:36.000000', 
            'post_url': 'http://ransomxifxwc5eteopdobynonjctkxxvap77yqifu2emfbecgbqdw6qd.onion/3b4c885a-d3a4-447d-b6ba-5b34af83ebf0/', 
            'country': 'ZA',
            'activity': 'Public Sector', 
            'duplicates': []
        }
    }

    rawGroup = {
        'name': '0mega', 
        'captcha': False, 
        'parser': True, 
        'javascript_render': False, 
        'meta': None, 
        'locations': [
            {
                'fqdn': 'omegalock5zxwbhswbisc42o2q2i54vdulyvtqqbudqousisjgc7j7yd.onion', 
                'title': '0mega | Blog', 
                'version': 3, 
                'slug': 'http://omegalock5zxwbhswbisc42o2q2i54vdulyvtqqbudqousisjgc7j7yd.onion', 
                'available': False, 
                'updated': '2025-02-15 10:21:12.122854', 
                'lastscrape': '2025-02-16 08:20:36.324630', 
                'enabled': True, 
                'type': 'DLS'
            }, 
            {
                'fqdn': '0mega.cc', 
                'title': '0mega.cc', 
                'version': 0, 
                'slug': 'http://0mega.cc', 
                'available': True, 
                'updated': '2025-02-16 07:22:19.913926', 
                'lastscrape': '2025-02-16 07:22:19.913926', 
                'enabled': True, 
                'type': 'DLS'
            }
        ], 
        'profile': []
    }

    # Create a mapping of group names to their details for faster lookup
    # groups_map = {
    #     group['name']: GroupInfo(
    #         name=group['name'],
    #         url=group.get('url'),
    #         description=group.get('description'),
    #         status=group.get('status')
    #     ) for group in groups_data
    # }
    
    # Filter and combine data for the specified country
    # country_attacks = []
    # for victim in victims_data:
    #     if victim.get('country', '').upper() == country_code.upper():
    #         # Get group information
    #         group_info = groups_map.get(victim.get('group'))
            
    #         # Create press info if available
    #         press_info = None
    #         if 'press' in victim:
    #             press_info = PressInfo(
    #                 link=victim['press'].get('link'),
    #                 source=victim['press'].get('source'),
    #                 summary=victim['press'].get('summary')
    #             )
            
    #         # Create infostealer data if available
    #         infostealer_data = None
    #         if 'infostealer' in victim:
    #             infostealer_data = InfostealerData(**victim['infostealer'])
            
    #         print("Victim: ", victim)
    #         print("Press: ", press_info)
    #         print("Info: ", infostealer_data)
    #         print("Group: ", group_info)
            
    #         responseVictim = {
    #             'post_title': 'Telkom', 
    #             'group_name': 'wannacry', 
    #             'discovered': '2017-05-16 00:00:00.000000', 
    #             'published': '2017-05-16 00:00:00.000000', 
    #             'post_url': '', 
    #             'country': 'ZA', 
    #             'activity': 'Communication', 
    #             'website': '', 
    #             'description': '', 
    #             'duplicates': []
    #         }
            
    #         try:
    #             # Create attack details
    #             attack = AttackDetails(
    #                 # Victim basic info
    #                 victim=victim.get('post_title'),
    #                 activity=victim.get('activity'),
    #                 attackdate=victim.get('published'),
    #                 claim_url=victim.get('claim_url'),
    #                 country=victim.get('country'),
    #                 description=victim.get('description'),
    #                 discovered=victim.get('discovered'),
    #                 domain=victim.get('domain'),
    #                 duplicates=victim.get('duplicates', []),
    #                 group=victim.get('group'),
                    
    #                 # Additional data
    #                 infostealer=infostealer_data,
    #                 press=press_info,
    #                 screenshot=victim.get('screenshot'),
    #                 url=victim.get('url'),
                    
    #                 # Group information
    #                 group_info=group_info
    #             )
    #         except Exception as e:
    #             print("Conversion Error: ", e)
            
    #         country_attacks.append(attack)
    
    # Sort attacks by discovered date, most recent first
    country_attacks.sort(key=lambda x: x.discovered, reverse=True)
    
    if not country_attacks:
        raise HTTPException(
            status_code=404,
            detail=f"No attacks found for country code: {country_code}"
        )
    
    return country_attacks

# Custom exception handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    print(
    '''
       _______________                         |*\_/*|________
      |  ___________  |                       ||_/-\_|______  |
      | |           | |                       | |           | |
      | |   0   0   | |                       | |   0   0   | |
      | |     -     | |                       | |     -     | |
      | |   \___/   | |                       | |   \___/   | |
      | |___     ___| |                       | |___________| |
      |_____|\_/|_____|                       |_______________|
        _|__|/ \|_|_.............💔.............._|________|_
       / ********** \                           / ********** \ 
     /  ************  \  Ransomware.live API  /  ************  \ 
    --------------------                     --------------------
    '''
    )
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)