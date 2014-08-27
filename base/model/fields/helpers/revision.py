from git import Repo, GitCmdObjectDB

from django.conf import settings


class Revision(object):

    def __init__(self):
        self._revision = None
        self.set_revision()

    def get_source_folder(self):
        if 'PROJECT_ROOT' not in dir(settings):
            raise AttributeError('Missing settings attribute: \'PROJECT_ROOT\' required by revision field class')
        return settings.PROJECT_ROOT

    def set_revision(self):
        repo = Repo(self.get_source_folder(), odbt=GitCmdObjectDB)
        try:
            branch = unicode(repo.active_branch)
        except:
            branch = 'branch'
        try:
            commit = unicode(repo.active_branch.commit)
        except:
            commit = 'commit'
        self._revision = '{0}:{1}'.format(branch, commit)

    def get_revision(self):
        return self._revision

site_revision = Revision()
