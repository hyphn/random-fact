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

# CLASS FOR SETTINGS

class JSONFile:
    def __init__(self, filename: str, interval:int = 900, loop=None):
        self.filename = filename
        self.interval = interval
        self._reload()
        loop = loop or asyncio.get_event_loop()
        loop.create_task(self._task)
            
    def _reload(self):
        with open(self.filename) as f:
            self.cache = json.load(f)
            
    async def _task(self):
        await asyncio.sleep(900)
        self._reload()
    
    def __getitem__(self, i):
        return self.cache[i]

# ###########################

# APP
app = Kyoukai(__name__)

SETTINGS = JSONFile("settings.json", loop=app.loop)

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


# Route listing
@app.route("/api/v1/endpoints")
async def endpoints(ctx):
    return Response(json.dumps(list(SETTINGS['facts'])), 200,
                    content_type="application/json")

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
