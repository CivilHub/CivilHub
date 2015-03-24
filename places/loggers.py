import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
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
        },
    },
    'loggers': {
        'django': {
            'handlers': ['main'],
            'level': 'DEBUG',
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
        }
    },
}
