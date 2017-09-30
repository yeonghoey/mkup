import os


ORG_EXTENSIONS = ('.org', '.org_archive')

IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif')


def ensure_path(path):
    if path.endswith(os.sep):
        basedir = path
    else:
        basedir, _ = os.path.split(path)
    try:
        os.makedirs(basedir)
    except OSError:
        if not os.path.isdir(basedir):
            raise
