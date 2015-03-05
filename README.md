django-angular-boilerplate
==========================
Based in a fork from [thinkster-django-angular-boilerplate](https://github.com/brwr/thinkster-django-angular-boilerplate)


## Installation

*NOTE: Requires [virtualenv](http://virtualenv.readthedocs.org/en/latest/),
[virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/) and
[Node.js](http://nodejs.org/).*

* Clone this repository.
* Create a new repository in github or bitbucket, and name it whatever you want
* `$ git clone git@github.com:<your username>/thinkster-django-angular-boilerplate.git <your project>`
* `$ cd <your project>/`
* `$ python refactor.py [-g GIT_REMOTE_HOST] [-r REPO_ADDRESS] [-w WEBSITE] [-e] project_name username` (`$ python refactor.py -h` for usage, or read below)
* `$ mkvirtualenv your-project-env`
* `$ pip install -r requirements.txt`
* `$ npm install -g bower`
* `$ npm install`
* `$ bower install`
* `$ python manage.py migrate`
* `$ python manage.py runserver`


## Refactor usage


        usage: refactor.py [-h] [-v] [-g GIT_REMOTE_HOST] [-r REPO_ADDRESS]
                           [-w WEBSITE] [-e] [-s]
                           project_name username

        This script modifies the boilerplate so it is called like the new given
        project name.

        positional arguments:
          project_name          the name of the new project (without spaces)
          username              your remote's repo host username (used for building
                                repo address)

        optional arguments:
          -h, --help            show this help message and exit
          -v, --version         show program's version number and exit
          -g GIT_REMOTE_HOST, --git-remote-host GIT_REMOTE_HOST
                                your project's git remote manager. Accepted:
                                github.com or bitbucket.org. Default: github.com
          -r REPO_ADDRESS, --repo-address REPO_ADDRESS
                                your project's git repo's https address. Default:
                                project_name on selected git host
          -w WEBSITE, --website WEBSITE
                                your project's website. Default: repo_address (without
                                .git extension)
          -e, --run-extras      run extra commands indicated in README.md (requires
                                sudo)
          -s, --runserver       starts django development web server in
                                http://localhost:8000/

