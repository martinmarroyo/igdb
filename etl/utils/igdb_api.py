"""A collection of functions used to interact with the IGDB API"""
import json
import requests
from loguru import logger

def get_auth_code(client_id: str, client_secret: str, grant_type: str) -> tuple:
    """Gets the Oauth access token for IGDB"""
    # Build request url
    base_url = "https://id.twitch.tv/oauth2/token?"
    query_str = f"client_id={client_id}&client_secret={client_secret}&grant_type={grant_type}"
    try:
        auth_req = requests.post(base_url+query_str)
        payload = json.loads(auth_req.content)
        if auth_req.status_code == 200:
            logger.info('Auth code obtained')
            return payload, False
        # There request returned an error. Send the message content with the status code
        return payload, auth_req.status_code
    except Exception as ex:
        logger.exception('An error occurred during auth code request. Check credentials and stack trace.')
        return {}, ex


def generate_header(auth_code: dict, client_id: str) -> dict:
    """Generates a header to send with data requests to an IGDB endpoint"""
    return {
        'Client-ID': client_id, 
        'Authorization': f"Bearer {auth_code['access_token']}"
    }