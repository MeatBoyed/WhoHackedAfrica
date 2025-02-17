from typing import List
import requests
import re
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from Schemas import AffectedDetails, AttackResponse


attacks_router = APIRouter()
# book_service = BookService()


@attacks_router.get(
    "/{country_code}", response_model=List[AttackResponse]
)
async def get_attacks_by_country(
    country_code: str,
):
    print("Processing Request for: ", country_code)
    # Make request  
    response = requests.get(f"https://api.ransomware.live/v2/countrycyberattacks/{country_code}") 
    if (response.status_code == 400):
        # Country not Found
        return HTTPException(404);

    # Extract Data
    raw_attacks = response.json()
    attacks = raw_attacks[:5] # Slice to get only first 10
    # print("Fetched Attack: ", attacks[0])

    # Get Victim Data
    response = []
    print("Processing Victims")
    for attack in attacks:
        victim_domain = attack.get("domain")
        victim_name = attack.get("victim")
        victim_code = extract_short_code(victim_name)

        victim_res = requests.get(f"https://api.ransomware.live/v2/searchvictims/{victim_code}") # Request Victims data
        
        # if (victim_res.status_code == 200):

        try:
            if (victim_res.json()["error"] == f"No victims found for keyword {victim_code}"):
                print("I AMMMM HERREREERER ERRROORRRRR")
                # Build Response object
                response.append({
                    "date": attack["date"],  # Attack date
                    "title": attack['title'], # Hacker group
                    "article_url": attack["url"],  # Press source link
                    "hacker_group": "",  # Hacker group
                    "attack_summary": attack.get("summary", "N/A"),  # Attack description
                    "screenshot": "",  # Screenshot of attack leak

                    "victim": attack["victim"],  # Use attack name from API
                    "domain": attack["domain"],  # Use attack name from API
                    "affected": {
                        "affected_customers":"", 
                        "affected_employees": "",  # Compromised employees
                        "third_party_affected": "",
                        "claim_url": ""
                    },
                })
                affectedDetails = AffectedDetails(
                    customers=0,
                    employees=0,
                    third_parties=0,
                    claim_url="",
                )
                response.append(AttackResponse(
                    date= attack["date"],
                    country=attack["country"],
                    title=attack["title"],
                    hacker_group="",
                    attack_summary=attack.get("summary", "N/A"),
                    screenshot="",
                    victim=attack["title"],
                    domain=attack["title"],
                    affected=affectedDetails
                ))
                continue
        except Exception as e:
            # Build Response object
            victim_data = victim_res.json()[0]
            # print("Fetched Victim: ", victim_data)
            # response.append({
            #     "date": attack["date"],  # Attack date
            #     "title": attack['title'], # Hacker group
            #     "hacker_group": victim_data.get("group", "Unknown"),  # Hacker group
            #     "attack_summary": attack.get("summary", "N/A"),  # Attack description
            #     # "press_link": victim_data.get("press", {}).get("source", "N/A"),  # Press source link
            #     "screenshot": victim_data.get("screenshot", "N/A"),  # Screenshot of attack leak

            #     "victim": attack["victim"],  # Use attack name from API
            #     "domain": attack["domain"],  # Use attack name from API
            #     "affected": {
            #         "affected_customers": victim_data.get("infostealer", {}).get("users", "N/A"),  # Compromised customers
            #         "affected_employees": victim_data.get("infostealer", {}).get("employees", "N/A"),  # Compromised employees
            #         "third_party_affected": victim_data.get("infostealer", {}).get("thirdparties", "N/A"),  # Affected third parties
            #         "claim_url": victim_data.get("claim_url", "N/A"),  # Ransom claim link (if exists)
            #     },
            # })
            affectedDetails = AffectedDetails(
                customers=victim_data.get("infostealer", {}).get("users", "N/A"),
                employees=victim_data.get("infostealer", {}).get("employees", "N/A"),
                third_parties=victim_data.get("infostealer", {}).get("thirdparties", "N/A"),
                claim_url=victim_data.get("claim_url", {}),
            )
            response.append(AttackResponse(
                date= attack["date"],
                country=attack["country"],
                title=attack["title"],
                article_url=attack["url"],
                hacker_group=victim_data.get("group", "Unknown"),
                attack_summary=attack.get("summary", "N/A"),
                screenshot=victim_data.get("screenshot", "N/A"),
                victim=attack["title"],
                domain=attack["title"],
                affected=affectedDetails
            ))
            

    print("Returning Collected & Formated Data")
    return response

def extract_short_code(victim_name: str) -> str:
    """
    Extracts the short code from the victim name.
    If no short code is found, returns an empty string.
    """
    match = re.search(r"\(([^)]+)\)$", victim_name)
    return match.group(1) if match else victim_name