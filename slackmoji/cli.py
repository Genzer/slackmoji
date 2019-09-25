import click
import logging
from dotenv import load_dotenv
from pathlib import Path
import requests

from slackmoji.emojis import fetch_emojis, add_emoji

LOG = logging.getLogger(__name__)

@click.group(no_args_is_help=True)
@click.option("--debug", is_flag=True, default=False)
def main(debug: bool):
    
    logging.basicConfig(**__logging_config())
    load_dotenv()

    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

def __logging_config():
    return {
        'level': logging.INFO,
        'format': '%(asctime)s %(levelname)s %(name)s %(funcName)s \n %(message)s'
    }


@main.command(name = 'backup')
@click.argument('output_directory', type=click.Path(exists=True))
def backup(output_directory):

    emojis = fetch_emojis()

    skipped = 0
    output_path = Path(output_directory)
    for name, file_name, url in emojis:
        emoji_file: Path = output_path / file_name
        if emoji_file.exists():
            skipped += 1
            continue

        with open(emoji_file, 'wb') as emoji_file:
            LOG.debug(f"Fetch {url}")
            r = requests.get(url)
            emoji_file.write(r.content)
            LOG.info(f"Backed up emoji {name} as {file_name} in {output_path}")

    if skipped > 0:
        LOG.info(f"Skip {skipped} emojis since they are existing.")

@main.command()
@click.argument('input_directory', type=click.Path(exists=True))
def upload(input_directory: Path):

    emojis = fetch_emojis()
    remote_emoji_names = set(e.file_name for e in emojis)
    input_path = Path(input_directory)

    local_emojis = (file for file in input_path.iterdir() if file.is_file())

    for file in local_emojis:
        if file.name in remote_emoji_names:
            LOG.debug(f"Emoji {file.name} is already existing. Skip uploading!")
        else:
            add_emoji(file)

if __name__ == "__main__":
    main()