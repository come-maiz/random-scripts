import apt


cache = apt.Cache()


def get_immediate_dependencies(package_name):
    try:
        return [dependency[0].name for dependency in cache[package_name].candidate.get_dependencies('Depends')]
    except KeyError:
        return []


def get_all_dependencies(name):
    dependencies = []
    to_visit = get_immediate_dependencies(name)
    while to_visit:
        package_name = to_visit.pop()
        if package_name not in dependencies:
            dependencies.append(package_name)
            for dependency in get_immediate_dependencies(package_name):
                if dependency not in dependencies and dependency not in to_visit:
                    to_visit.append(dependency)
    return dependencies


def get_dependency_count():
    count = {}
    for package in cache:
        dependencies = get_all_dependencies(package.name)
        dependency_count = len(dependencies)
        if not dependency_count in count:
            count[dependency_count] = [package.name]
        else:
            count[dependency_count].append(package.name)
    return count
