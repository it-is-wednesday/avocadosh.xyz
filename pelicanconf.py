import sys
import os

sys.path.append(os.curdir)

from collage import generate_collage, fetch_albums
from pathlib import Path

from pelican.generators import Generator
from pelican.writers import Writer
from pelican import signals

from dotenv import load_dotenv

load_dotenv()

LASTFM_COLLAGE_PATH = "./content/static/lastfm-collage.webp"
LASTFM_RERENDER = False

AUTHOR = "maror"
SITENAME = "maror"
SITEURL = ""
THEME = "notmyidea"

PATH = "content"

TIMEZONE = "Asia/Jerusalem"

DEFAULT_LANG = "en"

STATIC_PATHS = ["static"]

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("Pelican", "https://getpelican.com/"),
    ("Python.org", "https://www.python.org/"),
    ("Jinja2", "https://palletsprojects.com/p/jinja/"),
    ("You can modify those links in your config file", "#"),
)

# Social widget
SOCIAL = (
    ("You can add links in your config file", "#"),
    ("Another social link", "#"),
)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

PLUGIN_PATHS = [str(Path("~/.local/pelican-plugins").expanduser())]
PLUGINS = ["org_reader", "jinja2content"]
ORG_READER_EMACS_LOCATION = "/usr/bin/emacs"
ORG_READER_EMACS_SETTINGS = Path("./emacs_settings.el").absolute()

INDEX_SAVE_AS = 'posts.html'

MENUITEMS = (("Home", "/"), ("Posts", "/posts.html"))


def get_collage_generator(pelican_object):
    class CollageGenerator(Generator):
        def generate_output(self, writer: Writer):
            if not Path(LASTFM_COLLAGE_PATH).exists():
                generate_collage(fetch_albums()).save(LASTFM_COLLAGE_PATH, quality=40)

    return CollageGenerator


signals.get_generators.connect(get_collage_generator)
