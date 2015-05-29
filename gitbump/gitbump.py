# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import click
import subprocess

@click.command()
@click.option('--major', is_flag=True, help="Bump the major number of the release")
@click.option('--minor', is_flag=True, help="Bump the minor number of the release")
@click.option('--patch', is_flag=True, help="Bump the patch number of the release")
@click.option('--build', is_flag=True, help="Mark as a build release, e.g. v1.0.1-build.1")
@click.option('--alpha', is_flag=True, help="Mark as an alpha release, e.g. v1.0.1-alpha.1")
@click.option('--beta', is_flag=True, help="Mark as a beta release, e.g. v1.0.1-beta.1")
@click.option('--rc', is_flag=True, help="Mark as an rc release, e.g. v1.0.1-rc.1")
@click.option('--stable', is_flag=True, help="Mark as a stable release, e.g. v1.0.2")
@click.option('--noconfirm', is_flag=True, help="Skip manual confirmation")
@click.option('--nopush', is_flag=True, help="Don't automatically push branch and tags")
def gitbump(major, minor, patch, build, alpha, beta, rc, stable, noconfirm, nopush):
    new_tag = None
    latest_tag = _get_latest_tag()
    vtag = Semver(latest_tag)

    # If none of the version relevant switches is given do autobump.
    if not any((major, minor, patch, build, alpha, beta, rc, stable)):
        new_tag = vtag.autobump()

    if not noconfirm:
        click.confirm(
            'gitbump will add this tag: {}. Continue?'.format(new_tag),
            default=True,
            abort=True
        )

    subprocess.check_call([
        'git',
        'tag',
        '-a', '{}'.format(new_tag),
        '-m', 'version {}'.format(new_tag[1:])
    ])

    if not nopush:
        subprocess.check_call(['git', 'push'])
        subprocess.check_call(['git', 'push', '--tags'])


def _get_latest_tag():
    """ Return the latest tag from a repository in the current working dir.
    """
    try:
        latest_tag = subprocess.check_output(
            ['git', 'describe', '--abbrev=0'],
            stderr=subprocess.STDOUT
        )
    except subprocess.CalledProcessError, e:
        click.secho(
            'Error calling git describe. Is your directory under VC? '
            'and do you already use semver like tags in it?',
            fg='red'
        )
        exit(1)
        return

    return latest_tag


class Semver(object):
    def __init__(self, tag):
        tag = tag.replace('-', '.')
        # Remove the v and the new line at the end.
        tag_list = tag[1:-1].split('.')
        self.major = int(tag_list[0])
        self.minor = int(tag_list[1])
        self.patch = int(tag_list[2])
        self.channel = None if len(tag_list) < 4 else tag_list[3]
        self.channel_version = None if len(tag_list) < 5 else int(tag_list[4])
        self.tag_list = [
            self.major,
            self.minor,
            self.patch,
            self.channel,
            self.channel_version
        ]
        self.version_format = 'stable' if len(self.tag_list) == 3 else 'channel'

    def get_tag_list(self):
        return self.tag_list

    def autobump(self):
        """ Increases last digit of latest tag.
        """
        if self.version_format == 'stable':
            self.patch += 1

        output = 'v{}.{}.{}'.format(
            self.major,
            self.minor,
            self.patch
        )

        if self.version_format == 'channel':
            self.channel_version += 1
            output += '-{}.{}'.format(
                self.channel,
                self.channel_version
            )

        return output

if __name__ == '__main__':
    gitbump()
