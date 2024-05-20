import log
logger = log.get_logger(__name__)

from atrox3d.simplegit import git

def isclean(status:git.GitStatus) -> bool:
    return not any([
                status.dirty,
                status.need_pull,
                status.need_push,
            ])

def grep(repos: list[git.GitRepo], names: list):
    for repo in repos:
        if not names:
            logger.debug(f'PROCESSING {repo.name}: NO NAMES LIST')                    
            yield repo
        else:
            for name in names:
                if name in repo.name:
                    logger.debug(f'PROCESSING {repo.name}: in name list: {names}')                    
                    yield repo
                    break
                else:
                    logger.debug(f'SKIPPING {repo.name}: not in name list: {names}')

def exclude(repos: list[git.GitRepo], names: list):
    for repo in repos:
        if not names:
            logger.debug(f'PROCESSING {repo.name}: NO NAMES LIST')                    
            yield repo
        else:
            for name in names:
                if name not in repo.name:
                    logger.debug(f'PROCESSING {repo.name}: in name list: {names}')                    
                    yield repo
                    break
                else:
                    logger.debug(f'EXCLUDING {repo.name}: not in name list: {names}')
