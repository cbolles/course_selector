import configparser
from bs4 import BeautifulSoup
import urllib.request
import utils.course_objects


def get_config(config_file: str) -> dict:
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


def get_program_data(config, program_name, program_type):
    url = config['immersions']['immersions_site'] + immersion_name
    immersion_page = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(immersion_page)
    print(soup.prettify())


def test():
    config = get_config('../properties/web_details.ini')





