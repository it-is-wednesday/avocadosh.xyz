from pathlib import Path

AUTHOR = 'maror'
SITENAME = 'maror'
SITEURL = ''
THEME = "notmyidea"

PATH = 'content'

TIMEZONE = 'Asia/Jerusalem'

DEFAULT_LANG = 'en'

STATIC_PATHS = ["static"]

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'https://getpelican.com/'),
         ('Python.org', 'https://www.python.org/'),
         ('Jinja2', 'https://palletsprojects.com/p/jinja/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

PLUGIN_PATHS = [str(Path("~/.local/pelican-plugins").expanduser())]
PLUGINS = ["org_reader"]
ORG_READER_EMACS_LOCATION = "/usr/bin/emacs"
ORG_READER_EMACS_SETTINGS = Path("./emacs_settings.el").absolute()
