import argparse
# import logging
# from pathlib import Path

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
    if status.need_pull or status.need_push or status.dirty:
        printfooter(print)
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

def print_args(args: argparse.Namespace, print=print) -> None:
    for arg, value in vars(args).items():
        print(f'{arg} = {value}')
