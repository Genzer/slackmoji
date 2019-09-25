import requests
import logging
import re
from collections import namedtuple

from pathlib import Path

from slackmoji import api

URL_PATTERN = re.compile('^https://.*')

LOG = logging.getLogger(__name__)

Emoji = namedtuple('Emoji', 'name file_name url')

def fetch_emojis():
    token = api.get_token()
    response = requests.get(
        'https://slack.com/api/emoji.list',
        params={
            'token': token
        })
    
    LOG.debug(f"Response from https://slack.com/api/emoji.list:\n {response}")
    emojis = response.json()['emoji']

    filtered_emojis = []

    for emoji_name, url in emojis.items():
        if URL_PATTERN.fullmatch(url):
            filtered_emojis.append(
                Emoji(
                    name=emoji_name,
                    file_name=f"{emoji_name}{Path(url).suffix}",
                    url=url))
    return filtered_emojis

def add_emoji(emoji_file: Path):
    token = api.get_token()

    file_extension = emoji_file.suffix
    emoji_name = emoji_file.name.replace(file_extension, '')
    LOG.error(f"Uploading emoji {emoji_file}")

    # NOTE:
    # ====
    # Read https://stackoverflow.com/questions/12385179/how-to-send-a-multipart-form-data-with-requests-in-python/12385661#12385661
    # Save my life!
    file = {
        'mode': (None, 'data'),
        'name': (None, emoji_name),
        'token': (None, token),
        'image': (emoji_file.name, open(emoji_file, 'rb'), 'image/gif')
    }

    response = requests.post(
        'https://slack.com/api/emoji.add',
        files=file
    )

    LOG.debug(response.request.body)

    if response.status_code != 200 or response.json()['ok'] == False:
        raise RuntimeError(response.text)