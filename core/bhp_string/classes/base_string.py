

class BaseString(object):

    def __init__(self):
        self.safe_allowed_chars = 'ABCDEFGHKMNPRTUVWXYZ2346789'

    def get_random_string(self, length=12, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRTUVWXYZ012346789!@#%^&*()?<>.,[]{}'):
        """ no dollar signs """
        import random
        try:
            random = random.SystemRandom()
        except NotImplementedError:
            pass
        return ''.join([random.choice(allowed_chars) for i in range(length)])

    def get_safe_random_string(self, length):
        """ safe for people, no lowercase and no 0OL1J5S etc."""
        return self.get_random_string(length, allowed_chars=self.safe_allowed_chars)
