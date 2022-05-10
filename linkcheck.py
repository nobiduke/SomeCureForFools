from distutils.log import debug
import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
import json

def checkLink(info):
    # for debugging
    # print(info.status_code)

    # accounts for server errors
    if info.status_code >= 400:
        # forbidden error
        if info.status_code == 403 or info.status_code == 401:
            raise ValueError("Invalid api key: try refreshing key, or if the key is known to be valid, refresh")
        # data not found error
        elif info.status_code == 404:
            raise ValueError("Player not found, maybe try a different region")
        else:
            raise BaseException(f"Servers may be down or unresponsive: Status {info.status_code}")

    # checks to make sure the request can be returned as json
    try:
        info = info.json()
    except json.JSONDecodeError:
        logging.debug("Failed to decode player data")
        return False
    
    return info
    