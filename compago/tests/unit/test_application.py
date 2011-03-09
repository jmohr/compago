from nose.tools import raises

from compago import Application

class TestApplication(object):

    def test_creation(self):
        app = Application()
        assert 'nosetests' in app.name, 'nosetests not in %s' % app.name
        app = Application('foobar')
        assert 'foobar' in app.name, 'foobar not in %s' % app.name

    def test_parser(self):
        app = Application()
        assert app.parser
        assert app.parser.prog == app.name

    def test_usage(self):
        app = Application('foobarapp')
        assert 'foobarapp' in app.usage
        assert '-h' in app.usage

    def test_add_option(self):
        app = Application()
        app.add_option('afoobar')
        assert 'afoobar' in app.usage
        app.add_option('-b', '--bfoobar', dest='bfb')
        assert '-b' in app.usage
        assert '--bfoobar BFB' in app.usage

    @raises(SystemExit)
    def test_run(self):
        app = Application()
        args = ['-h']
        res = app.run(args=args)

    def test_add_command(self):
        app = Application()
        def target(one, two='foo'):
            return 'target called: %s %s' % (one, two)
        app.add_command(target=target)
        res = app.run(args=['target', 'ooonnneee', '--two', 'tttwwwooo'])
        assert 'target called: ooonnneee tttwwwooo' in res

    def test_command_decorator(self):
        app = Application('myapp')
        @app.command
        def target():
            return 'you have masterfully hit the target, old chap'
        app.run(args=['target'])
