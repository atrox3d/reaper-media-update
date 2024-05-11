import argparse

def parse():
    parser = argparse.ArgumentParser()
    # output
    parser.add_argument('-L', '--loglevel', default='INFO')
    # actions
    parser.add_argument('-c', '--commit', default=None, nargs='?')
    parser.add_argument('-p', '--pull', action='store_true', default=False)
    parser.add_argument('-P', '--push', action='store_true', default=False)
    parser.add_argument('-a', '--addall', action='store_true', default=False)
    parser.add_argument('-x', '--all', action='store_true', default=False)
    # filters
    parser.add_argument('-s', '--skipclean', action='store_true', default=False)
    parser.add_argument('-l', '--listrepos', action='store_true', default=False)
    parser.add_argument('-f', '--filter', nargs='+', default=[],
                        choices='dirty push pull unclean'.split())
    # parser.add_argument('-g', '--grep', action='append', default=[])
    parser.add_argument('-g', '--grep',
                        # dest='array',
                        action='extend',
                        nargs='+',
                        type=str,
                        default=[]
                        )

    # parser.add_argument_group
    args = parser.parse_args()
    return args

