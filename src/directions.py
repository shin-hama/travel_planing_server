from dataclasses import dataclass, asdict
import os
from typing import Any, Literal, Optional

import googlemaps


@dataclass
class LatLng:
    lat: int
    lng: int


@dataclass
class DirectionsParams:
    origin: LatLng
    destination: LatLng
    mode: Literal["driving", "walking", "bicycling", "transit"]
    waypoints: Optional[list[LatLng]] = None


@dataclass
class Duration:
    text: str
    value: int  # unit: seconds


@dataclass
class Leg:
    duration: Duration


@dataclass
class Response:
    legs: list[Leg]
    ordered_waypoints: list[LatLng]
    waypoint_order: list[int]


def main(params: dict):
    try:
        args = DirectionsParams(**params)
    except Exception as e:
        raise e
    gmaps = googlemaps.Client(key=os.environ.get("GOOGLE_MAP_API_KEY"))

    # Request directions via public transit
    directions_result = gmaps.directions(optimize_waypoints=True, **params)

    result = parse_result(directions_result, args)

    return result


def parse_result(result: list[Any], param: DirectionsParams):
    if not result or len(result) == 0:
        return {"route": None, "status": "failed", "message": "Route does not exist"}

    route: dict = result[0]
    waypoint_order = route.get("waypoint_order")
    legs = route.get("legs")
    ordered = [param.waypoints[i] for i in waypoint_order]

    return {
        "route": asdict(Response(legs, ordered, waypoint_order)),
        "status": "success",
        "message": "success",
    }


if __name__ == "__main__":
    import dotenv

    dotenv.load_dotenv("./.env")
    result = main(
        {
            "origin": {"lat": 35.22, "lng": 135.51},
            "destination": {"lat": 35.02, "lng": 135.79},
            "mode": "driving",
            "waypoints": [
                {"lat": 35.02, "lng": 135.78},
                {"lat": 35.12, "lng": 135.69},
                {"lat": 35.02, "lng": 135.76},
            ],
        }
    )

    print(result)
