class PluginManager(object):

    def __init__(self, application, *args):
        self.application = application
        self.plugins = list(args)

    def register(self, plugin):
        if plugin not in self.plugins:
            self.plugins.append(plugin)

    def run_hook(self, hook, *args):
        for plugin in self.plugins:
            if hook == 'after_application_init':
                plugin.after_application_init(self.application)
            elif hook == 'before_command_run':
                plugin.before_command_run(self.application, args[0])
            elif hook == 'after_command_run':
                plugin.after_command_run(self.application, args[0])
            elif hook == 'option_added':
                plugin.option_added(self.application, args[0])
            elif hook == 'command_added':
                plugin.command_added(self.application, args[0])



class Plugin(object):

    def after_application_init(self, application):
        pass

    def before_command_run(self, application, command):
        pass

    def after_command_run(self, application, command):
        pass

    def option_added(self, application, option):
        pass

    def command_added(self, application, option):
        pass
