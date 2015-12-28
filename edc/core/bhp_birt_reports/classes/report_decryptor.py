from edc_base.encrypted_fields import Cryptor
from edc_base.encrypted_fields import Crypt


class ReportDecryptor(Cryptor):

    def __init__(self):
        self.algorithm = 'rsa'
        self.mode = 'local'

    def decrypt(self, line, **kwargs):
        line = line.replace('<div>enc1:::', '')
        line = line.replace('</div>', '')
        line = line.strip()
        secret = Crypt.objects.filter(hash=line)
        decrypted = self.rsa_decrypt(secret[0].secret)
        return '<div>' + decrypted + '</div>'
