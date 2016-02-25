import compago

app = compago.Application()
app.add_option('--debug', dest='debug', action='store_true', default=False)

if app.args['debug']:
    import logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)s: %(message)s')


@app.command
def simple():
    '''This is a simple command that takes no args.'''
    print 'Doing something simple!'


@app.command
def positional_args(one, two):
    '''This command takes two (required) positional arguments.'''
    # The "positional" arguments will be required. On the command line,
    # the user will call this command as:
    # complex_example.py positional_args <arg1> <arg2>
    print 'Positional args: one=%s, two=%s' % (one, two)


@app.command
def keyword_options(three='three', four=False):
    '''This command takes some keyword options.'''
    # Keyword arguments in your function def are parsed as --options on the
    # command line. For example, this command will be called thusly:
    # complex_example.py keyword_options --three=33333 --four
    # Note: keywords with boolean defaults will be toggle options
    print 'Options: three=%s, four=%s' % (three, four)


@app.command
def mix_and_match(name, greeting='Hello', yell=False):
    '''Mixing and matching positional args and keyword options.'''
    say = '%s, %s' % (greeting, name)
    if yell:
        print '%s!' % say.upper()
    else:
        print '%s.' % say


@app.option('-G', '--greeting', dest='greeting', default='Hello')
@app.option('--yell', dest='yell', action='store_true', default=False)
def option_decorator(name, greeting, yell):
    '''Same as mix_and_match, but using the @option decorator.'''
    # Use the @option decorator when you need more control over the
    # command line options.
    say = '%s, %s' % (greeting, name)
    if yell:
        print '%s!' % say.upper()
    else:
        print '%s.' % say


if __name__ == '__main__':
    app.run()
