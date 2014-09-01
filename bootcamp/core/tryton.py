__author__ = 'oussama'

from django.conf import settings
import sys, os
import warnings
warnings.filterwarnings("ignore", message="Old style callback, usecb_func(ok, store) instead")

TRYTOND_PATH = settings.TRYTOND_PATH

DIR = os.path.abspath(os.path.normpath(os.path.join(TRYTOND_PATH,'trytond')))
if os.path.isdir(DIR):
    sys.path.insert(0, os.path.dirname(DIR))

from trytond.modules import register_classes
from trytond.pool import Pool
from trytond.backend import Database
from trytond.tools import Cache

# Register classes populates the pool of models:
register_classes()

# Instantiate the database and the pool
DB = Database(settings.TRYTON_DB).connect()
POOL = Pool(settings.TRYTON_DB)
POOL.init()
user_obj = POOL.get('res.user')
cursor = DB.cursor()
Cache.clean(settings.TRYTON_DB)
try:
    # User 0 is root user. We use it to get the user id:
    USER = user_obj.search(cursor, 0, [
            ('login', '=', settings.TRYTON_UN),
            ], limit=1)[0]
finally:
    cursor.close()
    Cache.resets(settings.TRYTON_DB)