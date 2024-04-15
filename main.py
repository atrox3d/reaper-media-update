from pathlib import Path
import os
import argparse

from atrox3d.simplegit import git, repos


SCRIPT_DIR = Path(__file__).parent
JSON_PATH = SCRIPT_DIR / 'projects.json'

os.chdir(SCRIPT_DIR)
BASE_DIR = '..'

# repos.backup(BASE_DIR, json_path=JSON_PATH, recurse=True)

def printheader(repo:git.GitRepo):
    print('-' * 80)
    print('/'.join(repo.get_path().parts[-2:]))
    print('-' * 80)

def print_files(tag:str, files:list, renamed=False):
        for file in files:
            if renamed:
                print(f'STATUS | {tag} | {file[0]!r} -> {file[0]!r}')
            else:
                print(f'STATUS | {tag} | {file}')

def printinfo(repo:git.GitRepo, status:git.GitStatus):
    print(f'{status.branch}: {status.remote_branch}')
    if status.need_pull:
        print('STATUS | PULL needed')
    if status.need_push:
        print('STATUS | PUSH needed')
    if status.dirty:
        print('STATUS | DIRTY')
        print_files('ADDED    ', status.added)
        print_files('UNTRACKED', status.untracked)
        print_files('MODIFIED ', status.modified)
        print_files('DELETED  ', status.deleted)
        print_files('RENAMED  ', status.renamed, renamed=True)

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--commit', default=None, nargs='?')
    parser.add_argument('-p', '--pull', action='store_true', default=False)
    parser.add_argument('-P', '--push', action='store_true', default=False)
    parser.add_argument('-a', '--addall', action='store_true', default=False)
    parser.add_argument('-x', '--all', action='store_true', default=False)
    parser.add_argument('-s', '--skipuptodate', action='store_true', default=False)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse()
    print(args)
    
    for repo in repos.scan(BASE_DIR, remote=True):
        git.fetch(repo)
        status = git.get_status(repo)

        if args.skipuptodate and not status.dirty and not status.need_pull and not status.need_push:
            continue

        printheader(repo)
        printinfo(repo, status)

        if args.pull:
            print(f'PULL')
            git.pull(repo)
        
        if status.dirty:
            if args.addall or args.all:
                print(f'ADDING | all files')
                git.add(repo, all=True)
            if args.commit or args.all:
                print(f'COMMIT | {args.commit or "AUTOMATIC COMMIT"}')
                git.commit(repo, args.commit or 'AUTOMATIC COMMIT', add_all=args.all)

        if args.push or args.all:
            print(f'PUSH')
            git.push(repo)
