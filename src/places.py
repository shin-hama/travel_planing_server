import base64
from dataclasses import dataclass, asdict
import os

import googlemaps


@dataclass
class PlacesPhotosParams:
    place_id: str
    max_width: int
    max_height: int


@dataclass
class PlaceParams:
    place_id: str
    fields: list[str]
    language: str = "jp"


class Places:
    def __init__(self):
        self.gmaps = googlemaps.Client(key=os.environ.get("GOOGLE_MAP_API_KEY"))

    def get_place(self, params: PlaceParams):

        # Request directions via public transit
        _result = self.gmaps.place(**asdict(params))
        return _result["result"]

    def get_photo(self, params: dict) -> dict[str, str]:
        try:
            args = PlacesPhotosParams(**params)
        except Exception as e:
            raise e

        place = self.get_place(
            PlaceParams(place_id=args.place_id, fields=["photo"], language="jp")
        )
        photo_result = place["photos"][0]
        print(photo_result)

        # Request directions via public transit
        _result = self.gmaps.places_photo(
            **{
                "photo_reference": photo_result["photo_reference"],
                "max_width": args.max_width,
                "max_height": args.max_height,
            }
        )
        img = b"".join([r for r in _result])
        img_base64 = base64.b64encode(img)

        return {
            "image": img_base64.decode("utf-8"),
            "html_attribute": photo_result["html_attributions"],
        }


if __name__ == "__main__":
    import dotenv

    dotenv.load_dotenv("./.env")

    result = Places().get_photo(
        {
            "place_id": "ChIJmSDOgYFSGGARdwamwpOYorM",
            "max_width": 1080,
            "max_height": 1080,
        }
    )
    print(result)
