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

    def __str__(self):
        return f"Name: '{self.name}', Gender: {self.gender}, Division: {self.division}, Conference: '{self.conference_name}'"

    def __eq__(self, other):
        if isinstance(other, Team):
            return self.name == other.name and self.division == other.division
        return False

    def __hash__(self):
        return hash((self.name, self.gender, self.division, self.conference_name))
