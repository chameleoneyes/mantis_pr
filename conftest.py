import json
import pytest
from Fixture.application import Application
#from Fixture.db import DBfixture
import os.path
import importlib
import ftputil
import jsonpickle


fixture = None
target = None


def load_config(file):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as cf:
            target = json.load(cf)
    return target


@pytest.fixture
def app(request, config):
    global fixture
    browser = request.config.getoption("--browser")
    # web_config = load_config(request.config.getoption("--target"))['web']
    if fixture is None or not fixture.is_valid():
        #fixture = Application(browser=browser, url=config['web']["testUrl"])
        fixture = Application(browser=browser, config=config)
    fixture.session.ensure_login(pwd=config["webadmin"]["password"], login=config["webadmin"]["username"])
    return fixture


@pytest.fixture(scope='session')
def config(request):
    return load_config(request.config.getoption("--target"))

'''
@pytest.fixture(scope='session', autouse=True)
def configure_server(request, config):
    install_server_config(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])

    def fin():
        restore_server_config(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    request.addfinalizer(fin)
'''

def install_server_config(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile('config_inc_back.php'):
            remote.remove('config_inc_back.php')
        if remote.path.isfile('config_inc.php'):
            remote.rename('config_inc.php', 'config_inc_back.php')
        remote.upload(os.path.join(os.path.dirname(__file__), 'resources/config_inc.php'), 'config_inc.php')


def restore_server_config(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile('config_inc_back.php'):
            if remote.path.isfile('config_inc.php'):
                remote.remove('config_inc.php')
            remote.rename('config_inc_back.php', 'config_inc.php')


@pytest.fixture(scope='session', autouse=True)
def stop(request):
    def f_exit():
        fixture.clear_fixture()
    request.addfinalizer(f_exit)
    return fixture


@pytest.fixture
def check_ui(request):
    return request.config.getoption("--check_ui")


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--target", action="store", default="target.json")
    parser.addoption("--check_ui", action="store_true")


def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith("data_"):
            tdata = load_from_module(fixture[5:])
            metafunc.parametrize(fixture, tdata, ids=[str(x) for x in tdata])
        elif fixture.startswith("json_"):
            tdata = load_from_json(fixture[5:])
            metafunc.parametrize(fixture, tdata, ids=[str(x) for x in tdata])


def load_from_module(module):
    return importlib.import_module("data.%s" % module).tdata


def load_from_json(file):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/%s.json" % file)) as f:
        return jsonpickle.decode(f.read())
