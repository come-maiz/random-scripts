#!/usr/bin/env python2

import urllib2
import urlparse


def get_plugin_count(github_repo_url):
    count = {}
    repo = _get_repo_from_url(github_repo_url)
    snapcraft_yaml_file = _get_snapcraft_yaml_file(repo)
    if snapcraft_yaml_file:
        for line in snapcraft_yaml_file:
            line = line.strip()
            if line.startswith('plugin: '):
                plugin = line[8:]
                if plugin in count:
                    count[plugin] = count[plugin] + 1
                else:
                    count[plugin] = 1
        snapcraft_yaml_file.close()
    return count


def _get_repo_from_url(github_repo_url):
    parsed_url = urlparse.urlparse(github_repo_url)
    return parsed_url.path[1:]


def _get_snapcraft_yaml_file(github_repo):
    paths = ['snapcraft.yaml', '.snapcraft.yaml', 'snap/snapcraft.yaml']
    for path in paths:
        url = 'https://raw.githubusercontent.com/{}/master/{}'.format(
            github_repo, path)
        try:
            return urllib2.urlopen(url)
        except:
            pass
