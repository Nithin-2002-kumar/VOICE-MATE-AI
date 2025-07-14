import logging

def log_action(action, status="INFO"):
    if status == "ERROR":
        logging.error(action)
    else:
        logging.info(action)
