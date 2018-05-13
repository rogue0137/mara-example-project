"""Set up Navigation, ACL & Logos"""


import data_integration
import flask
import mara_acl
import mara_acl.users
import mara_app
import mara_app.layout
import mara_db
import mara_page.acl
from mara_config.config_system import wrap, patch
from mara_page import acl
from mara_page import navigation

from app.ui import start_page

blueprint = flask.Blueprint('ui', __name__, url_prefix='/ui', static_folder='static')

MARA_FLASK_BLUEPRINTS = [start_page.blueprint, blueprint]

# replace logo and favicon
patch(mara_app.config.favicon_url)(lambda: flask.url_for('ui.static', filename='favicon.ico'))
patch(mara_app.config.logo_url)(lambda: flask.url_for('ui.static', filename='logo.png'))


# add custom css
@wrap(mara_app.layout.css_files)
def css_files(original_function, response):
    files = original_function(response)
    files.append(flask.url_for('ui.static', filename='styles.css'))
    return files


# define protected ACL resources
@patch(mara_acl.config.resources)
def acl_resources():
    def iter(iterator_or_callable):
        if callable(iterator_or_callable):
            iterator_or_callable = iterator_or_callable()
        return iterator_or_callable
    return [acl.AclResource(name='Documentation',
                            children=iter(data_integration.MARA_ACL_RESOURCES)
                                     + iter(mara_db.MARA_ACL_RESOURCES)),
            acl.AclResource(name='Admin',
                            children=iter(mara_app.MARA_ACL_RESOURCES) + iter(mara_acl.MARA_ACL_RESOURCES))]


# activate ACL
patch(mara_page.acl.current_user_email)(mara_acl.users.current_user_email)
patch(mara_page.acl.current_user_has_permission)(mara_acl.permissions.current_user_has_permission)
patch(mara_page.acl.current_user_has_permissions)(mara_acl.permissions.current_user_has_permissions)

patch(mara_acl.config.whitelisted_uris)(lambda: ['/mara-app/navigation-bar'])


# navigation bar (other navigation entries will be automatically added)
@patch(mara_app.config.navigation_root)
def navigation_root() -> navigation.NavigationEntry:
    def navigation_entries(module):
        navigation_entries = module.MARA_NAVIGATION_ENTRY_FNS
        if callable(navigation_entries):
            navigation_entries = navigation_entries()

        return [fn() for fn in navigation_entries]

    return navigation.NavigationEntry(label='Root', children=(
            navigation_entries(data_integration)
            + [navigation.NavigationEntry('Settings', icon='cog', description='ACL & Configuration', rank=100,
                                          children=navigation_entries(mara_app) + navigation_entries(mara_acl))]))
