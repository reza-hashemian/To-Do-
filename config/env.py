from django.core.exceptions import ImproperlyConfigured
import os

import environ

env = environ.Env()

BASE_DIR = environ.Path(__file__) - 2
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

def env_to_enum(enum_cls, value):
    for x in enum_cls:
        if x.value == value:
            return x

    raise ImproperlyConfigured(f"Env value {repr(value)} could not be found in {repr(enum_cls)}")
