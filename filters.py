
from atrox3d.simplegit import git, repos

def isclean(status:git.GitStatus) -> bool:
    return not any([
                status.dirty,
                status.need_pull,
                status.need_push,
            ])

def grep(repos: list[git.GitRepo], names: list):
    for repo in repos:
        if not names:
            yield repo
        else:
            for name in names:
                if name in repo.name:
                    yield repo
                    break
