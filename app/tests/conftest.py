import pytest
import platform
import asyncio as io
import pathlib as plib

from .support.models import create_user
from ..utils.db_connect import db_connector, drop_schema
from ..utils.commons import get_attribute_values
from ..settings import DB_CONFIGS, APP_NAME
from .. import models

@pytest.fixture(scope='session')
def event_loop():
    if platform.system() == 'Windows':
        # As pytest with asyncio throws occasional RuntimeError('Event loop is closed') on Windows oses,
        # I'm setting windows loop event policy to avoid this issue.
        # It happens when working with sockets and streams
        io.set_event_loop_policy(io.WindowsSelectorEventLoopPolicy())
    loop = io.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope='session', autouse=True)
def configure_db():
    drop_schema(**DB_CONFIGS['test'])
    conn = db_connector('test')
    yield conn
    conn.close()
    
def make_dir(base_path: plib.Path, sub_dir: str):
    new_path = base_path / sub_dir
    new_path.mkdir()
    return new_path
    
@pytest.fixture(scope='module')
def prog_path(tmp_path_factory, mocker):
    prog = tmp_path_factory.mktemp(f'AppData/{APP_NAME}')
    mocker.path('app.utils.working_dirs.WorkingDirs.app_data', return_value=prog)
    return prog

@pytest.fixture(scope='module')
def assets_path(prog_path):
    return make_dir(prog_path, 'assets')

@pytest.fixture(scope='module')
def images_path(assets_path):
    return make_dir(assets_path, 'images')

@pytest.fixture(scope='module')
def avatars_path(images_path):
    return make_dir(images_path, 'avatars')

@pytest.fixture(scope='class', autouse=True)
def purge_db():
    yield
    for cls in get_attribute_values(models, exceptions=('_Model', 'Activity', 'ActivityLog')):
        cls.delete().execute()

@pytest.fixture(scope='class')
def user(request):
    _user = create_user()
    request.cls.user = _user
    yield _user
    _user.delete_instance()
