from pathlib import Path
import os
import argparse
import logging

from atrox3d.simplegit import git, repos
import filters
import options
import output

SCRIPT_DIR = Path(__file__).parent
JSON_PATH = SCRIPT_DIR / 'projects.json'

os.chdir(SCRIPT_DIR)
BASE_DIR = '..'

# repos.backup(BASE_DIR, json_path=JSON_PATH, recurse=True)

if __name__ == '__main__':
    args = options.parse()
    logger = output.setup_logger(level=args.loglevel.upper())
    output.print_args(args, logger.debug)

    for repo in filters.grep(repos.scan(BASE_DIR, has_remote=True), args.grep):
        try:
            logger.debug(f'fetching {repo.remote}')
            git.fetch(repo)
            
            logger.debug(f'getting status for {repo.path}')
            status = git.get_status(repo)

            if args.skipclean and filters.isclean(status):
                logger.debug(f'skipping clean repo: {repo.path}')
                continue
            if 'unclean' in args.filter and filters.isclean(status):
                logger.debug(f'skipping clean repo: {repo.path}')
                continue
            if 'dirty' in args.filter and not status.dirty:
                logger.debug(f'skipping non-dirty repo: {repo.path}')
                continue
            if 'pull' in args.filter and not status.need_pull:
                logger.debug(f'skipping non-pull repo: {repo.path}')
                continue
            if 'push' in args.filter and not status.need_push:
                logger.debug(f'skipping non-push repo: {repo.path}')
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
                if args.addall or args.all:
                    logger.info(f'ADDING | all files')
                    git.add(repo, all=True)
                if args.commit or args.all:
                    logger.info(f'COMMIT | {args.commit or "AUTOMATIC COMMIT"}')
                    git.commit(repo, args.commit or 'AUTOMATIC COMMIT', add_all=args.all)

            if args.push or args.all:
                logger.info(f'PUSH')
                git.push(repo)
            # printfooter()
        except git.GitException as ge:
            ge.print(printer=logger.error)