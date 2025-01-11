from typing import Dict, TypedDict

import requests

import ipaddress


FREE_IP_API_URL = "https://freeipapi.com/api/json"


class Location(TypedDict):
    country: str
    region: str
    city: str


def get_location(ip: str) -> Location:
    ipaddress.ip_address(ip)
    response = requests.get(f"{FREE_IP_API_URL}/{ip}")
    response.raise_for_status()
    data: Dict[str, str] = response.json()
    return {
        "country": data["countryName"],
        "region": data["regionName"],
        "city": data["cityName"],
    }


if __name__ == "__main__":
    print(get_location("8.8.8.8"))  # Google IP
