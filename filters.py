import argparse
import types
# from functools import partial

import filters
import log
logger = log.get_logger(__name__)

from atrox3d.simplegit import git

def is_clean(status:git.GitStatus) -> bool:
    return not any([
                status.dirty,
                status.need_pull,
                status.need_push,
            ])

def matches_substring(target: str, substrings: list[str]) -> bool:
    for substring in substrings:
        if substring in target:
            return True
    return False

def is_processable(name, include, exclude):
    if include:
        if not matches_substring(name, include):
            return False
    if exclude:
        if  matches_substring(name, exclude):
            return False
    return True


def meet_args_conditions(repo: git.GitRepo, status: git.GitStatus, args: argparse.Namespace) -> bool:
    if args.skipclean and filters.is_clean(status):
        logger.debug(f'skipping clean repo: {repo.path}')
        return False

    if 'unclean' in args.filter and filters.is_clean(status):
        logger.debug(f'skipping clean repo: {repo.path}')
        return False

    if 'dirty' in args.filter and not status.dirty:
        logger.debug(f'skipping non-dirty repo: {repo.path}')
        return False

    if 'pull' in args.filter and not status.need_pull:
        logger.debug(f'skipping non-pull repo: {repo.path}')
        return False

    if 'push' in args.filter and not status.need_push:
        logger.debug(f'skipping non-push repo: {repo.path}')
        return False

    return True
