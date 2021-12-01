import json
import pytest
from Fixture.application import Application
#from Fixture.db import DBfixture
import os.path
import importlib



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
def app(request):
    global fixture
    browser = request.config.getoption("--browser")
    web_config = load_config(request.config.getoption("--target"))['web']
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, url=web_config["testUrl"])
    return fixture


@pytest.fixture(scope='session', autouse=True)
def stop(request):
    def f_exit():
        fixture.clear_fixture()
    request.addfinalizer(f_exit)
    return fixture


@pytest.fixture(scope='session')
def db(request):
    db_config = load_config(request.config.getoption("--target"))['db']
    dbfixture = DBfixture(host=db_config['host'], name=db_config['name'], user=db_config['user'], pwd=db_config['password'])
    def fin():
        dbfixture.destroy()
    request.addfinalizer(fin)
    return dbfixture


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
