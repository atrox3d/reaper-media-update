from pathlib import Path
import os

from atrox3d.simplegit import git, repos
from atrox3d.logger import logmanager, modulelogging

import filters
import options
import output

SCRIPT_DIR = Path(__file__).parent
JSON_PATH = SCRIPT_DIR / 'projects.json'

os.chdir(SCRIPT_DIR)
BASE_DIR = '..'

if __name__ == '__main__':
    args = options.parse()
    
    logmanager.setup_logging(caller_path=__file__)
    modulelogging.set_module_loggers_level(filters, args.loglevel.upper())
    logger = logmanager.get_logger(__name__, level=args.loglevel.upper())

    output.print_args(args, logger.info)
    if args.print_options_and_exit:
        exit()
    
    for repo in repos.scan(BASE_DIR, has_remote=True):
        if not filters.is_processable(repo.name, args.grep, args.exclude):
            logger.info(f'filtering out {repo.name}')
            continue

        if args.listrepos:
            logger.debug(f'listing only repo: {repo.path}')
            logger.info('/'.join(repo.get_path().parts[-2:]))
            continue

        try:

            logger.debug(f'fetching {repo.remote}')
            git.fetch(repo)
            
            logger.debug(f'getting status for {repo.path}')
            status = git.get_status(repo)

            if not filters.meet_args_conditions(repo, status, args):
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