

class Logic(object):

    def __init__(self, *args, **kwargs):
        if args:
            if ((isinstance(args[0], (tuple, list)) or hasattr(args[0], '__call__')) and len(args[0]) == 3):
                self.predicate, self.consequence, self.alternative = args[0]
            else:
                raise AttributeError('Attribute \'logic\' must be a tuple of (predicate, consequence, alternative) or callable')
        else:
            self.predicate = kwargs.get('predicate')
            self.consequence = kwargs.get('consequence')
            self.alternative = kwargs.get('alternative')
            self.comment = kwargs.get('comment')
