from web_app import __version__, web_app


def test_version():
    assert __version__ == "0.1.0"


def test():
    output = web_app.test()
    assert isinstance(output, str)
