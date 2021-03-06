#!/bin/python
from __future__ import print_function
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
parser.add_argument( '--skip-filename', dest='skip_filename', help='Glob compared to the filename.', action='append' )
parser.add_argument( '--skip-regex', dest='skip_regex', help='Regex compared to the entire (relative) path', action='append' )
parser.add_argument( '--run-relative', dest='run_relative', help='Run the command in the watched directory', action='store_true' )
parser.add_argument( '--run-wait-time', dest='run_wait_time', help='After running, ignore events for this many seconds (default 2)' )

parser.add_argument( '--prefix', dest='print_prefix', help='Prefix for information log.' )

parser.add_argument( '--no-color', dest='color', action='store_false' )

parser.add_argument( '--skip-color', dest='skipcolor' )
parser.add_argument( '--start-color', dest='startcolor' )
parser.add_argument( '--done-color', dest='donecolor' )

parser.set_defaults( skip_dot=True, skip_directory=True, actions=['created', 'modified'], initial_run=False, run_wait_time=2.0, run_relative=False, color=True, skipcolor='blue', startcolor='green', donecolor='cyan', print_prefix='>>> ' )

args = parser.parse_args()
skip_regexes = []
float(args.run_wait_time)

if args.skip_dot:
    skip_regexes.append( ( re.compile( '.*/\..*' ), 'starts with a dot' ) )

if args.skip_filename is not None:
    for n in args.skip_filename:
        _regex = re.compile( '^./*' + n.replace( '*', '.*' ) )
        skip_regexes.append( ( _regex, 'matches filename "%s"' % n ) )
if args.skip_regex is not None:
    for n in args.skip_regex:
        _regex = re.compile( n )
        skip_regexes.append( ( _regex, 'matches regex "%s"' % n ) )

#Color text
def print_prefix( n ):
    return args.print_prefix + n

if args.color:
    try:
        from termcolor import cprint
        print_skip = lambda n: cprint( print_prefix( n ), args.skipcolor )
        print_start = lambda n: cprint( print_prefix( n ), args.startcolor )
        print_done = lambda n: cprint( print_prefix( n ), args.donecolor )
    except:
        print( 'Error during loading of colors, continuing without them' )
        args.color = False

if not args.color:
    print_skip = lambda n: print( print_prefix( n ) )
    print_start = lambda n: print( print_prefix( n ) )
    print_done = lambda n: print( print_prefix( n ) )

#Watchdog code
def run():
    if args.run_relative:
        call( args.command, cwd=args.path )
    else:
        call( args.command )

import time
nextRunTime = time.time()

def onUpdate( action, filename ):
    global nextRunTime
    if time.time() - nextRunTime < 0:
        print_skip( 'Skipping %s action on %s, timeout from last run (%.02f)' % ( action, filename, nextRunTime - time.time() ) )
        return

    if action not in args.actions:
        print_skip( 'Skipping %s action on %s' % ( action, filename ) )
        return

    if args.skip_directory and not os.path.isfile( filename ):
        print_skip( 'Skipping %s action on %s, is a directory' % ( action, filename ) )
        return
    
    for n in skip_regexes:
        regex, reason = n

        if regex.match( filename ):
            print_skip( 'Skipping %s action on %s, %s' % ( action, filename, reason ) )
            return

    print_start( 'Updating for %s action on %s.' % ( action, filename ) )
    run()
    nextRunTime = time.time() + float(args.run_wait_time)
    print_done( 'Done running command.' )

if args.initial_run:
    print_start( 'Doing initial run.' )
    run()
    print_done( 'Beginning with watching.' )

easywatch.watch( args.path, onUpdate )
