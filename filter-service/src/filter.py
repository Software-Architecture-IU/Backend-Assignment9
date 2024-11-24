import json
import re
from typing import Optional

from config import config


def filter_message(body: json) -> Optional[str]:
    message = body['message'].lower()

    stop_words = [word.lower() for word in config['stop_words']]
    regexp_stop_words = [re.compile(r'\b' + re.escape(word) + r'\b') for word in stop_words]

    for regex in regexp_stop_words:
        match = regex.search(message)
        if match:
            return match.group()

    return None
