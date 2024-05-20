from pathlib import Path
import os
import argparse
# import logging

# import log
# log.setup_logging() # setup logging before imports

from atrox3d.simplegit import git, repos
from atrox3d.logger import logmanager as log, modulelogging as mlog
# from atrox3d.logging import logmanager
import filters
import options
import output

SCRIPT_DIR = Path(__file__).parent
JSON_PATH = SCRIPT_DIR / 'projects.json'

os.chdir(SCRIPT_DIR)
BASE_DIR = '..'

def meet_args_conditions(repo: git.GitRepo, status: git.GitStatus, args: argparse.Namespace) -> bool:
    if args.skipclean and filters.isclean(status):
        logger.info(f'skipping clean repo: {repo.path}')
        return False
    
    if 'unclean' in args.filter and filters.isclean(status):
        logger.info(f'skipping clean repo: {repo.path}')
        return False
    
    if 'dirty' in args.filter and not status.dirty:
        logger.info(f'skipping non-dirty repo: {repo.path}')
        return False
    
    if 'pull' in args.filter and not status.need_pull:
        logger.info(f'skipping non-pull repo: {repo.path}')
        return False
    
    if 'push' in args.filter and not status.need_push:
        logger.info(f'skipping non-push repo: {repo.path}')
        return False
    
    return True


if __name__ == '__main__':
    args = options.parse()
    log.setup_logging(caller_path=__file__)
    logger = log.get_logger(__name__, level=args.loglevel.upper())
    mlog.set_module_loggers_level(filters, args.loglevel.upper())
    output.print_args(args, logger.info)
    if args.print_options_and_exit:
        exit()
    
    for repo in filters.exclude(filters.grep(repos.scan(BASE_DIR, has_remote=True), args.grep), args.exclude):
        try:
            logger.debug(f'fetching {repo.remote}')
            git.fetch(repo)
            
            logger.debug(f'getting status for {repo.path}')
            status = git.get_status(repo)

            if not meet_args_conditions(repo, status, args):
                continue

            if args.listrepos:
                logger.debug(f'listing only repo: {repo.path}')
                logger.info('/'.join(repo.get_path().parts[-2:]))
                continue
            
            output.printheader(repo, status, print=logger.info)
            output.printinfo(repo, status, print=logger.info)

            if args.pull:
                logger.info(f'PULL')
                git.pull(repo)
            
            if status.dirty:
                if args.addall or args.add_commit_push:
                    logger.info(f'ADDING | all files')
                    git.add(repo, all=True)
                if args.commit or args.add_commit_push:
                    logger.info(f'COMMIT | {args.commit or "AUTOMATIC COMMIT"}')
                    git.commit(repo, args.commit or 'AUTOMATIC COMMIT', add_all=args.all)

            if args.push or args.add_commit_push:
                logger.info(f'PUSH')
                git.push(repo)
            # printfooter()
        except git.GitException as ge:
            ge.print(printer=logger.error)