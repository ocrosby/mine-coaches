from pydantic import BaseModel


class Team(BaseModel):
    name: str
    gender: str
    division: str
    conference_name: str
    conference_tds_id: str
    conference_tds_url: str
    tds_id: str
    tds_url: str
