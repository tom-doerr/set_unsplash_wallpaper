#!/usr/bin/env python3
# Written with Codex.

'''
Download a wallpaper.
'''

import argparse
import base64
import datetime
import json
import os
import requests
import sys
import time
from matplotlib import image as img
from matplotlib import pyplot as plt

from pathlib import Path

# Set the configuration file.
CONFIG_FILE = os.path.join(Path.home(), '.config', 'wallpaper.json')


DEFAULT_CONFIG = {
    'url': 'https://source.unsplash.com/{query}/7680x4320',
    'query': '',
    'interval': 60 * 60 * 24,
}

# Set the default output directory.
DEFAULT_DIR = os.path.join(Path.home(), '.wallpaper')


# Get random url with 8k wallpaper that is not from unsplash.com.
def get_url_with_8k_wallpaper():
    '''
    Returns the url with 8k wallpaper that is not from unsplash.
    '''
    return 'https://source.unsplash.com/random/7680x4320'



def get_config():
    '''
    Returns the configuration.
    '''
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as config_file:
            config = json.load(config_file)
    else:
        config = DEFAULT_CONFIG

    return config

def set_config(config):
    '''
    Sets the configuration.
    '''
    with open(CONFIG_FILE, 'w') as config_file:
        json.dump(config, config_file, indent=4)

def get_wallpaper(config):
    '''
    Returns the wallpaper.
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
    }
    url = config['url'].format(query=config['query'])
    response = requests.get(url, headers=headers)


    if response.status_code == 200:
        return response.content
    else:
        return None

def write_wallpaper(config, wallpaper):
    '''
    Writes the wallpaper to the output directory.
    '''
    if not os.path.exists(DEFAULT_DIR):
        os.mkdir(DEFAULT_DIR)

    wallpaper_path = os.path.join(DEFAULT_DIR, datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f') + '.jpg')
    with open(wallpaper_path, 'wb') as wallpaper_file:
        wallpaper_file.write(wallpaper)

def main():
    '''
    Sets the wallpaper.
    '''
    # Set the default configuration.
    config = get_config()

    # Set the command line parser.
    parser = argparse.ArgumentParser(description='Sets the wallpaper.')
    parser.add_argument('--query', '-q', default=config['query'], help='the query to search for')
    args = parser.parse_args()

    # Set the configuration.
    config['query'] = args.query
    set_config(config)

    # Download the wallpaper.
    wallpaper = get_wallpaper(config)
    while wallpaper is None:
        time.sleep(1)
        wallpaper = get_wallpaper(config)

    # Write the wallpaper.
    write_wallpaper(config, wallpaper)

    # Get the newest file in the DEFAULT_DIR directory.
    newest_file = sorted(os.listdir(DEFAULT_DIR))[-1]

    # Set the wallpaper.
    os.system('feh --bg-fill --no-xinerama ' + os.path.join(DEFAULT_DIR, newest_file))

    # Load the wallpaper image using matplotlib.
    image = plt.imread(os.path.join(DEFAULT_DIR, newest_file))


if __name__ == '__main__':
    main()

