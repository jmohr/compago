import argparse
import inspect
import logging

from compago import Option


logger = logging.getLogger(__name__)

class CommandError(Exception): pass


class Command(object):

    def __init__(self, target, parent=None):
        self.target = target
        self.name = target.__name__
        if parent:
            self.prog = '%s %s' % (parent.name, target.__name__)
            self.parents = [parent.parser]
        else:
            self.prog = target.__name__
            self.parents = []
        self.description = target.__doc__ or ''
        self.options = []

    def run(self, *args):
        self.options += self.default_options()
        cmd_ns = self.parser.parse_args(args)
        logger.debug('Parsed command namespace: %s' % cmd_ns.__dict__)
        kwargs = {}
        for k, v in cmd_ns.__dict__.items():
            if k in self.args:
                kwargs[k] = v
        try:
            logger.debug('Running target:%s' % self.target)
            return self.target(**kwargs)
        except TypeError, e:
            raise CommandError('Invalid command args: %s' % e)

    def default_options(self):
        options = []
        logger.debug('self.args:%s' % str(self.args))
        logger.debug('self.kwargs:%s' % str(self.kwargs))
        for arg in self.args:
            if arg in self.kwargs:
                default = self.kwargs[arg]
                if isinstance(default, bool):
                    if default:
                        action = 'store_false'
                    else:
                        action = 'store_true'
                else:
                    action = 'store'
                option = Option('-%s' % arg[0], '--%s' % arg,
                                action=action, dest=arg,
                                required=False, default=default)
            else:
                option = Option(arg, type=unicode)
            if not option.dest in [o.dest for o in self.options]:
                logger.debug('Option:%s not already found in options:%s' % (
                        option, self.options))
                options.append(option)
            else:
                logger.debug('Option:%s already in options:%s' % (
                        option, self.options))
        return options

    def add_option(self, *args, **kwargs):
        option = Option(*args, **kwargs)
        logger.debug('Adding option:%s' % option)
        self.options.append(option)

    @property
    def parser(self):
        parser = argparse.ArgumentParser(prog=self.prog,
                    description=self.description, parents=self.parents)
        for option in self.options:
            logger.debug('Adding argument:%s to parser.' % option)
            parser.add_argument(*option.args, **option.kwargs)
        return parser

    @property
    def usage(self):
        return self.parser.format_help()

    @property
    def args(self):
        args, varargs, keywords, defaults = inspect.getargspec(self.target)
        return args

    @property
    def kwargs(self):
        args, varargs, keywords, defaults = inspect.getargspec(self.target)
        kwargs = dict(zip(*[reversed(l) for l in (args, defaults or [])]))
        return kwargs
