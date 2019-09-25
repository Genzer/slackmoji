import os
import logging

LOG = logging.getLogger(__name__)

def get_token():
    return os.getenv('SLACK_API_TOKEN')
