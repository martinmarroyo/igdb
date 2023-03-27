"""A collection of functions to orchestrate the ETL pipeline from IGDB API to storage"""
import utils.igdb_api as API

def start(client_id: str, client_secret: str, grant_type: str, config: dict) -> tuple:
    """Starts the ETL process"""
    # Get auth code
    auth_code, err = API.get_auth_code(client_id, client_secret, grant_type)
    return True, None # Success, Error