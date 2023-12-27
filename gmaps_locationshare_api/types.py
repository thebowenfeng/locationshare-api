from dataclasses import dataclass


@dataclass
class Location:
    longitude: float
    latitude: float
    address: str


@dataclass
class Person:
    id: str
    profile_pic_url: str
    fullname: str
    nickname: str
    location: Location
    battery: int
