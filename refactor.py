#!/usr/bin/env python
# ------------------------------------------------------------
# refactor.py
#
# Modifies the boilerplate to a new given project name.
#
# Author:
# Victor De Ponte, <rdbvictor19@gmail.com>
# ------------------------------------------------------------
import os
import argparse
import subprocess

def git(*args):
    return subprocess.check_output(['git'] + list(args))


class Refactorer(object):
    """Refactors the boilerplate to a new project name"""

    def __init__(self, *args, **kwargs):
        super (Refactorer, self).__init__()
        self._project = None
        self._repo = None
        self._repo_git = None
        self._website = None
        self._run_extras = False

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.__unicode__())

    def __unicode__(self):
        return "Refactorer(project=%s, repo=%s, website=%s, extras=%s)" % (
            self._project, self._repo, self._website, str(self._run_extras))

    def process_args(self):
        description  = "This script modifies the boilerplate so it is called "
        description += "like the new given project name."
        args_parser = argparse.ArgumentParser(
            prog="refactor.py",
            description=description,
            epilog="Author: Victor De Ponte <rdbvictor19@gmail.com>, @Throoze."
            )
        args_parser.add_argument('-v','--version', 
            action='version', version='%(prog)s 1.0')
        # args_parser.add_argument('-i','--has-issue-tracking', action='store_true',
        #     help="adds issue tracking information")
        args_parser.add_argument('project_name',
            help="the name of the new project (without spaces)")
        args_parser.add_argument('username',
            help="your remote's repo host username (used for building repo address)")
        args_parser.add_argument('-g', '--git-remote-host', default='github.com',
            help="your project's git remote manager. Accepted: github.com or bitbucket.org. Default: github.com")
        args_parser.add_argument('-r', '--repo-address',
            help="your project's git repo's https address. Default: project_name on selected git host")
        args_parser.add_argument('-w','--website', 
            help="your project's website. Default: repo_address (without .git extension)")
        args_parser.add_argument('-e','--run-extras', 
            help="run extra commands indicated in README.md (not implemented yet)", action='store_true')
        ns = args_parser.parse_args()
        if ns.repo_address is None:
            ns.repo_address = "https://%s/%s/%s.git" % (
                ns.git_remote_host, ns.username, ns.project_name)
        if ns.website is None:
            ns.website = ns.repo_address[:len(ns.repo_address)-4]
        self._project = ns.project_name
        self._repo = ns.repo_address
        self._website = ns.website
        self._repo_git = "git@%s:%s/%s.git" % (
            ns.git_remote_host, ns.username, ns.project_name)
        self._run_extras = ns.run_extras

    def modify_bower_json(self):
        f = open('./bower.json','r+')
        text = f.read()
        old_name = '"name": "thinkster_django_angular_boilerplate"'
        new_name = '"name": "%s"' % self._project
        old_web = '"homepage": "https://github.com/brwr/thinkster-django-angular-boilerplate"'
        new_web = '"homepage": "%s"' % self._website
        new_text = text.replace(old_name, new_name).replace(old_web, new_web)
        f.write(new_text)
        f.close()

    def modify_manage_py(self):
        f = open('./manage.py','r+')
        text = f.read()
        new_text = text.replace('thinkster_django_angular_boilerplate', self._project)
        f.write(new_text)
        f.close()

    def modify_package_json(self):
        f = open('./package.json','r+')
        text = f.read()
        old_name = '"name": "thinkster_django_angular_boilerplate"'
        new_name = '"name": "%s"' % self._project
        old_repo = '"url": "https://github.com/brwr/thinkster-django-angular-boilerplate'
        new_repo = '"url": "%s' % self._website
        old_web = '"homepage": "https://github.com/brwr/thinkster-django-angular-boilerplate"'
        new_web = '"homepage": "%s"' % self._website
        new_text = text.replace(old_repo, new_repo).replace(old_web, new_web).replace(old_name, new_name)
        f.write(new_text)
        f.close()
        

    def modify_procfile(self):
        f = open('./Procfile','r+')
        text = f.read()
        old = 'web: gunicorn thinkster_django_angular_boilerplate.wsgi --log-file -'
        new = 'web: gunicorn %s.wsgi --log-file -' % self._project
        new_text = text.replace(old, new)
        f.write(new_text)
        f.close()

    def modify_js_module(self):
        old_name = './static/javascripts/thinkster.js'
        new_name = './static/javascripts/%s.js' % self._project
        git('mv', old_name, new_name)
        f = open(new_name,'r+')
        text = f.read()
        old = 'thinkster'
        new = '%s' % self._project
        new_text = text.replace(old, new)
        f.write(new_text)
        f.close()

    def modify_templates(self):
        templates = [
            "./templates/index.html",
            "./templates/javascripts.html"
        ]
        for filename in templates:
            with open(filename, 'r+') as f:
                text = f.read()
                o1 = 'thinkster-django-angular-boilerplate'
                o2 = 'thinkster'
                n1 = '%s project' % self._project
                n2 = '%s' % self._project
                new_text = text.replace(o1, n1.title()).replace(o2, n2)
                f.write(new_text)

    def modify_django_files(self):
        folder = "./thinkster_django_angular_boilerplate/"
        files = [
            folder + "settings_global.py",
            folder + "settings.dist.py",
            folder + "urls.py",
            folder + "wsgi.py"
        ]
        settings_env = folder + "settings.py"
        for filename in files:
            with open(filename, 'r+') as f:
                text = f.read()
                old = "thinkster_django_angular_boilerplate"
                new = self._project
                new_text = text.replace(old, new)
                f.write(new_text)
        import shutil
        shutil.copyfile(files[1], settings_env)
        os.rename(folder, "./" + self._project)

    def apply_changes_to_git_repo(self):
        git('add','.')
        git('commit','-m','Boilerplate refactored to new project: {0}'.format(self._project))
        git('checkout', '--track', 'origin/release')
        git('merge', 'master')
        git('checkout', 'master')
        git('remote', 'remove', 'origin')
        git('remote', 'add', 'origin', self._repo_git)
        git('push', '--all')
        git('push', '--tags')

    def run_extras(self):
        if self._run_extras:
            print 'Running extra commands...'
            # TODO: run extra commands

    def run(self):
        self.process_args()
        self.modify_bower_json()
        self.modify_manage_py()
        self.modify_package_json()
        self.modify_procfile()
        self.modify_js_module()
        self.modify_templates()
        self.modify_django_files()
        self.apply_changes_to_git_repo()
        self.run_extras()
    



if __name__ == '__main__':
    refactor = Refactorer()
    refactor.run()
    exit(0)