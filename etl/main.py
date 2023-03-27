"""
A worker that grabs data from the `games` endpoint at the IGDB
and writes the data found to storage.

@Author: Martin Arroyo
@Email: martinm.arroyo7@gmail.com

"""
import os
import yaml
from yaml.loader import SafeLoader
from loguru import logger
from pathlib import Path
from utils import pipeline

def main(*args) -> bool:
    # Grab config items
    try:
        client_id, client_secret, grant_type, config = args
    except ValueError as ve:
        logger.info(f'Check to make sure all config values are passed into main: {repr(ve)}\nExiting...')
        return False
    # Start pipeline
    success, err = pipeline.start(client_id, client_secret, grant_type, config)
    if err:
        logger.info(f'There was an error during pipeline execution: {repr(err)}. Review stacktrace and try again.')
        raise err
    
    return success


if __name__ == '__main__':
    # Initialize config and start pipeline
    status = False
    try:
        # Configuration setup
        CLIENT_ID = os.environ['CLIENT_ID']
        CLIENT_SECRET = os.environ['CLIENT_SECRET']
        GRANT_TYPE = os.environ['GRANT_TYPE']
        PIPELINE_CONFIG = os.environ['PIPELINE_CONFIG']
        with open(Path.cwd()/PIPELINE_CONFIG, 'r') as file:
            config = yaml.load(file, Loader=SafeLoader)
        logger.info('Starting pipeline...')
        status = main(CLIENT_ID, CLIENT_SECRET, GRANT_TYPE, config)
    except KeyError as ke:
        logger.info(f'Missing required environment variable(s): {repr(ke)}')
    except FileNotFoundError as fnfe:
        logger.info(f'Missing required config file or incorrect path provided: {Path.cwd()/PIPELINE_CONFIG}: {repr(fnfe)}')
    except Exception:
        logger.exception('An error occurred while starting the pipeline. Exiting...')
    finally:
        if status:
            logger.info('Process complete! View data at...') # TODO: add location to view data
        else:
            logger.info('Something went wrong. Try again.')
