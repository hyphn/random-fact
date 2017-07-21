"""

RANDOM FACT SITE.

:copyright: (c) 2017 Jakeoid.
:license: MIT, see LICENSE.md for details.

"""

# HOUSEKEEPING
import json

# RANDOM
from random import choice

# KYOUKAI
from kyoukai import Kyoukai, util
from werkzeug import Response

# ############################

# APP
app = Kyoukai(__name__)

with open('settings.json') as settingsfile:
    SETTINGS = json.load(settingsfile)

# SERVER
IP = SETTINGS['server']['ip'] or "0.0.0.0"
PORT = SETTINGS['server']['port'] or 8080

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

    if name in SETTINGS['facts']:
        resp = {"status": 200, "string": choice(SETTINGS['facts'][name])}
        status = 200

    else:
        resp = {"status": 400, "error": "That is not a valid category."}
        status = 400

    return Response(json.dumps(resp), status, content_type="application/json")


# ############################

# Run our App.
app.run(IP, PORT)
