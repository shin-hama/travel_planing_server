import base64
from dataclasses import dataclass
import os

import googlemaps


@dataclass
class PlacesPhotosParams:
    photo_reference: str
    max_width: int
    max_height: int


def get_photo(params: dict) -> dict[str, str]:
    try:
        PlacesPhotosParams(**params)
    except Exception as e:
        raise e

    gmaps = googlemaps.Client(key=os.environ.get("GOOGLE_MAP_API_KEY"))

    # Request directions via public transit
    _result = gmaps.places_photo(**params)
    img = b"".join([r for r in _result])
    img_base64 = base64.b64encode(img)

    return {"result": img_base64.decode("utf-8")}


if __name__ == "__main__":
    import dotenv

    dotenv.load_dotenv("./.env")
    result = get_photo(
        {
            "photo_reference": "CnRvAAAAwMpdHeWlXl-lH0vp7lez4znKPIWSWvgvZFISdKx45AwJVP1Qp37YOrH7sqHMJ8C-vBDC546decipPHchJhHZL94RcTUfPa1jWzo-rSHaTlbNtjh-N68RkcToUCuY9v2HNpo5mziqkir37WU8FJEqVBIQ4k938TI3e7bf8xq-uwDZcxoUbO_ZJzPxremiQurAYzCTwRhE_V0",
            "max_width": 1080,
            "max_height": 1080,
        }
    )
    print(result)
