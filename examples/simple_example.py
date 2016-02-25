# examples/simple_example.py - A simple compago example script.

# To try this example:
#   0. Make sure you have compago installed if you've just checked out
#      the sources. See README for details.
#   1. python ./simple_example.py --help
#   2. python ./simple_example.py do_something --help
#   3. python ./simple_example.py do_something

import compago


# First, make our application
app = compago.Application()


# Next, simply use the @app.command decorator to define a command
@app.command
def do_something():
    """This description will show up in the --help. Try it!"""
    print('Something is happening!')
    return 123


# Finally, tell the app to run
app.run()
