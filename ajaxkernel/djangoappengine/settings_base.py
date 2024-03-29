# Initialize App Engine SDK if necessary
try:
    from google.appengine.api import api_proxy_stub_map
except ImportError:
    from .boot import setup_env
    setup_env()

from djangoappengine.utils import on_production_server, have_appserver

# DEBUG = not on_production_server
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ROOT_URLCONF = 'urls'

DATABASES = {
    'default': {
        'ENGINE': 'djangoappengine.db',
    },
}

if on_production_server:
    EMAIL_BACKEND = 'djangoappengine.mail.AsyncEmailBackend'
else:
    EMAIL_BACKEND = 'djangoappengine.mail.EmailBackend'

PREPARE_UPLOAD_BACKEND = 'djangoappengine.storage.prepare_upload'
SERVE_FILE_BACKEND = 'djangoappengine.storage.serve_file'
DEFAULT_FILE_STORAGE = 'djangoappengine.storage.BlobstoreStorage'
FILE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024
FILE_UPLOAD_HANDLERS = (
    'djangoappengine.storage.BlobstoreFileUploadHandler',
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
)

CACHE_BACKEND = 'memcached://?timeout=0'
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

if not on_production_server:
    INTERNAL_IPS = ('127.0.0.1',)
