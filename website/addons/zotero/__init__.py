from . import model
from . import routes

MODELS = [
    model.ZoteroUserSettings,
    model.ZoteroNodeSettings,
]


USER_SETTINGS_MODEL = model.ZoteroUserSettings
NODE_SETTINGS_MODEL = model.ZoteroNodeSettings

ROUTES = [routes.api_routes]

SHORT_NAME = 'zotero'
FULL_NAME = 'Zotero'

OWNERS = ['user', 'node']

ADDED_DEFAULT = []
ADDED_MANDATORY = []

VIEWS = ['widget']
CONFIGS = ['user', 'node']

CATEGORIES = ['citations']

INCLUDE_JS = {}

INCLUDE_CSS = {
    'widget': [],
    'page': [],
    'files': []
}

WIDGET_HELP = 'Zotero'

HAS_HGRID_FILES = False

# HERE = os.path.dirname(os.path.abspath(__file__))
NODE_SETTINGS_TEMPLATE = None  # use default node settings template
USER_SETTINGS_TEMPLATE = None  # use default user settings template
