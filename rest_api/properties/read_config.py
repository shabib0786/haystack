import configparser

def get_config_urls():
    config = configparser.RawConfigParser()
    config.read('/config/chatbot.properties')
    details_dict = dict(config.items('urls'))
    return details_dict
