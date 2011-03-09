import logging
logger = logging.getLogger(__name__)


class Option(object):
    '''One "option" to be passed into an ArgumentParser.'''

    def __init__(self, *args, **kwargs):
        logger.debug('Instantiating new Option with args:%s, kwargs:%s' % (
                str(args), str(kwargs)))
        self.args = args
        self.kwargs = kwargs
        if 'dest' in kwargs:
            logger.debug('Found "dest" in kwargs: %s' % kwargs['dest'])
            self.dest = kwargs['dest']
        else:
            logger.debug('Key "dest" not found in kwargs:%s' % str(kwargs))
            try:
                self.dest = [a for a in args if not a.startswith('-')][0]
            except IndexError:
                try:
                    self.dest = [a.strip('--') for a in args if a.startswith('--')][0]
                except IndexError:
                    self.dest = [a.strip('-') for a in args if a.startswith('-')][0]
            logger.debug('Inferred dest:%s' % self.dest)

    def __repr__(self):
        args = ', '.join([repr(a) for a in self.args])
        kwargs = ', '.join(['%s=%s' % (k,repr(v)) for k,v in self.kwargs.items()])
        if args:
            if kwargs:
                val = ', '.join((args, kwargs))
            else:
                val = args
        elif kwargs:
            val = kwargs
        else:
            val = ''
        return u"Option(%s)" % (val)
