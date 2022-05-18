from flask import Request
import functions_framework

import src.directions as directions
import src.places as places


@functions_framework.http
def hello_http(request: Request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    # Set CORS headers for the preflight request
    if request.method == "OPTIONS":
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }

        return ("", 204, headers)

    # Set CORS headers for the main request
    headers = {"Access-Control-Allow-Origin": "*"}

    request_json = request.get_json(silent=True)
    print(request.method)
    print(request.args)
    print(request.path)
    print(request_json)

    if not request_json:
        return (
            {
                "message": "Invalid parameters",
                "status": "failed",
                "route": None,
            },
            headers,
        )

    try:
        if request.path == "/directions":
            return (directions.main(request_json), headers)
        elif request.path == "/places_photos":
            return (places.get_photo(request_json), headers)
        else:
            print("test")
            raise Exception("not implemented")
    except Exception as e:
        print(e.with_traceback(None))
        return (
            {
                "message": "An error has ocurred",
                "status": "failed",
                "route": None,
            },
            headers,
        )
