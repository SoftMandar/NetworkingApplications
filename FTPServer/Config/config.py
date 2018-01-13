import os
import configparser
import logging.config
import json


BASE_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class FTPServerConfig(object):


    def __init__(self, config_file="FTPServer/server_config.ini",logger_config_file="FTPServer/logger_config.json"):

        self.config_parser = configparser.ConfigParser()
        self.config_parser.read(config_file)

        if os.path.exists(logger_config_file):

                with open(logger_config_file, "rt") as cfg:
                        logging.config.dictConfig(json.load(cfg))
        else:
            logging.basicConfig(level=logging.INFO)

    def getDefaultFolder(self):
        return self.config_parser.get("ftpsrvconfig","folder")

    def getConfigPort(self):
        return int(self.config_parser.get("ftpsrvconfig","port"))

    def getDefaultHostAddress(self):
        return self.config_parser.get("ftpsrvconfig", "hostaddress")
