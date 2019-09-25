# slackmoji

A simple CLI tools for bulk upload/download Slack's emojis.

## Build

```sh
# This is for preparation of the repository
python3.6 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install pybuilder

# Install all dependencies
pyb
```

## Usage

### Slack API Token

1 - Please make a copy of `.env.example` to `.env`.
2 - Please follow the link on the `.env` to obtain your Slack API token. Once you got it, please set it on the `SLACK_API_TOKEN` variable.

```sh
# For backing up the entire custom emojis
python -m slackmoji.cli backup ~/my-slack-emojis

# For bulk uploading only new emojis
python -m slackmoji.cli upload ~/my-slack-emojis
```
