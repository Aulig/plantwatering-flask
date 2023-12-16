import json
import logging
from collections import OrderedDict
from datetime import datetime
from logging.handlers import RotatingFileHandler

from structlog import wrap_logger
from structlog.processors import JSONRenderer

from app import app

app.logger.setLevel(logging.DEBUG)

def add_fields(_, level, event_dict):
    """ Add custom fields to each record. """
    event_dict['timestamp'] = datetime.utcnow().isoformat()
    event_dict['level'] = level

    return event_dict


def sorted_json_dumps(input, **kwargs):
    """
    calls json.dumps but sorts the keys in the output to our desires
    :return: JSON string
    """

    main_message = input.pop("event")

    # we want the main log message to be first so it doesn't get truncated in sentry
    ordered_dict = OrderedDict([("event", main_message), *input.items()])

    return json.dumps(ordered_dict, **kwargs)


# Add a handler to write log messages to a file
if app.config.get("LOG_FILENAME"):
    import pathlib

    log_path = pathlib.Path(__file__).parent.absolute().joinpath(app.config["LOG_FILENAME"])

    # doesnt actually rotate because the intended use case is broken on windows.
    # just writes infinitely to the same log file (even after the set 50mb limit)
    file_handler = RotatingFileHandler(filename=log_path,
                                       maxBytes=1024 * 1024 * 50,
                                       mode="a",
                                       encoding="utf-8")

    file_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)

# Wrap the application logger with structlog to format the output
logger = wrap_logger(
    app.logger,
    processors=[
        add_fields,
        JSONRenderer(serializer=sorted_json_dumps)
    ]
)
