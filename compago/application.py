import argparse
import inspect
import logging
import os.path
import sys

from compago.command import Command, InvalidCommand
from compago.option import Option

logger = logging.getLogger(__name__)


class Application(object):
    '''
    The Application class is the core of a Compago application. When writing
    a Compago script, a user will instantiate an Application(), and then
    use that object's @command and/or @option decorators to define one or
    more commands.

    Example:

        from compago import Application

        myapp = Application()

        @myapp.command
        def do_something():
            print "doing something..."

        @myapp.command
        def another_thing(thing):
            print "and another thing... %%s" %% thing

        if __name__ == '__main__': myapp.run()

    This is a fully functional Compago application. You can now run
    it from the command line:

        >$ python myapp.py do_something --help
        usage: myapp.py [-h]

        optional arguments:
          -h, --help  show this help message and exit
    '''

    commands = {}
    options = []

    def __init__(self, name=None, usage=None):
        '''
        @param name:    Then name of this application. Default: sys.argv[0]
        @type name:     str
        @param usage:   A usage string for this application.
        @type usage:    str
        '''
        if name:
            self.name = name
        else:
            self.name = sys.argv[0]
        if usage:
            self.usage = usage
        else:
            self.usage = '%s [options] arguments' % self.name
        logger.debug('Initializing new application with name: %s' % name)

    @property
    def parser(self):
        '''
        Returns an ArgumentParser configured with the appropriate options.
        '''
        parser = argparse.ArgumentParser()
        for option in self.options:
            parser.add_argument(*option.args, **option.kwargs)
        return parser

    def add_command(self, command):
        self.commands[command.name] = command

    def command(self, func):
        '''
        Decorator to define a function as an application command.

        @param func:    The function to decorate.
        @type func:     function
        '''
        logger.debug("Adding command %s to application %s" % (func, self))
        args, varargs, keywords, defaults = inspect.getargspec(func)
        logger.debug("Found args: %s" % args)

        defaults = defaults or []
        kwargs = dict(zip(*[reversed(l) for l in (args, defaults)]))
        logger.debug("Found kwargs: %s" % kwargs)

        options = []

        for arg in args:
            logger.debug("Parsing argument %s" % arg)
            if arg in kwargs:
                logger.debug("Argument %s is optional" % arg)
                default = kwargs[arg]
                logger.debug("Argument %s has default: %s" % (arg, default))
                if isinstance(default, bool):
                    logger.debug("Adding boolean argument")
                    action = 'store_true'
                else:
                    logger.debug("Adding regular argument")
                    action = 'store'
                options.append(Option('-%s' % arg[0],
                                      '--%s' % arg,
                                      action=action,
                                      dest=arg,
                                      required=False,
                                      default=default))
            else:
                logger.debug("Argument %s is required, has no default." % arg)
                options.append(Option(arg, type=unicode))

        command = Command(target=func)
        command.__doc__ = func.__doc__
        command.options = options

        self.commands[command.name] = command

        return func

    def option(self, *args, **kwargs):
        '''
        Decorator to explicitly define options for a command. If you use
        this decorator, there is no need to also use the @command decorator.
        '''

        option = Option(*args, **kwargs)

        def decorate(func):
            name = func.__name__
            if name not in self.commands:
                command = Command(func)
                command.__doc__ = func.__doc__ or ''
                command.options = []
                self.add_command(command)
            self.commands[name].options.append(option)
            return func

        return decorate

    def run(self, commands=None, default_command=None):
        '''
        Runs the application. Usually used in an "if __name__ == '__main__'"
        block at the end of your script. Will execute the command given by
        the user at the command line, or alternately print out help or
        usage, depending on the provided options.

        @param commands: Add commands to the application
        @type commands: list
        @param default_command: If no command is specified, run this
        @type default_command: str
        '''
        if commands:
            self.commands.update(commands)
        try:
            try:
                command = sys.argv[1]
            except IndexError:
                command = default_command
            if command is None:
                raise InvalidCommand, 'Please provide a command.'
            self.handle(command, sys.argv[2:])
            sys.exit(0)
        except Exception, e:
            print "\nERROR: %s\n" % e
            print self.get_usage()
        sys.exit(1)

    def handle(self, command_name, args=None):
        '''Executes the given command with the proper arguments.

        @param command_name:    Name of the command to run.
        @type command_name:     str
        @param args:    Additional arguments to pass to command.
        @type args:     list'''
        args = list(args or [])
        try:
            command = self.commands[command_name]
        except KeyError:
            raise InvalidCommand, 'Command %s not found' % command_name
        help_args = ('-h', '--help')

        app_args = [arg for arg in args if arg not in help_args]

        app_namespace, remaining_args = self.parser.parse_known_args(app_args)

        for arg in help_args:
            if arg in args:
                remaining_args.append(arg)
        logger.debug('Including help, remaining_args is: %s' % remaining_args)

        if getattr(command, 'capture_all_args', False):
            logger.debug('Catch-all enabled for command %s' % command)
            command_namespace, unparsed_args = \
                command.parser.parse_known_args(remaining_args)
            positional_args = [unparsed_args]
        else:
            logger.debug('Catch-all not enabled for command %s' % command)
            command_namespace = command.parser.parse_args(remaining_args)
            positional_args = []

        logger.debug('Got command_namespace: %s' % command_namespace)
        logger.debug('Got positional_args: %s' % positional_args)

        return command.run(*positional_args, **command_namespace.__dict__)

    def get_usage(self):
        pad = max([len(k) for k in self.commands]) + 2
        format = '  %%- %ds%%s' % pad
        result = []

        if self.usage:
            result.append('USAGE:\n')
            result.append('  %s\n' % self.usage)

        if self.commands:
            result.append('COMMANDS:\n')
            for name, command in self.commands.items():
                description = command.description or ''
                usage = format % (name, description)
                result.append(usage)
            result.append('\nType %s <command> --help for specific usage.' % self.name)

        return '\n'.join(result)
