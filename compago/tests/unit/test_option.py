from compago import Option


class TestOption(object):

    def test_args_kwargs(self):
        opt = Option('one', 2, three=3)
        assert 'one' in opt.args
        assert 2 in opt.args
        assert 'three' in opt.kwargs

    def test_repr(self):
        opt = Option('one')
        assert 'one' in repr(opt), 'Incorrect repr: %s' % repr(opt)
        opt = Option(one=1, two='two')
        assert 'one=1' in repr(opt), 'Incorrect repr: %s' % repr(opt)
        assert "two='two'" in repr(opt), 'Incorrect repr: %s' % repr(opt)
        opt = Option('one', 2, three=3)
        assert 'one' in repr(opt), 'Incorrect repr: %s' % repr(opt)
        assert '2' in repr(opt), 'Incorrect repr: %s' % repr(opt)
        assert 'three=3' in repr(opt), 'Incorrect repr: %s' % repr(opt)

    def test_unicode(self):
        opt = Option('one', 2, three=3)
        assert unicode(opt) == repr(opt)
        assert str(opt) == repr(opt)
