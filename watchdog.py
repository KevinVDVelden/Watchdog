#!/bin/python
import easywatch
import sys
import os
from subprocess import call

if len( sys.argv ) < 3:
    print( 'Needs 2 arguments, directory to watch and a command to execute' )

path = sys.argv[1]
command = sys.argv[2:]

def run():
    call( command )

def onUpdate( action, filename ):
    if action not in ( 'created', 'modified' ):
        print( 'Skipping %s action on %s' % ( action, filename ) )
        return
    if not os.path.isfile( filename ):
        print( 'Skipping %s action on %s, is a directory' % ( action, filename ) )
        return
    
    basename = os.path.basename( filename )
    if basename[0] == '.':
        print( 'Skipping %s action on %s, starts with a .' % ( action, filename ) )
        return

    print( 'Updating for %s action on %s.' % ( action, filename ) )
    run()

run()
easywatch.watch( path, onUpdate )
