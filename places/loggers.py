import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'main': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
        },
        'users': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'userspace.log'),
        },
        'core': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'userspace.log'),
        },
        'core_tasks': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'tasks.log'),
            'formatter': 'default',
        },
        'map_tasks': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'markers.log'),
        },
        'tracker_tasks': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'tracker.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['main'],
            'level': 'INFO',
            'propagate': True,
        },
        'userspace': {
            'handlers': ['users'],
            'level': 'INFO',
            'propagate': True,
        },
        'tokens': {
            'handlers': ['core'],
            'level': 'INFO',
            'propagate': False,
        },
        'tasks': {
            'handlers': ['core_tasks'],
            'level': 'INFO',
            'propagate': False,
        },
        'maps': {
            'handlers': ['map_tasks'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'tracker': {
            'handlers': ['tracker_tasks'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
