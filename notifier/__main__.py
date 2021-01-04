#!/usr/bin/python

import argparse
from tools import Config
import os
import requests


REL_SETTINGS_PATH = "settings.yaml"
DEFAULT_MESSAGE = "!"


def get_settings_path() -> str:
    parent_dir_path = os.path.dirname(__file__)
    return os.path.join(parent_dir_path, REL_SETTINGS_PATH)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="A simple usage of the Telegram Bot API.",
                                         allow_abbrev=True)
    arg_parser.add_argument("--chat_id", type=str, help="sets the chat_id in settings")
    arg_parser.add_argument("--token", type=str, help="sets the bot token in settings")
    arg_parser.add_argument("--text", type=str, default=DEFAULT_MESSAGE, help="specifies the message to send to chat")
    arg_parser.add_argument("--silence_message", action="store_true", dest="silenced",
                            help=f"silences default '{DEFAULT_MESSAGE}' message to chat when no message is specified")
    arg_parser.add_argument("--suppress_save", action="store_true", help="suppresses saving entries to settings")
    args = arg_parser.parse_args()

    config = Config(get_settings_path())

    update_config_entries = {
        "chat_id": args.chat_id,
        "token": args.token
    }

    for item_key, item_value in update_config_entries.items():
        if item_value is not None:
            config.update_entries({item_key: item_value})

    if not config.validate_keys():
        raise Exception("Settings not valid. Use --token and --api_key options to set settings entries.")
    elif not args.suppress_save:
        config.save()

    if not args.silenced:
        data = {"chat_id": config.get_entry('chat_id'), "text": args.text}
        bot_url = f"https://api.telegram.org/bot{config.get_entry('token')}/sendMessage"
        response = requests.post(bot_url, data=data)
        print(response)
