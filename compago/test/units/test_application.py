import sys

from nose.tools import raises

from compago import Application, Command, Option
from compago.command import InvalidCommand

def target():
    return 'target hit'


class BasicCommand(Command):
    def run(self):
        return 'basic_command hit'


class CommandWithArgs(Command):
    options = (
        Option('name')
    )
    def run(self):
        return 'command_with_args hit'


class CommandWithOpts(Command):
    options = (
        Option('-n', '--name', help='name_help', dest='name'),
        Option('-v', '--verbose', help='verbose_help',
               dest='verbose', action='store_true'),
    )
    def run(self):
        return 'command_with_opts hit'


class CommandWithDynamicOpts(Command):

    def __init__(self, default_name='Dynamo'):
        self.default_name = default_name

    def get_options(self):
        return (
            Option('-d', '--default', help='default_help',
                   dest='default', default=self.default_name),
        )
    def run(self, name):
        return 'command_with_dynamic_opts hit with %s' % name


class CommandWithCatchAll(Command):
    capture_all_args = True

    def get_options(self):
        return (Option('--test', dest='test', action='store_true'),)
    def run(self, remaining_args, test):
        return 'command_with_catch_all hit with %s' % remaining_args


class ComplexCommand(Command):
    options = (
        Option('apos'),
        Option('bpos'),
        Option('-c', '--cpos', help='cpos_help', dest='cpos'),
        Option('-d', '--dpos', help='dpos_help', dest='dpos'),
    )
    def run(self, *args, **kwargs):
        return 'complex_command hit with %s' % str(args)


class TestApplication(object):

    def test_application_name(self):
        app = Application('test_name')
        assert app.name == 'test_name'

    def test_application_usage(self):
        app = Application(usage='test_usage')
        assert app.usage == 'test_usage'
        app = Application(name='test_name')
        assert 'test_name' in app.usage

    def test_add_command(self):
        app = Application()
        command = Command(target=target)
        app.add_command(command)
        assert 'target' in app.commands
        assert len(app.commands.keys()) == 1
        assert app.commands['target'].target == target
        res = app.handle('target')
        assert 'target hit' in res

    def test_command_decorator(self):
        app = Application()
        @app.command
        def example():
            return 'example hit'
        assert 'example' in app.commands
        res = app.handle('example')
        assert 'example hit' in res

    def test_command_decorator_with_positional(self):
        app = Application()
        @app.command
        def example(positional):
            return 'example hit with arg: %s' % positional
        res = app.handle('example', ['testarg'])
        assert 'testarg' in res

    def test_option_decorator(self):
        app = Application()

        #@app.option('name')
        #def example(name):
        #    return 'example hit with %s' % name
        #res = app.handle('example', ['testname'])
        #assert 'testname' in res

        #@app.option('-t', '--test', dest='test')
        #def ex2(test):
        #    return 'ex2 hit with %s' % test
        #res = app.handle('ex2', ['testtest'])
        #assert 'testtest' in res