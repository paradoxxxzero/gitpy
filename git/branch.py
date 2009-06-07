# Copyright (c) 2009, Rotem Yaari <vmalloc@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of organization nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY Rotem Yaari ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL Rotem Yaari BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
from ref import Ref

class Branch(Ref):
    def delete(self):
        raise NotImplementedError()
    def __repr__(self):
        return "<branch %s>" % (self.name,)
class LocalBranch(Branch):
    def delete(self):
        self.repo._executeGitCommandAssertSuccess("git branch -D %s" % (self.name,))
class RemoteBranch(Branch):
    pass
class RegisteredRemoteBranch(RemoteBranch):
    def __init__(self, repo, remote, name):
        super(RegisteredRemoteBranch, self).__init__(repo, name)
        self.remote = remote
    def getHead(self):
        return self.repo._getCommitByRefName("%s/%s" % (self.remote.name, self.name))
    def delete(self):
        """
        Deletes the actual branch on the remote repository!
        """
        self.repo.push(self.remote, fromBranch="", toBranch=self, force=True)
    def getNormalizedName(self):
        return "%s/%s" % (self.remote.name, self.name)
    def __repr__(self):
        return "<branch %s on remote %r>" % (self.name, self.remote.name)
