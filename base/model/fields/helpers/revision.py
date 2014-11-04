from git import Repo, GitDB

from django.conf import settings


class Revision(object):

    def __init__(self):
        self._revision = None
        self.repo = Repo(self.source_folder, odbt=GitDB)
        self.tag = self.repo.git.describe(tags=True)
        self.branch = unicode(self.repo.active_branch)
        self.commit = unicode(self.repo.active_branch.commit)
        self.revision = '{0}:{1}'.format(self.branch, self.commit)

    @property
    def source_folder(self):
        if 'PROJECT_ROOT' not in dir(settings):
            raise AttributeError('Missing settings attribute: \'PROJECT_ROOT\' required by revision field class')
        return settings.PROJECT_ROOT

site_revision = Revision()
