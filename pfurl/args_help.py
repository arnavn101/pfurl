from colorama import Fore as Colors
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import pkg_resources

from pfurl import man

# get package version number from setup.py
# https://stackoverflow.com/a/2073599/6023006
VERSION = pkg_resources.require('pfurl')[0].version


def indent(string: str, spaces=4):
    """Add some spaces in front of every newline character."""
    space = '\n' + (' ' * spaces)
    return space + string.replace('\n', space)


DESCRIPTION_TEXT = f"""
`pfurl` is a communications program that sends http-type curl 
data to a remote service. Although it is mostly used in the 
"pf" family of programs and in the ChRIS suite, it can be also
used a general-purpose curl replacement.

In addition to sending JSON-formatted strings to a service, 
`pfurl` can also send files and whole directories -- the latter
being a zip compression of a directory tree.

Various authentication options for verifying identify with the
remote service are also available.
"""


EXAMPLE = f"""
EXAMPLE

    Say 'hello' to a `pfcon` service listening on the localhost at port 5005
    and print response "prettily" using an indent of 4.
    
        pfurl                                                   \\
            --verb POST --raw                                   \\
            --http {man.EXAMPLE_HTTP}             \\
            --jsonwrapper 'payload'                             \\
            --msg                                               \\
                '{{  "action": "hello",
                    "meta": {{
                        "askAbout":     "sysinfo",
                        "echoBack":     "Hi there!",
                        "service":      "host"
                    }}
                }}' --quiet --jsonpprintindent 4

"""

FULL_DESCRIPTION = f"""
{Colors.CYAN}
        __            _ 
       / _|          | |
 _ __ | |_ _   _ _ __| |
| '_ \|  _| | | | '__| |
| |_) | | | |_| | |  | |
| .__/|_|  \__,_|_|  |_|
| |                     
|_|                     


                            Process-File-over-URL

           A simple URL-based communication and control script.

                              -- version {Colors.YELLOW}{VERSION}{Colors.CYAN} --

    {indent(DESCRIPTION_TEXT)}

{Colors.RED}

              +---------------------------------------------------------+
              | Use --auth <user>:<password> and --authToken <token>    |
              |         arguments for secure communication.             |    
              +---------------------------------------------------------+
{Colors.RESET}



    NAME

            pfurl 

        - curl-type http communication client.

    USAGE

            pfurl
"""

MAN_TOPICS = ', '.join(man.DICTIONARY.keys())

def nat(num):
    """Converts a value to a positive number, or throws a TypeError"""
    num = int(num)
    if num < 1:
        raise TypeError(f'{num} < 1')
    return num


parser = ArgumentParser(allow_abbrev=False,
                        formatter_class=ArgumentDefaultsHelpFormatter)

# we cannot customize the order of appearance so leave these out
# description=man.LONG_DESCRIPTION,
# epilog=man.EXAMPLE,


parser.add_argument('--msg',
                    metavar='<JSONpayload>',
                    type=str,
                    help='Message to send to pman or similar listener')
parser.add_argument('--verb',
                    metavar='RESTVERB',
                    type=str,
                    help='The REST verb to use for the remote service')
parser.add_argument('--http',
                    metavar='http://<IP>[:<port>]</some/path/>',
                    default=f'{man.LOCAL_IP_ADDRESS}:5055',
                    help='The address of the remote service')
parser.add_argument('--httpProxy',
                    metavar='[http://]<IP>[:<port>]',
                    type=str,
                    help='If specified, instruct `pfurl` to use the proxy as specified. '
                         'Currently, only "http" is supported. '
                         '(example: --httpProxy http://proxy.host.org:1234)')
parser.add_argument('--auth',
                    metavar='<user>:<passwd>',
                    type=str,
                    help='A user name and password authentication string')
parser.add_argument('--jsonwrapper',
                    metavar='<outerMsgJSONwrapper>',
                    type=str,
                    help='An optional outer wrapper for the JSON payload')
parser.add_argument('--quiet',
                    action='store_true',
                    help='if specified, only echo the final JSON payload returned'
                         '\nfrom remote server')
parser.add_argument('--raw',
                    action='store_true',
                    help='Do not wrap return data from remote call in a JSON wrapper')
parser.add_argument('--oneShot',
                    action='store_true',
                    help='Transmit a shutdown control sequence to remote server '
                         'after communicating. This of course only works for services that '
                         'understand the shutdown protocol')
parser.add_argument('--man',
                    metavar='<topic>',
                    type=str,
                    help='Provide detailed help on various topics (possible values: )'
                          + MAN_TOPICS)
parser.add_argument('--desc', '-x',
                    action='store_true',
                    help="Provide an overview help page")
parser.add_argument('--synopsis', '-y',
                    action='store_true',
                    help="Provide a short help summary")
parser.add_argument('--content-type',
                    metavar='type',
                    type=str,
                    help='Curl content-type descriptor')
parser.add_argument('--jsonpprintindent',
                    metavar='<indent>',
                    type=nat,
                    help='Print return JSON payload from remote service using')
parser.add_argument('--httpResponseBodyParse',
                    action='store_true',
                    help='Interpret the return payload as encapsulated in an http response')
parser.add_argument('--version',
                    action='store_true',
                    help='Print version number')
parser.add_argument('--unverifiedCerts',
                    action='store_true',
                    help='Allows transmission of https requests with self signed SSL certificates')
parser.add_argument('--authToken',
                    metavar='<token>',
                    type=str,
                    help='A token to transmit for authentication with an http request')
parser.add_argument('--verbosity', '-v',
                    metavar='<N>',
                    type=int,
                    default=0,
                    help='Set the verbosity level. "0" typically means no/minimal output. '
                         'Allows for more fine tuned output control as opposed to '
                         '"--quiet" that effectively silences everything')

# Insert a newline character before every optional argument in the usage string
# and remove the first line (which said "usage: pfurl [-h]").
OPTIONS_ON_LINES = '\n[--'.join(parser.format_usage().replace('\n', ' ').split('[--')[1:])
FULL_DESCRIPTION += indent(OPTIONS_ON_LINES, 16)
EXAMPLE = indent(EXAMPLE, 4)

# produce argparse's help section without the usage line
ARGS_HELP = parser.format_help().replace(parser.format_usage(), '\n')
ARGS_HELP = ARGS_HELP.replace('optional arguments:\n', '')
ARGS_HELP = F'\n    ARGS{ARGS_HELP}'
# don't indent args.help, argparse figures out the number of columns we can use


def print_version():
    parser.exit(1, f'Version: {VERSION}\n')


def print_short_description():
    print(FULL_DESCRIPTION)
    print(EXAMPLE)
    parser.exit(1)


def print_long_description():
    print(FULL_DESCRIPTION)
    print(ARGS_HELP)
    print(EXAMPLE)
    parser.exit(1)


def print_man_page(topic='commands'):
    page = man.DICTIONARY[topic]
    if not page:
        print(f'{Colors.RED}man page "{topic}" not found.{Colors.RESET}')
        parser.exit(1)
    print(page)
    parser.exit(0)
