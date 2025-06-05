import os
import collections
if not hasattr(collections, 'Mapping'):
    import collections.abc
    collections.Mapping = collections.abc.Mapping
    collections.MutableMapping = collections.abc.MutableMapping
    collections.Sequence = collections.abc.Sequence
    collections.MutableSequence = collections.abc.MutableSequence
    collections.Set = collections.abc.Set
    collections.Callable = collections.abc.Callable # Added Callable as it's often needed too
    # For older Django versions, Iterator might also be needed from collections.abc
    if not hasattr(collections, 'Iterator'):
        collections.Iterator = collections.abc.Iterator

def pytest_configure():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'superlist.settings')
    import django
    django.setup()
