# Watchdog
Simple python watchdog using easywatch.

## Dependencies
Required: easywatch<br />
Optional: termcolor

## Usage
    usage: watchdog [-h] [--no-skip-dotfiles] [--no-skip-directory]
                    [--initial-run] [--watch-actions {created,modified,deleted}]
                    [--skip-filename SKIP_FILENAME] [--skip-regex SKIP_REGEX]
                    [--run-relative] [--run-wait-time RUN_WAIT_TIME]
                    [--prefix PRINT_PREFIX] [--no-color] [--skip-color SKIPCOLOR]
                    [--start-color STARTCOLOR] [--done-color DONECOLOR]
                    path ...

    Watches a directory for changes and executes a command.

    positional arguments:
      path                  Path to watch for changes.
      command               Command to run when changes are detected, executed
                            literally.

    optional arguments:
      -h, --help            show this help message and exit
      --no-skip-dotfiles    Trigger on files beginning with a dot.
      --no-skip-directory   Trigger on directories.
      --initial-run         Do a run on startup, before setting up watching.
      --watch-actions {created,modified,deleted}
                            What actions to trigger on
      --skip-filename SKIP_FILENAME
                            Glob compared to the filename.
      --skip-regex SKIP_REGEX
                            Regex compared to the entire (relative) path
      --run-relative        Run the command in the watched directory
      --run-wait-time RUN_WAIT_TIME
                            After running, ignore events for this many seconds
                            (default 2)
      --prefix PRINT_PREFIX
                            Prefix for information log.
      --no-color
      --skip-color SKIPCOLOR
      --start-color STARTCOLOR
      --done-color DONECOLOR
