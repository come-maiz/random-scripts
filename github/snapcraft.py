import re
import urlparse

import requests

_SCRIPLETS = ['prepare', 'build', 'install', 'version-script']
_tar_type_regex = re.compile(r'.*\.((tar(\.(xz|gz|bz2))?)|tgz)$')


def _get_repo_from_url(github_repo_url):
    """
    Get full repository name from github url
    :param github_repo_url: string, url
    :return: string, full name
    """
    parsed_url = urlparse.urlparse(github_repo_url)
    return parsed_url.path[1:]


def get_snapcraft_yaml_file(github_repo_url):
    """
    Extracts snapcraft file from repository
    :param github_repo_url: string, url of the repository
    :return: string, text of yaml file
    """

    github_repo = _get_repo_from_url(github_repo_url)
    paths = ['snapcraft.yaml', '.snapcraft.yaml', 'snap/snapcraft.yaml']
    for path in paths:
        url = 'https://raw.githubusercontent.com/{}/master/{}'.format(
            github_repo, path)
        response = requests.request('GET', url)

        if response.status_code == 200:
            return response.text


def get_plugins_count(snapcraft_file):
    """
    Parse plugins from a snapcraft file
    :param snapcraft_file: string, your snapcraft file
    :return: dict, {plugin: count}
    """
    plugins = {}

    for line in snapcraft_file.split('\n'):
        line = line.strip()
        if line.startswith('plugin: '):
            plugin = line[8:]
            if plugin in plugins:
                plugins[plugin] = plugins[plugin] + 1
            else:
                plugins[plugin] = 1
    return plugins


def get_scriplets_count(snapcraft_file):
    """
     Parse scriplets from a snapcraft file
     :param snapcraft_file: string, your snapcraft file
     :return: dict, {scriplet: count}
     """
    scriplets = {}

    for line in snapcraft_file.split('\n'):
        line = line.strip()
        line = line.split(':')[0]

        if line in _SCRIPLETS:
            if line not in scriplets:
                scriplets[line] = 1
            else:
                scriplets[line] += 1
    return scriplets


def get_sources_count(snapcraft_file):
    """
     Parse sources from a snapcraft file
     :param snapcraft_file: string, your snapcraft file
     :return: dict, {source: count}
     """
    sources = {}

    for line in snapcraft_file.split('\n'):
        line = line.strip()
        if line.startswith('source:'):
            src_type = _get_source_type_from_uri(line[7:])

            if src_type in sources:
                sources[src_type] += 1
            else:
                sources[src_type] = 1
    return sources


def _get_source_type_from_uri(source):
    """
    Detect source type of source
    Code copied from the snapcraft project: https://github.com/snapcore/snapcraft
    :param source: string, your source
    :return: string, source type
    """
    source_type = 'local'
    if source.startswith('bzr:') or source.startswith('lp:'):
        source_type = 'bzr'
    elif source.startswith('git:') or source.startswith('git@') or \
            source.endswith('.git'):
        source_type = 'git'
    elif source.startswith('svn:'):
        source_type = 'subversion'
    elif _tar_type_regex.match(source):
        source_type = 'tar'
    elif source.endswith('.zip'):
        source_type = 'zip'
    elif source.endswith('deb'):
        source_type = 'deb'
    elif source.endswith('rpm'):
        source_type = 'rpm'
    elif source.endswith('7z'):
        source_type = '7z'

    return source_type
