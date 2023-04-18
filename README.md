# Curator Bot

> A Discord bot that curates messages posted by members.

## Prerequisites

The recommended way of running the bot is via Docker. If you want to run it outside of Docker, then you need to have the following installed:

- Python 3.11
- [Poetry](https://python-poetry.org/)

## Getting started

### Preparing the Discord application

Go to https://discord.com/developers/applications and create a new Discord application. In your new application, go to Bot settings.

On the Bot settings page and perform the following steps:

- Enter a name and add a nice profile picture
- **Click on View token and store this token somewhere safe.** The Python script will make use of this token via the `DISCORD_BOT_TOKEN` environment variable.
- Enable the `Message Content Intent` under `Privileged Gateway Intents`. The bot needs this intent to read the contents of messages.

### Inviting the Discord bot to your server

Go to the `URL Generator` page under `OAuth2`. Enable the `bot` scope, and then the following permissions:

- Send Messages _(for sending messages to the #curation-gems channel)_
- Manage Messages _(for removing EMOJI_NAME reactions that were added by the authors of posts)_

Finally, visit the generated URL at the bottom of the page. If you are an administrator of a server, this will allow you to invite the bot to your server.

### Running the Python script

In the root of the project, run `poetry install`, followed by `poetry shell` to enter the Python environment.

Prepare an `.env` file in the root of the project. An example can be found in `.env.example`.

Put the bot token you saved earlier in the `DISCORD_BOT_TOKEN` variable. To get the channel IDs for `TARGET_CHANNEL_ID` and `CURATIONS_CHANNEL_ID`, simply right-click on their respective channels in Discord, and click `Copy ID`. The channel ID will now be in your clipboard, ready to be pasted.

Optionally, you can set the emoji name to be tracked in the `EMOJI_NAME` variable (defaults to "thumbsup"). You can also change the reaction threshold in `REACTION_THRESHOLD` (defaults to 5).

Once you have prepared your `.env` file, and you are in the Python environment, run `python main.py` to start the bot. If all is well, your bot should now appear online in Discord.

## Technical information

### Database

The bot makes use of a simple SQLite database to keep track of which messages have already been posted to #curation-gems, to avoid duplicates. This database is stored in the `curator.sqlite3` file by default. The path to the database file can be overridden by setting the `DATABASE_PATH` environment variable.
