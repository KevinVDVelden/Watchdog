#!/bin/python
import easywatch
import argparse
import os
from subprocess import call


### Argument parsing
parser = argparse.ArgumentParser( description='Watches a directory for changes and executes a command.' )
parser.add_argument( 'path', help='Path to watch for changes.' )
parser.add_argument( 'command', nargs=argparse.REMAINDER, help='Command to run when changes are detected, executed literally.' )
parser.add_argument( '--no-skip-dotfiles', dest='skip_dot', action='store_false', help='Trigger on files beginning with a dot.' )
parser.add_argument( '--no-skip-directory', dest='skip_directory', action='store_false', help='Trigger on directories.' )
parser.add_argument( '--initial-run', dest='initial_run', action='store_true', help='Do a run on startup, before setting up watching.' )
parser.add_argument( '--watch-actions', dest='actions', help='What actions to trigger on', choices=['created', 'modified', 'deleted'] )

parser.set_defaults( skip_dot=True, skip_directory=True, actions=['created', 'modified'], initial_run=False, run_relative=False )

args = parser.parse_args()
print( args )

#Watchdog code
def run():
    call( args.command )

def onUpdate( action, filename ):
    if action not in args.actions:
        print( 'Skipping %s action on %s' % ( action, filename ) )
        return

    if args.skip_directory and not os.path.isfile( filename ):
        print( 'Skipping %s action on %s, is a directory' % ( action, filename ) )
        return
    
    basename = os.path.basename( filename )
    if args.skip_dot and basename[0] == '.':
        print( 'Skipping %s action on %s, starts with a .' % ( action, filename ) )
        return

    print( 'Updating for %s action on %s.' % ( action, filename ) )
    run()

if args.initial_run:
    run()

easywatch.watch( args.path, onUpdate )
