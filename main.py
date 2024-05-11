from pathlib import Path
import os
import argparse
import logging

from atrox3d.simplegit import git, repos

SCRIPT_DIR = Path(__file__).parent
JSON_PATH = SCRIPT_DIR / 'projects.json'

os.chdir(SCRIPT_DIR)
BASE_DIR = '..'

# repos.backup(BASE_DIR, json_path=JSON_PATH, recurse=True)

def printheader(repo:git.GitRepo, width=80, print=print):
    print('-' * 80)
    path = '/'.join(repo.get_path().parts[-2:])
    branch = f'{status.branch}: {status.remote_branch}'
    print(f'{path}{branch:>{width-len(path)}}')

def printfooter(print=print):
    print('-' * 80)

def print_files(tag:str, files:list, renamed=False, print=print):
        for file in files:
            if renamed:
                print(f'STATUS | {tag} | {file[0]!r} -> {file[0]!r}')
            else:
                print(f'STATUS | {tag} | {file}')

def printinfo(repo:git.GitRepo, status:git.GitStatus, print=print):
    # print(f'{status.branch}: {status.remote_branch}')
    if status.need_pull:
        print('STATUS | PULL needed')
    if status.need_push:
        print('STATUS | PUSH needed')
    if status.dirty:
        print('STATUS | DIRTY')
        print_files('ADDED    ', status.added, print=print)
        print_files('UNTRACKED', status.untracked, print=print)
        print_files('MODIFIED ', status.modified, print=print)
        print_files('DELETED  ', status.deleted, print=print)
        print_files('RENAMED  ', status.renamed, renamed=True, print=print)

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-L', '--loglevel', default='INFO')
    parser.add_argument('-c', '--commit', default=None, nargs='?')
    parser.add_argument('-p', '--pull', action='store_true', default=False)
    parser.add_argument('-P', '--push', action='store_true', default=False)
    parser.add_argument('-a', '--addall', action='store_true', default=False)
    parser.add_argument('-x', '--all', action='store_true', default=False)
    parser.add_argument('-s', '--skipclean', action='store_true', default=False)
    parser.add_argument('-l', '--listrepos', action='store_true', default=False)
    parser.add_argument('-f', '--filter', nargs='+', default=[],
                        choices='dirty push pull unclean'.split())
    parser.add_argument('-g', '--grep', action='append', default=[])
    parser.add_argument_group
    args = parser.parse_args()
    return args

def isclean(status:git.GitStatus) -> bool:
    return not any([
                status.dirty,
                status.need_pull,
                status.need_push,
            ])

def setup_logger(
                    level: int|str =logging.INFO,
                    root_level: int|str =logging.INFO,
                    format: str='%(levelname)5s | %(message)s'
                ) -> logging.Logger:
    LOGFILE = str(Path(__file__).parent / Path(__file__).stem) + '.log'
    handlers = [
        logging.FileHandler(LOGFILE, mode='w'),
        logging.StreamHandler()
    ]
    logging.basicConfig(level=root_level, format=format, handlers=handlers)
    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    return logger

def print_args(args: argparse.Namespace, print=print) -> None:
    for arg, value in vars(args).items():
        print(f'{arg} = {value}')

def grep(repos: list[git.GitRepo], names: list):
    for repo in repos:
        if not names:
            yield repo
        else:
            for name in names:
                if name in repo.name:
                    yield repo
                    break

if __name__ == '__main__':
    args = parse()
    logger = setup_logger(level=args.loglevel.upper())
    print_args(args, logger.debug)
    for repo in grep(repos.scan(BASE_DIR, has_remote=True), args.grep):
        try:
            logger.debug(f'fetching {repo.remote}')
            git.fetch(repo)
            logger.debug(f'getting status for {repo.path}')
            status = git.get_status(repo)

            if args.skipclean and isclean(status):
                logger.debug(f'skipping clean repo: {repo.path}')
                continue
            if 'unclean' in args.filter and isclean(status):
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
            
            printheader(repo, print=logger.info)
            printinfo(repo, status, print=logger.info)

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