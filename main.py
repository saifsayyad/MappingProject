import argparse

from Application import Application


def check_positive(value):
    i_value = int(value)
    if i_value <= 0:
        raise argparse.ArgumentTypeError(f'{value} invalid input, has to be positive.')
    return i_value


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Argument Parser")
    parser.add_argument("--history", dest='history', action='store_true',
                        help="stores and reuses previously seen article info.")
    parser.add_argument("--interval", dest='interval', type=check_positive, default=5,
                        help="refresh interval in min (+ve integer value)")
    args = parser.parse_args()
    application = Application(args)
    application.start()
