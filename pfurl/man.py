"""
Colorful documentation in the form of Python strings.
"""
from colorama import Fore as Colors, Style
from pfmisc import local_ip_address

LOCAL_IP_ADDRESS = local_ip_address()
EXAMPLE_HTTP = f'http://{LOCAL_IP_ADDRESS}:5005/api/v1/cmd'


_PUSHPATH = f'        {Colors.CYAN}{Style.BRIGHT}pushPath{Style.NORMAL}' \
               f'            {Colors.MAGENTA}push a filesystem path over HTTP.'

_PULLPATH = f'        {Colors.CYAN}{Style.BRIGHT}pullPath{Style.NORMAL}' \
               f'            {Colors.MAGENTA}pull a filesystem path over HTTP.'

_COMMANDS = f"""
This script/module provides CURL-based GET/PUT/POST communication over http
to a remote REST-like service: {Colors.GREEN}

     ./pfurl.py [--auth <username:passwd>] [--verb <GET/POST>]   \\
                --http <IP>[:<port>]</some/path/>

{Colors.WHITE}
Where --auth is an optional authorization to pass to the REST API,
--verb denotes the REST verb to use and --http specifies the REST URL.

Additionally, a 'message' described in JSON syntax can be pushed to the
remote service, in the following syntax:
{Colors.GREEN}
     pfurl     [--auth <username:passwd>] [--verb <GET/POST>]   \\
                --http <IP>[:<port>]</some/path/>               \\
               [--msg <JSON-formatted-string>]

{Colors.WHITE}
In the case of the 'pman' system this --msg flag has very specific
contextual syntax, for example:
{Colors.GREEN}

     pfurl      --verb POST --http {EXAMPLE_HTTP}--msg \\
                    '{{  "action": "run",
                        "meta": {{
                            "cmd":      "cal 7 1970",
                            "auid":     "rudolphpienaar",
                            "jid":      "<jid>-1",
                            "threaded": true
                        }}
                    }}'


{Colors.CYAN}

The following specific action directives are directly handled by script:

{_PUSHPATH}

{_PULLPATH}

{Colors.YELLOW}
To get detailed help on any of the above commands, type
{Colors.CYAN}

    ./pfurl.py --man <pushPath|pullPath>
{Colors.RESET}
"""

_PUSHPATH += f"""
{Colors.RESET}
This pushes a file over HTTP. The 'meta' dictionary
can be used to specify content specific information
and other information.

Note that the "file" server is typically *not* on the
same port as the `pman` process. Usually a prior call
must be made to `pman` to start a one-shot listener
on a given port. This port then accepts the file transfer
from the 'pushPath' method.

The "meta" dictionary consists of several nested
dictionaries. In particular, the "remote/path"
field can be used to suggest a location on the remote
filesystem to save the transmitted data. Successful
saving to this path depends on whether or not the
remote server process actually has permission to
write in that location.

{Colors.YELLOW}EXAMPLE:
{Colors.GREEN}

pfurl --verb POST --http {EXAMPLE_HTTP} --msg """ + r"""\
    '{  "action": "pushPath",
        "meta":
            {
                "local":
                    {
                        "path":         "/path/on/client"
                    },
                "remote":
                    {
                        "path":         "/path/on/server"
                    },
                "transport":
                    {
                        "mechanism":    "compress",
                        "compress": {
                            "archive":  "zip",
                            "unpack":   true,
                            "cleanup":  true
                        }
                    }
            }
    }'
""" + F"""
{Colors.YELLOW}ALTERNATE -- using copy/symlink:
{Colors.LIGHTGREEN_EX}

pfurl --verb POST --http {EXAMPLE_HTTP} --msg """ + r"""\
    '{  "action": "pushPath",
        "meta":
            {
                "local":
                    {
                        "path":         "/path/on/client"
                    },
                "remote":
                    {
                        "path":         "/path/on/server"
                    },
                "transport":
                    {
                        "mechanism":    "copy",
                        "copy": {
                            "symlink": true
                        }
                    }
            }
    }'
""" + Colors.RESET

_PULLPATH += f"""
{Colors.RESET}
This pulls data over HTTP from a remote server.
The 'meta' dictionary can be used to specify content
specific information and other detail.

Note that the "file" server is typically *not* on the
same port as a `pman` process. Usually a prior call
must be made to `pman` to start a one-shot listener
on a given port. This port then accepts the file transfer
from the 'pullPath' method.

The "meta" dictionary consists of several nested
dictionaries. In particular, the "remote/path"
field can be used to specify a location on the remote
filesystem to pull. Successful retrieve from this path
depends on whether or not the remote server process actually
has permission to read in that location.

{Colors.YELLOW}EXAMPLE -- using zip:
{Colors.GREEN}

pfurl --verb POST --http {EXAMPLE_HTTP} --msg """ + r"""\
    '{  "action": "pullPath",
        "meta":
            {
                "local":
                    {
                        "path":         "/path/on/client"
                    },
                "remote":
                    {
                        "path":         "/path/on/server"
                    },
                "transport":
                    {
                        "mechanism":    "compress",
                        "compress": {
                            "archive":  "zip",
                            "unpack":   true,
                            "cleanup":  true
                        }
                    }
            }
    }'
""" + f"""
{Colors.YELLOW}ALTERNATE -- using copy/symlink:
{Colors.LIGHTGREEN_EX}

pfurl --verb POST --http {EXAMPLE_HTTP} --msg """ + r"""\
    '{  "action": "pullPath",
        "meta":
            {
                "local":
                    {
                        "path":         "/path/on/client"
                    },
                "remote":
                    {
                        "path":         "/path/on/server"
                    },
                "transport":
                    {
                        "mechanism":    "copy",
                        "copy": {
                            "symlink": true
                        }
                    }
            }
    }'
""" + Colors.RESET

DICTIONARY = {
    'commands': _COMMANDS,
    'pushPath': _PUSHPATH,
    'pullPath': _PULLPATH
}
