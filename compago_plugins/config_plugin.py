from UserDict import DictMixin
import os
import yaml
from compago.plugin import Plugin


class Config(DictMixin):

    @staticmethod
    def load(path):
        try:
            attrs = yaml.load(open(path))
        except IOError:
            return Config()
        else:
            return Config(**attrs)

    def __init__(self, **kwargs):
        self.attributes = kwargs or {}

    def __getitem__(self, key):
        try:
            return self.attributes[key]
        except KeyError:
            raise Exception('{0} is not configured.'.format(key))

    def keys(self):
        return self.attributes.keys()


class ConfigPlugin(Plugin):

    def __init__(self, path=None):
        self.path = path

    def after_application_init(self, application):
        application.add_option('--configfile', dest='cfpath',
                               metavar='PATH',
                               help='The path to the config file.')
        if application.args['cfpath']:
            if not os.path.exists(application.args['cfpath']):
                raise IOError('Config file {0} does not exist!'.format(
                    application.args['cfpath']))
            self.path = application.args['cfpath']
        if not self.path:
            self.path = '{0}.conf'.format(application.name)
        application.config = Config.load(self.path)
