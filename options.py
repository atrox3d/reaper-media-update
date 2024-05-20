import argparse

def parse():
    parser = argparse.ArgumentParser()
    # output
    parser.add_argument('-L', '--loglevel', default='INFO')
    parser.add_argument('-o', '--print-options-and-exit', action='store_true', default=False)

    # actions
    parser.add_argument('-c', '--commit', default=None)
    parser.add_argument('-p', '--pull', action='store_true', default=False)
    parser.add_argument('-P', '--push', action='store_true', default=False)
    parser.add_argument('-a', '--addall', action='store_true', default=False)
    parser.add_argument('-x', '--add-commit-push', action='store_true', default=False)
    # parser.add_argument('-r', '--run-git-commands', action='extend', nargs='+', type=str, default=[])
    # filters
    parser.add_argument('-s', '--skipclean', action='store_true', default=False)
    parser.add_argument('-l', '--listrepos', action='store_true', default=False)
    parser.add_argument('-f', '--filter', nargs='+', default=[],
                        choices='dirty push pull unclean'.split())
    parser.add_argument('-g', '--grep', action='extend', nargs='+', type=str, default=[])
    parser.add_argument('-e', '--exclude', action='extend', nargs='+', type=str, default=[])

    args = parser.parse_args()
    return args

