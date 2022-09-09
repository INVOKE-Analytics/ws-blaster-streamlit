from enum import Enum
from pydantic import BaseModel


class Platform(str, Enum):
    Ayuh_Malaysia = "Ayuh_Malaysia"
    meniaga = "meniaga"
    decoris = "Decoris"

class PlatformPath(str, Enum):
    path = "/home/ammar/wsbAPI/venvWSBAPI/User"


class ListClient(str, Enum):
    pass

class PostSim(BaseModel):
    id:int
    simcard_name:str

class GetSim(PostSim):
    pass