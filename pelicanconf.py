import sys
import os

sys.path.append(os.curdir)

from collage import generate_collage, fetch_albums, generate_test_collage
from pathlib import Path

from pelican.generators import Generator
from pelican.writers import Writer
from pelican import Pelican, signals

from dotenv import load_dotenv

import subprocess

from pandoc_cv import cv

load_dotenv()

LASTFM_MOCK = True

CV_RERENDER = False

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
    ("L*nkedIn", "https://www.linkedin.com/in/ma-or/"),
    ("GitHub", "https://github.com/it-is-wednesday/"),
    ("Last.fm", "https://www.last.fm/user/jpegaga"),
    ("Instagram", "https://www.instagram.com/maror.pashosh/"),
    ("OpenDota", "https://www.opendota.com/players/118991125"),
)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

PLUGIN_PATHS = [str(Path("~/.local/pelican-plugins").expanduser())]
PLUGINS = ["org_reader", "jinja2content"]
ORG_READER_EMACS_LOCATION = "/usr/bin/emacs"
ORG_READER_EMACS_SETTINGS = Path("./emacs_settings.el").absolute()

INDEX_SAVE_AS = "posts.html"

MENUITEMS = (("Home", "/"), ("Posts", "/posts.html"), ("CV", "/Maor Kadosh CV.pdf"))


def get_cv_generator(pelican_object: Pelican):
    class CvGenerator(Generator):
        def generate_output(self, writer: Writer):
            input_file = Path("./pandoc_cv/Maor Kadosh CV.org")

            any_missing = not cv.already_generated(input_file.stem, writer.output_path)
            if pelican_object.settings["CV_RERENDER"] or any_missing:
                cv.generate_all(
                    input_file,
                    Path(writer.output_path),
                    Path("./pandoc_cv/styles"),
                )

    return CvGenerator


def get_collage_generator(pelican_object: Pelican):
    class CollageGenerator(Generator):
        def generate_output(self, writer: Writer):
            dest = Path(writer.output_path).joinpath("theme/lastfm-collage.webp")
            img = (
                generate_test_collage()
                if pelican_object.settings["LASTFM_MOCK"]
                else generate_collage(fetch_albums())
            )
            img.save(dest.absolute(), quality=40)

    return CollageGenerator


signals.get_generators.connect(get_cv_generator)
signals.get_generators.connect(get_collage_generator)
