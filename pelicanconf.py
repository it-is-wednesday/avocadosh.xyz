import os
import sys

sys.path.append(os.curdir)

import subprocess
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pelican.generators import Generator
from pelican.writers import Writer

import cv
from collage import fetch_albums, generate_collage, generate_test_collage
from pelican import Pelican, signals

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

EXTRA_PATH_METADATA = {
    "static/favicon.ico": {"path": "favicon.ico"},
}

#
MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.codehilite": {"css_class": "highlight"},
        "markdown.extensions.extra": {},
        "markdown.extensions.meta": {},
    },
    "output_format": "html5",
    "extensions": ["admonition", "codehilite"],
}
# Feed generation is usually not desired when developing
FEED_ALL_ATOM: Optional[str] = None
CATEGORY_FEED_ATOM: Optional[str] = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

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
PLUGINS = ["jinja2content"]

INDEX_SAVE_AS = "posts.html"

MENUITEMS = (("Home", "/"), ("Posts", "/posts.html"), ("CV", "/Maor Kadosh CV.pdf"))


def get_cv_generator(pelican_object: Pelican):
    class CvGenerator(Generator):
        def generate_output(self, writer: Writer):
            input_file = Path("./cv/Maor Kadosh CV.org")

            any_missing = not cv.already_generated(input_file.stem, writer.output_path)
            if pelican_object.settings["CV_RERENDER"] or any_missing:
                cv.generate_all(
                    input_file,
                    Path(writer.output_path),
                    Path("./cv/styles"),
                )

    return CvGenerator


def get_collage_generator(pelican_object: Pelican):
    class CollageGenerator(Generator):
        def generate_output(self, writer: Writer):
            dest = Path(writer.output_path).joinpath("theme/lastfm-collage.webp")
            dest.parent.mkdir(exist_ok=True)
            img = (
                generate_test_collage()
                if pelican_object.settings["LASTFM_MOCK"]
                else generate_collage(fetch_albums())
            )
            img.save(dest.absolute(), quality=40)

    return CollageGenerator


signals.get_generators.connect(get_cv_generator)
signals.get_generators.connect(get_collage_generator)
