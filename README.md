# KYC-Api

## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it
easy? [Use the template at the bottom](#editing-this-readme)!

## Architecture of the API

It Just Uses MVC Architecture Try googling it

## Integrate with your tools

It also includes docker.

- [x] [Set up project integrations](https://gitlab.com/sujeet.k1/flask-api/-/settings/integrations)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/index.html)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing(SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to
structure it however you want - this is just a starting point!). Thank you
to [makeareadme.com](https://www.makeareadme.com/) for this template.

## Suggestions for a good README

Every project is different, so consider which of these sections apply to yours. The sections used in the template are
suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long
is better than too short. If you think your README is too long, consider utilizing another form of documentation rather
than cutting out information.

## Name

Choose a self-explaining name for your project.

## Description

Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be
unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your
project, this is a good place to list differentiating factors.

## Badges

On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the
project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Installation

Developed using python 3.10

Install using pip

```commandline
pip install -r requirements.txt
```

Additional Docker configuration is available.

```docker
docker build -f Dockerfile .
```

## Error Codes

IPPC -> Image Pre-Processor crash

FCC -> Filter Code Crash

MB -> Model Broke

> if you have any problem Contact ....... NO ONE

## Branching Strategy

Why this well, it were hard to maintain a code base forget passing on to other engineers you cant handle very much.

> Note git\git bash should be installed into your machine. if you want to make changes

![alt text](https://miro.medium.com/max/1400/1*9yJY7fyscWFUVRqnx0BM6A.png)

* The Master of the branch is main
* If you want to add additional features to this project use command

```git
git flow feature start <Name_the_feature>
```

when finished developing the feature please use this command

```git
git flow feature finish <Name_the_feature>
```

Once develop has acquired enough features for a release (or a predetermined release date is approaching), you _'fork'_ a
release branch off of develop.

#### why release? well...

No new features can be added after this point — only bug fixes, documentation generation, and other release-oriented
tasks should go in this branch.

```git
git flow release start <tag>
```

> To finish a release branch, use the following methods:

```git
git flow release finish <tag>
```

> ### There include other features

like **Hotfix**, what you say????

Well “hotfix” branches are used to quickly patch production releases.

```git
git flow hotfix start hotfix_branch
```

and there is **support** ,**BugFix**
honestly I don't have any patience to write anymore do your own research

## Support

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address,
etc.

## Roadmap

If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing

State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started.
Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps
explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce
the likelihood that the changes inadvertently break something. Having instructions for running tests is especially
helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Reference

Official Website

- [Flask](https://flask.palletsprojects.com/)
- [Gunicorn](http://gunicorn.org/)
- [Python](https://www.python.org/)
- [Docker](https://docs.docker.com/)

Tutorial

- [Python](https://docs.python.org/3/tutorial/)

## Authors and acknowledgment

- Sujeet(_**"Me"**_)

## Project status

Current bugs list

    -  image pre-porcessor is not working properly
    -  acurate name is not picked properly from pan and aadhaar ocr