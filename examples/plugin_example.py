import compago

app = compago.Application()

@app.command
def test_command(name):
    app.logger.error('Yes! This is logging at its finest!')
    app.logger.info(app.config['TEST_OPTION'])

if __name__ == '__main__':
    app.run()
