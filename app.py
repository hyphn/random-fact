"""

RANDOM FACT SITE.

:copyright: (c) 2017 Jakeoid.
:license: MIT, see LICENSE.md for details.

"""

# KYOUKAI
from kyoukai import Kyoukai
from kyoukai import util

# RANDOM
from random import choice

# HOUSEKEEPING
import json

# ############################

# APP
app = Kyoukai(__name__)

# SETTINGS
settings = None

with open('settings.json') as settingsfile:
    settings = json.load(settingsfile)

# SERVER
ip = settings['server']['ip']
port = settings['server']['port']

# ############################


# Site Index.
@app.route("/")
async def index(ctx):
    """The overall homepage/index of the website."""
    file_directory = 'templates/index.html'

    with open(file_directory) as file:
        content = file.read()
        return util.as_html(content)


# Categories.
@app.route("/api/v1/<name>")
async def endpoint(ctx, name):
    """The endpoint used in order to gather the facts about the categories."""

    header = {
        'Content-Type': 'application/json'
    }

    try:
        return util.Response({"status": 200, "string": choice(settings['facts'][name])}, status=200, headers=header)
    except:
        return util.Response({"status": 404, "error": "That is not a valid category."}, status=200, headers=header)


# ############################

# Run our App.
app.run(ip=ip, port=port)
