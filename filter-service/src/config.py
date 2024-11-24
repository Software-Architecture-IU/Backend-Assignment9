import json
import logging
import os
import sys
from pathlib import Path

LOGGING_LEVELS = {'DEBUG': logging.DEBUG, 'INFO': logging.INFO, 'WARNING': logging.WARNING, 'ERROR': logging.ERROR,
                  'CRITICAL': logging.CRITICAL}


def load_config(config_path: str | Path) -> dict:
    """ Load configuration file """
    try:
        config = {}
        config_file = json.loads(Path(config_path).read_text('utf-8'))
        app_env = os.environ.get('APP_ENVIRONMENT')
        if app_env is None:
            app_env = 'local'

        config.update(config_file[app_env])
        config.update(config_file['logging'])
        config['stop_words'] = config_file['stop_words']

        logging_level = config['logging_level']
        if logging_level not in LOGGING_LEVELS.keys():
            raise KeyError(f'Incorrect logging level provided: {logging_level}')

        config['rabbitmq']['user'] = os.environ.get('RABBITMQ_USER')
        config['rabbitmq']['password'] = os.environ.get('RABBITMQ_PASSWORD')
    except KeyError as e:
        sys.exit(f'Incorrect configuration file: {e}')

    return config


def configure_logging(config: dict) -> None:
    """ Configure logger according to the config.json file """
    level = config['logging_level']
    format = config['logging_format']

    logging.basicConfig(level=LOGGING_LEVELS[level], format=format)


config = load_config('config.json')
configure_logging(config)
