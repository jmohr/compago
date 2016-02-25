![Compago][logo]

    Copyright: ©2016 Justin Mohr. See LICENSE for details.

Write polished command line applications in a fraction of the time.
Guaranteed, or double your money back!

Compago is a framework for simple command-line parsing in Python. Compago
provides a simple framework and set of decorators to allow you to quickly
and easily define a set of commands within a script. For those familiar with
Ruby's Thor, Compago fills a similar niche.

This project was inspired by the excellent Flask-Script extension for Flask,
but has been entirely rewritten to remove all Flask dependencies.

(see: http://packages.python.org/Flask-Script/)

Quick Start
-----------------------------------------------------------------------------

First, install compago with pip, or alternately fetch the sources from Github or PyPI.

    $ pip install compago

Then, create a python file named "mycommand.py" containing this:

    import compago

    app = compago.Application()

    @app.command
    def say_hello(to="world"):
        print("Hello there, %s" % to)

    if __name__ == '__main__':
        app.run()

Save the file, and run it thusly:

    $ python mycommand.py

For some more in-depth examples, see the /examples folder in the sources.

Background
-----------------------------------------------------------------------------

Why Compago?

We've all needed to whip up a quick command line script at some point. How
often have you wanted to wrap a quick five lines of Python in a script for
reuse? Perhaps your little script requires a few arguments to be passed in.
In the past, you've had a few options:

  - Quick and dirty: just hard code some global variables at the top of
    your script.
  - Better, but still messy: just directly pull in sys.argv
  - Best, but difficult: use optparse or argparse

If you'll be using the script often, option 1 can become a pain very quickly.
You have to open the file in a text editor every time you need to change the
values. And if you ever need to let someone else use the script, option 1 can
be a no-go.

Option 2 is pretty easy, but just directly using sys.argv can get out
of control very quickly if you need to pull in more than one command line
argument. And similar to using global variables, expecting other users to
always play nice with the command line args is just asking for trouble.

Using argparse and/or optparse is the most prudent option, but if your script
is just a few lines of code, setting up all of that boilerplate can add a ton
of overhead to your quick script.

With Compago, you have another option. With the use of some simple
decorators, Compago can introspect a function, and set up command line
arguments and defaults automagically.

For example, instead of importing optparse, and manually setting up each
option in an OptionParser, and then taking the output of that and feeding
it into your function, you can just define your function thusly:

myapp.py:

  @app.command
  def check_host(hostname, username='admin', password='testing123'):
      '''Do some stuff.'''
      print "Let's do some junk on %s as user %s." % (
          hostname, username)

Now, the function's arguments (hostname, username, password) will be
available as command line arguments to your script:

  $ ./myapp.py check_host localhost --username=root --password=testing234
  Let's do some junk on localhost as user root.
  $ ./myapp.py check_host host1.example.com
  Let's do some junk on host1.example.com as user admin.

That's it! No other nasty boilerplate required.

Installing Compago
-----------------------------------------------------------------------------

Use pip or easy_install:

  pip install compago
  easy_install compago

Boom. Done.

Or alternately, fetch the source from github:

  git clone https://github.com/jmohr/compago.git

Using Compago
-----------------------------------------------------------------------------

Starting a Compago script is as easy as importing the compago module, and
creating a compago.Application object.

  import compago

  app = compago.Application()

An Application has one primary attribute, a name. By default, this will just
be the name of the script (sys.argv[0]), but you can override this if needed.
The name will be shown in the help.

Commands and Options
-----------------------------------------------------------------------------

After you create the application, you need to define some commands. A command
will be accessible for the user to call on the command line. For example, in
the Quick Start example above, the "check_host" function is a command. You
can define as many commands as you want in your script.

The @app.command decorator is pretty straight forward in its usage. Simply
decorate a function (with or without arguments), and the function will then
be available as a "command" on the command line.

Function arguments without a default defined will be "positional" or
"required" arguments on the command line. For example, in the check_host
example above, the "hostname" argument is required on the command line.

If you provide a default for your function argument, it will be an option
on the command line. For example:

  @myapp.command
  def mycommand(say="Hello", name="John Doe"):
    print "%s, %s." % (say, name)

In that example, the arguments "say" and "name" will be available as options
on the command line:

  python myapp.py --say="What up" --name="Justin Beiber"
  or
  python myapp.py -s "Goodbye" -n "Dude"

If the options are not specified, the defaults will be used. One special
type of option exists, and that is a boolean option:

  @myapp.command
  def mycommand(debug=False):
    if debug:
      print "Lots of great debugging info..."
    else:
      print "Terse. Very terse."

In this example, the "debug" option is a switch on the command line:

  python myapp.py --debug

If provided, debug will be set to True. No need to provide a value.

You can mix up the argument types, as well:

  @myapp.command
  def deploy(hostname, username="admin", verbose=True):
    result = ssh_to(hostname, username=username)
    if verbose: print result

It works as you'd expect.

Another decorator is available if you need more control over the options.
You can define one or more @option decorators on your function, and pass
in the same arguments that you would pass directly to argparse.ArgumentParser
to define an option. See it in action:

  @myapp.option('-x', '--execute', dest='command')
  @myapp.option('-U', '--user', dest='username')
  def run(command, username):
    with exec_user(username):
      call(command)

This also works about as you'd expect. One thing to note, if you decorate
your function with one or more @option decorators, there is no need to also
decorate it with @command. This will be done automatically.

Finally, adding help strings to your commands is super easy. Just put a
docstring in the function, and that string will be shown when the user
runs --help or -h on the command line. For example:

  @myapp.command
  def help_included():
    '''This command has some help.'''
    pass

When the user runs "python myapp.py --help", it will show the docstring next
to help_included. Try it!

Plugins
-----------------------------------------------------------------------------

Compago provides a simple plugin framework, which allows you to write your
own plugins to be used in your scripts. Two default plugins are provided,
and are turned on by default if you have the compago_plugins module
installed.

The default plugins are LoggingPlugin and ConfigPlugin. LoggingPlugin
provides access to Python's logging infrastructure from within your commands.
For example:

  @myapp.command
  def test_command(name):
    myapp.logger.info('Hello, {0}!'.format(name))

This command will log an INFO message to myapp.py.log (or whatever your
script is called). By default, logging will not occur unless you call your
script with the --log option:

  $ python myapp.py --log test_command Justin

You can also specify --logfile, which will override the default location
of the log file.

  $ python myapp.py --log --logfile /var/log/myapp.log test_command Justin

The second default plugin is the ConfigPlugin. This allows you to read
config vars from a YAML formatted config file (default location:
./myapp.py.conf). This location can be overridden by specifying the
--configfile option on the command line.

Any config variables defined in the config file are available within your
commands as myapp.config['YOUR_KEY']. For example, say you have a config file
named /etc/myapp.conf:

  YOUR_NAME: Justin
  YOUR_EMAIL: justin@example.org
  YOUR_BACON_LEVELS:
    -low
    -medium
    -high

And you call your script thusly:

  $ python myapp.py --configfile /etc/myapp.conf

Then, within your commands, you can fetch these config variables:

  @myapp.command
  def test_command():
    print myapp.config['YOUR_NAME']
    # ... etc ...

You can disable plugins by overriding Application.default_plugins before
instantiating your Application:

  from compago import Application
  Application.default_plugins = []

  myapp = Application()

  # ... etc ...

### Writing your own plugins

You can write your own plugins easily. A plugin is a class that inherits
from compago.plugin.Plugin. It should override one or more of the hook
methods:

  after_application_init(application) - called just after the application is
                                        initialized
  before_command_run(application, command) - called before a command is run
  after_command_run(application, command) - called just after a command is run
  option_added(application, option) - called after an option is defined
  command_added(application, command) - called after a command is defined

For example, let's say we want a simple plugin that prints out the current
time before and after each command is run. Create a file time_plugin.py:

  from compago.plugin import Plugin
  from datetime import datetime

  class TimePlugin(Plugin):

    def before_command_run(self, application):
      print datetime.now()

    def after_command_run(self, application):
      print datetime.now()

Then, to use the plugin in your compago application:

  from compago import Application
  from time_plugin import TimePlugin

  myapp = Application()
  myapp.add_plugin(TimePlugin())

  @myapp.command
  def testing123():
    pass

  if __name__ == '__main__':
    myapp.run()

Simple as that!

FAQ
-----------------------------------------------------------------------------

Q: Why did you write Compago?

A: I really liked the way Thor and Flask-Script worked, and I wanted a
similar tool for my plain old Python scripts. And I had way to much time
on my hands.

Q: What does Compago mean?

A: According to Google Translate -- which is *never* wrong -- compago is
Latin for "joint" or "connection".

TODO
-----------------------------------------------------------------------------

  * Create more helper functions for fun stuff.

