#!/bin/python
import easywatch
import argparse
import os
import re
from subprocess import call


### Argument parsing
parser = argparse.ArgumentParser( description='Watches a directory for changes and executes a command.' )
parser.add_argument( 'path', help='Path to watch for changes.' )
parser.add_argument( 'command', nargs=argparse.REMAINDER, help='Command to run when changes are detected, executed literally.' )
parser.add_argument( '--no-skip-dotfiles', dest='skip_dot', action='store_false', help='Trigger on files beginning with a dot.' )
parser.add_argument( '--no-skip-directory', dest='skip_directory', action='store_false', help='Trigger on directories.' )
parser.add_argument( '--initial-run', dest='initial_run', action='store_true', help='Do a run on startup, before setting up watching.' )
parser.add_argument( '--watch-actions', dest='actions', help='What actions to trigger on', choices=['created', 'modified', 'deleted'] )
parser.add_argument( '--skip-filename', dest='skip_filename', help='Glob compared to the filename.', nargs='*' )
parser.add_argument( '--skip-regex', dest='skip_regex', help='Regex compared to the entire (relative) path', nargs='*' )
parser.add_argument( '--run-relative', dest='run_relative', help='Run the command in the watched directory', action='store_true' )

parser.set_defaults( skip_dot=True, skip_directory=True, actions=['created', 'modified'], initial_run=False, run_relative=False )

args = parser.parse_args()
skip_regexes = []

if args.skip_dot:
    skip_regexes.append( ( re.compile( '.*/\..*' ), 'starts with a dot' ) )

for n in args.skip_filename:
    _regex = re.compile( n.replace( '*', '.*' ) )
    skip_regexes.append( ( _regex, 'matches filename "%s"' % n ) )
for n in args.skip_regex:
    _regex = re.compile( n )
    skip_regexes.append( ( _regex, 'matches regex "%s"' % n ) )

#Watchdog code
def run():
    if args.run_relative:
        call( args.command, cwd=args.path )
    else:
        call( args.command )

def onUpdate( action, filename ):
    if action not in args.actions:
        print( 'Skipping %s action on %s' % ( action, filename ) )
        return

    if args.skip_directory and not os.path.isfile( filename ):
        print( 'Skipping %s action on %s, is a directory' % ( action, filename ) )
        return
    
    for n in skip_regexes:
        regex, reason = n

        if regex.match( filename ):
            print( 'Skipping %s action on %s, %s' % ( action, filename, reason ) )
            return

    print( 'Updating for %s action on %s.' % ( action, filename ) )
    run()

if args.initial_run:
    run()

easywatch.watch( args.path, onUpdate )
