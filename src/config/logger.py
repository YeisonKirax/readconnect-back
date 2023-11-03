import json
import logging

from pythonjsonlogger import jsonlogger

from config.environment import env_data, Env


class JsonFormatter(logging.Formatter):
    def __init__(self):
        super(JsonFormatter, self).__init__()

    def format(self, record):
        json_record = {"message": record.getMessage()}
        return json.dumps(json_record)


def set_up_json_logger():
    console_handler = logging.StreamHandler()
    format_str = "%(asctime)s %(levelname)s %(message)s"
    formatter = jsonlogger.JsonFormatter(format_str, json_ensure_ascii=True)
    console_handler.setFormatter(formatter)
    extra_props = {
        "app_name": "FASTAPI",
        "process_type": "API",
        "context": __name__,
    }

    logging.basicConfig(
        level=logging.INFO if env_data.ENV == Env.Production else logging.DEBUG,
        format=format_str,
        datefmt="%m/%d/%Y %H:%M",
        handlers=[console_handler],
    )


def set_up_json_logger_2():
    logger = logging.root
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    logger.handlers = [handler]
