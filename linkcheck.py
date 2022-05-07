import requests
import json

def checkLink(info):
    # for debugging
    # print(info.status_code)

    # accounts for server errors
    if info.status_code >= 400:
        # forbidden error
        if info.status_code == 403 or info.status_code == 401:
            print("Invalid api key: try refreshing key, or if the key is known to be valid, refresh")
            return False
        # data not found error
        elif info.status_code == 404:
            print("Player not found, maybe try a different region")
            return False
        else:
            raise BaseException(f"Servers may be down or unresponsive: Status {info.status_code}")

    # checks to make sure the request can be returned as json
    try:
        info = info.json()
    except json.JSONDecodeError:
        print("Failed to decode player data")
        return False
    
    return info
    