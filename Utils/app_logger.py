import logging
logger = logging.getLogger(__name__)

@staticmethod
def app_logger(**kwargs):
    file_name = f"{kwargs.get('file_name')}.log" if kwargs.get('file_name') is not None else 'general_logs.log'