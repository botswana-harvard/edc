

class StringHelper(object):

    def get_random_string(self, length=12, allowed_chars=None):
        import random
        allowed_chars = (allowed_chars or
                         'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRTUVWXYZ012346789!@#%^&*()?<>.,[]{}')
        return ''.join([random.choice(allowed_chars) for _ in range(length)])

    def get_safe_random_string(self, length):
        """ safe for people, no lowercase and no 0OL1J5S etc."""
        allowed_chars = 'ABCDEFGHKMNPRTUVWXYZ2346789'
        return self.get_random_string(length, allowed_chars=allowed_chars)
