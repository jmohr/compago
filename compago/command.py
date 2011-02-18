import argparse


class InvalidCommand(Exception):
    '''Raised when an invalid/nonexistant command is attempted.'''
    pass

class Command(object):
    '''
    When a function in your script is decorated as a @command, it will
    be tied into one of these Command objects.
    '''

    options = []
    target = lambda:None

    def __init__(self, target=None):
        '''
        @param target:  The function that this command executes.
        @type  target:  function
        '''
        if target:
            self.target = target

    @property
    def name(self):
        '''Returns target.__name__ as the command's name.'''
        return self.target.__name__

    @property
    def description(self):
        '''Returns the description string for this command.'''
        description = self.__doc__ or ''
        return description.strip()

    @property
    def parser(self):
        '''Returns an ArgumentParser for this command's options.'''
        parser = argparse.ArgumentParser(description=self.description)

        for option in self.get_options():
            parser.add_argument(*option.args, **option.kwargs)

        return parser

    def get_options(self):
        return self.options

    def run(self, *args, **kwargs):
        '''
        Calls this command's target function.
        '''
        return self.target(*args, **kwargs)
