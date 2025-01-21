import argparse

def parse():
    parser = argparse.ArgumentParser()
    # output
    parser.add_argument('-L', '--loglevel', default='INFO',
                        help='sets log level, default info')
    parser.add_argument('-o', '--print-options-and-exit', action='store_true', default=False,
                        help='prints options and exit')

    # actions
    parser.add_argument('-c', '--commit', default=None,
                        help='commits with the provided message')
    parser.add_argument('-p', '--pull', action='store_true', default=False,
                        help='pulls from origin after getting status')
    parser.add_argument('-P', '--push', action='store_true', default=False,
                        help='pushed at the end')
    parser.add_argument('-a', '--addall', action='store_true', default=False,
                        help='adds all the files before committing')
    parser.add_argument('-x', '--add-commit-push', action='store_true', default=False,
                        help='adds, commits and pushes')
    # parser.add_argument('-r', '--run-git-commands', action='extend', nargs='+', type=str, default=[])
    # filters
    parser.add_argument('-s', '--skipclean', action='store_true', default=False,
                        help='skips repos with no modifications')
    parser.add_argument('-l', '--listrepos', action='store_true', default=False,
                        help='list repos without performing any op')
    parser.add_argument('-f', '--filter', nargs='+', default=[],
                        choices='dirty push pull unclean'.split(),
                        help='process only repos with the status specified')
    parser.add_argument('-g', '--grep', action='extend', nargs='+', type=str, default=[],
                        help='include only repos containig one of the strings')
    parser.add_argument('-e', '--exclude', action='extend', nargs='+', type=str, default=[],
                        help='exclude repos containig one of the strings')

    args = parser.parse_args()
    return args

