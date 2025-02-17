from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pydantic import BaseModel

class InfostealerData(BaseModel):
    employees: Optional[int] = None
    employees_url: Optional[int] = None
    thirdparties: Optional[int] = None
    thirdparties_domain: Optional[int] = None
    update: Optional[datetime] = None
    users: Optional[int] = None
    users_url: Optional[int] = None

class PressInfo(BaseModel):
    link: Optional[str] = None
    source: Optional[str] = None
    summary: Optional[str] = None

class GroupInfo(BaseModel):
    name: str
    url: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None

class VictimData(BaseModel):
    victim: str
    activity: Optional[str] = None
    attackdate: Optional[str] = None
    claim_url: Optional[str] = None
    country: str
    description: Optional[str] = None
    discovered: Optional[str] = None
    domain: Optional[str] = None
    duplicates: List[str] = []
    group: str
    infostealer: Optional[InfostealerData] = None
    press: Optional[PressInfo] = None
    screenshot: Optional[str] = None
    url: Optional[str] = None

class AffectedDetails(BaseModel):
    customers: Optional[int] = ""
    employees: Optional[int] = ""
    third_parties: Optional[int] = ""
    claim_url: Optional[str] = ""


class AttackResponse(BaseModel):
    date: str
    country: str
    title: str
    article_url: str
    hacker_group: str
    attack_summary: str
    screenshot: Optional[str] = ''
    victim: str
    domain: str
    affected: AffectedDetails
