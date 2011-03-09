import os, os.path

import compago

app = compago.Application()
command = app.command


@command
def list_files(path, verbose=False):
    if verbose:
        for dirpath, dirnames, filenames in os.walk(path):
            print dirpath
            for filename in filenames:
                print '    %s' % filename
    else:
        print '\n'.join(os.listdir(path))

@command
def cleanup_pyc(path, verbose=False):
    if verbose: print 'Removing files:'
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith('.pyc'):
                f = os.path.join(dirpath, filename)
                if verbose: print '  %s' % f
                os.unlink(f)


if __name__ == '__main__': app.run()