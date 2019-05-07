
# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

"""
Cookiecutter-Git Post Project Generation Hook Module.
"""
import base64
from contextlib import contextmanager
import errno
import getpass
import json
import os
import re
import shutil
import subprocess

if os.name == "nt":

    def quote(arg):
        # https://stackoverflow.com/a/29215357
        if re.search(r'(["\s])', arg):
            arg = '"' + arg.replace('"', r"\"") + '"'
        meta_chars = '()%!^"<>&|'
        meta_re = re.compile(
            "(" + "|".join(re.escape(char) for char in list(meta_chars)) + ")"
        )
        meta_map = {char: "^%s" % char for char in meta_chars}

        def escape_meta_chars(m):
            char = m.group(1)
            return meta_map[char]

        return meta_re.sub(escape_meta_chars, arg)


else:
    try:  # py34, py35, py36, py37
        from shlex import quote
    except ImportError:  # py27
        from pipes import quote

from invoke import Result, run, UnexpectedExit
import requests


class MockResult(Result):
    mock_stdout = {
        "github.com": """Password for 'https://NathanUrwin@github.com':
Counting objects: 18, done.
Delta compression using up to 8 threads.
Compressing objects: 100% (15/15), done.
Writing objects: 100% (18/18), 6.24 KiB | 0 bytes/s, done.
Total 18 (delta 0), reused 0 (delta 0)
To https://github.com/NathanUrwin/cookiecutter-git-demo.git
* [new branch]      master -> master
Branch master set up to track remote branch master from origin.""",
        "gitlab.com": """Password for 'https://NathanUrwin@gitlab.com':
Counting objects: 13, done.
Delta compression using up to 8 threads.
Compressing objects: 100% (10/10), done.
Writing objects: 100% (13/13), 5.25 KiB | 0 bytes/s, done.
Total 13 (delta 0), reused 0 (delta 0)
remote:
remote: The private project NathanUrwin/cookiecutter-git-demo was successfully created.
remote:
remote: To configure the remote, run:
remote:   git remote add origin https://gitlab.com/NathanUrwin/cookiecutter-git-demo.git
remote:
remote: To view the project, visit:
remote:   https://gitlab.com/NathanUrwin/cookiecutter-git-demo
remote:
To https://gitlab.com/NathanUrwin/cookiecutter-git-demo.git
* [new branch]      master -> master
Branch master set up to track remote branch master from origin.""",
        "bitbucket.org": """Password for 'https://NathanUrwin@bitbucket.org':
Counting objects: 13, done.
Delta compression using up to 8 threads.
Compressing objects: 100% (10/10), done.
Writing objects: 100% (13/13), 5.26 KiB | 0 bytes/s, done.
Total 13 (delta 0), reused 0 (delta 0)
To https://bitbucket.org/NathanUrwin/cookiecutter-git-demo.git
* [new branch]      master -> master
Branch master set up to track remote branch master from origin.""",
    }

    def __init__(self, remote_provider, **kwargs):
        stdout = self.mock_stdout.get(remote_provider, "")
        super(MockResult, self).__init__(stdout, **kwargs)




class PostGenProjectHook(object):
    """
    Post Project Generation Class Hook.
    """
    json_header = {"Content-Type": "application/json; charset=utf-8"}
    repo_dirpath = os.getcwd()
    cookiecutter_json_filepath = os.path.join(
        repo_dirpath, "cookiecutter.json"
    )
    raw_repo_slug_dirpath = os.path.join(
        repo_dirpath, "{% raw %}{{cookiecutter.repo_slug}}{% endraw %}"
    )

    def __init__(self, *args, **kwargs):
        """
        Initializes the class instance.
        """

    def run(self):
        run('git clone {{cookiecutter.git_repository}}')
        subprocess.Popen(['sourcetrail', '{{cookiecutter.project_name}}.srctrlprj'])









def main():
    """
    Runs the post gen project hook main entry point.
    """
    PostGenProjectHook().run()


# This is required! Don't remove!!
if __name__ == "__main__":
    main()