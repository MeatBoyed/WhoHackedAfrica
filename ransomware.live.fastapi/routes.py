from typing import List
import requests
import re
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from Schemas import AffectedDetails, AttackDetails, AttackResponse


attacks_router = APIRouter()
# book_service = BookService()


@attacks_router.get(
    # "/{country_code}", response_model=List[AttackResponse]
    "/{country_code}", response_model=AttackResponse
)
async def get_attacks_by_country(
    country_code: str,
):
    print("Processing Request for: ", country_code)
    # Make request  
    attacks_res = requests.get(f"https://api.ransomware.live/v2/countrycyberattacks/{country_code}") 
    if (attacks_res.status_code == 400):
        # Country not Found
        return HTTPException(404)

    # Extract Data
    raw_attacks = attacks_res.json()[:5] # Slice to get only first 10

    # Get Victim Data
    attacks: List[AttackDetails] = []
    totalAffectedCustomers = 0
    totalAffectedEmployees = 0
    totalAffectedThirdparties = 0
    print("Processing Victims")
    for attack in raw_attacks:
        # victim_domain = attack.get("domain")
        victim_name = attack.get("victim")
        victim_code = extract_short_code(victim_name)
        victim_res = requests.get(f"https://api.ransomware.live/v2/searchvictims/{victim_code}") # Request Victims data
        
        # if (victim_res.status_code == 200):
        try:
            if (victim_res.json()["error"] == f"No victims found for keyword {victim_code}"):
                print("I AMMMM HERREREERER ERRROORRRRR")
                affectedDetails = AffectedDetails(
                    customers=0,
                    employees=0,
                    third_parties=0,
                    claim_url="",
                )
                attacks.append(AttackDetails(
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
            victim_data = victim_res.json()[0]
            affectedDetails = AffectedDetails(
                customers=victim_data.get("infostealer", {}).get("users", "N/A"),
                employees=victim_data.get("infostealer", {}).get("employees", "N/A"),
                third_parties=victim_data.get("infostealer", {}).get("thirdparties", "N/A"),
                claim_url=victim_data.get("claim_url", {}),
            )
            attackDetails = AttackDetails(
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
            )

            # Draw Insights
            if (attackDetails.affected.customers > 0):
                totalAffectedCustomers += attackDetails.affected.customers
            if (attackDetails.affected.employees > 0):
                totalAffectedEmployees += attackDetails.affected.employees
            if (attackDetails.affected.third_parties > 0):
                totalAffectedThirdparties += attackDetails.affected.third_parties

            attacks.append(attackDetails)


    # Draw basic insights
    # print("Aggregating Insights")
    # totalAffectedCustomers = 0
    # totalAffectedEmployees = 0
    # totalAffectedThirdparties = 0
    # for attack in response:
    #     if (attack.affected.customers > 0):
    #         totalAffectedCustomers +=  
    #     if (attack.affected.employees > 0):
    #         totalAffectedEmployees += 1
    #     if (attack.affected.third_parties > 0):
    #         totalAffectedThirdparties += 1


    print("Returning Collected & Formated Data")
    return AttackResponse(
        total_affected_customers=totalAffectedCustomers,
        total_affected_employees=totalAffectedEmployees,
        total_affected_third_parties=totalAffectedThirdparties,
        total_affected_people=totalAffectedCustomers + totalAffectedEmployees + totalAffectedThirdparties,
        attacks=attacks,
        total_attacks=len(attacks)
    )


def extract_short_code(victim_name: str) -> str:
    """
    Extracts the short code from the victim name.
    If no short code is found, returns an empty string.
    """
    match = re.search(r"\(([^)]+)\)$", victim_name)
    return match.group(1) if match else victim_name