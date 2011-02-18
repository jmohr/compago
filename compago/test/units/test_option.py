from compago.option import Option

class TestOption(object):

    def test_option(self):
        o = Option('one', 'two', thing='three', another=4)
        assert o is not None
        assert 'one' in o.args
        assert 'two' in o.args
        assert 'thing' in o.kwargs
        assert 'another' in o.kwargs