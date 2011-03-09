import argparse
import logging
import sys
import traceback

from compago import Option, Command, CommandError


logger = logging.getLogger(__name__)


class ApplicationError(Exception): pass


class Application(object):

    def __init__(self, name=None):
        self.name = name or sys.argv[0]
        self.options = []
        self.commands = {}
        self.plugins = []

    @property
    def parser(self):
        parser = argparse.ArgumentParser(prog=self.name, add_help=False)
        for option in self.options:
            parser.add_argument(*option.args, **option.kwargs)
        return parser

    @property
    def usage(self):
        logger.debug('Generating usage string.')
        usage = []
        usage.append(self.parser.format_help())
        if self.commands:
            pad = max([len(c) for c in self.commands]) + 2
            fmt = '  %%-%ds%%s' % pad
            usage.append('commands:\n')
            for name, cmd in self.commands.items():
                usage.append(fmt % (name, cmd.description))
            usage.append('\nType %s <command> --help for specific usage.' % self.name)
        return '\n'.join(usage)

    def add_option(self, *args, **kwargs):
        option = Option(*args, **kwargs)
        logger.debug('Adding app-level option:%s' % option)
        self.options.append(option)
        app_ns, remainder = self.parser.parse_known_args(sys.argv)
        for k,v in app_ns.__dict__.items():
            setattr(self, k, v)
        return option

    def option(self, *args, **kwargs):
        def wrap(target):
            name = target.__name__
            if name not in self.commands:
                cmd = self.add_command(target)
            else:
                cmd = self.commands[name]
            cmd.add_option(*args, **kwargs)
            return target
        return wrap

    def add_command(self, *args, **kwargs):
        if 'parent' not in kwargs:
            kwargs['parent'] = self
        cmd = Command(*args, **kwargs)
        self.commands[cmd.name] = cmd
        return cmd

    def command(self, target):
        self.add_command(target)

    def add_plugin(self, plugin):
        self.plugins.append(plugin)

    def run(self, args=None, default=None):
        logger.debug('Running application with args:%s, default:%s' % (
                args, default))

        for plugin in self.plugins:
            plugin.before_run()

        if not args:
            logger.debug('args is None, so using sys.argv')
            args = sys.argv
        args = list(args)
        if self.name in args:
            logger.debug('Removing my own name:%s from the args:%s' % (
                    self.name, args))
            args.remove(self.name)
        logger.debug('Initial args:%s' % args)

        try:
            # take the first arg that doesn't start with '-' and is not appname
            cmd = [a for a in args if not a.startswith('-') and not a == self.name][0]
            logger.debug('Found command:%s' % cmd)
        except IndexError:
            logger.debug('No command found, using default:%s' % default)
            cmd = default

        if cmd not in self.commands:
            logger.debug('Command:%s not in app.commands:%s' % (
                    cmd, self.commands))
            print self.usage
            sys.exit(0)

        logger.debug('Removing command:%s from args:%s' % (cmd, args))
        args.remove(cmd)
        app_ns, remaining_args = self.parser.parse_known_args(args)
        logger.debug('After parsing app-level options: %s' % remaining_args)
        logger.debug('app-level options are: %s' % app_ns.__dict__)

        try:
            logger.debug('Executing command:%s with args:%s' % (
                        cmd, str(args)))
            result = self.commands[cmd].run(*args)
            [p.after_run() for p in self.plugins]
            return result
        except CommandError, e:
            logger.error('Command failed: %s' % e)
            logger.error(traceback.format_exc())
            print self.usage
            print '\nERROR: %s' % e
            sys.exit(1)
