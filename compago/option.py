import logging
logger = logging.getLogger(__name__)


class Option(object):
    """One "option" to be passed into an ArgumentParser."""

    def __init__(self, *args, **kwargs):
        logger.debug('Instantiating new Option with args:%s, kwargs:%s' % (
                str(args), str(kwargs)))
        self.args = args
        self.kwargs = kwargs
        self._destination = None

    @property
    def destination(self):
        if not self._destination:
            if 'dest' in self.kwargs:
                logger.debug('Found "dest" in kwargs: %s' % self.kwargs['dest'])
                self._destination = self.kwargs['dest']
            else:
                logger.debug('Key "dest" not found in kwargs:%s' % str(self.kwargs))
                try:
                    self._destination = [a for a in self.args if isinstance(a, str) and not a.startswith('-')][0]
                except IndexError:
                    try:
                        self._destination = [a.strip('--') for a in self.args if a.startswith('--')][0]
                    except IndexError:
                        self._destination = [a.strip('-') for a in self.args if a.startswith('-')][0]
        return self._destination

    def __repr__(self):
        args = ', '.join([repr(a) for a in self.args])
        kwargs = ', '.join(['%s=%s' % (k, repr(v))
                            for k, v in self.kwargs.items()])
        if args:
            if kwargs:
                val = ', '.join((args, kwargs))
            else:
                val = args
        elif kwargs:
            val = kwargs
        else:
            val = ''
        return "Option({})".format(val)
