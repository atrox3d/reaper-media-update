import argparse
import logging
from pathlib import Path

from atrox3d.simplegit import git, repos


def printheader(repo:git.GitRepo, status:git.GitStatus, width=80, print=print):
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
