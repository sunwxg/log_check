from optparse import OptionParser 

def args_options():

    usage = "usage: %prog [options] [node] < log_file\n" + \
            "      [node] = axe (default)\n" + \
            "             = mgw\n" \
            "      [options]\n" \
            "             --version\n" \
            "             --help\n" \
            "             -h"

    parser = OptionParser(usage=usage, version='This %prog version is 0.1')

    (options, args) = parser.parse_args()

