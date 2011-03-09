from nose.tools import raises

from compago import Command

class TestCommand(object):

    def test_target_instantiation(self):
        def target(a, b='bbb', c=True):
            '''Test Target'''
            return 'abc123'
        cmd = Command(target)
        assert cmd.target == target
        assert cmd.name == 'target'
        assert cmd.description == 'Test Target'
        res = cmd.target('fubar', b='babar', c=False)
        assert 'abc123' in res

    @raises(TypeError)
    def test_target_too_few_args(self):
        def target(a):
            pass
        cmd = Command(target)
        cmd.target()

    @raises(TypeError)
    def test_target_too_many_args(self):
        def target():
            pass
        cmd = Command(target)
        cmd.target('foo', 'bar')

    def test_parser(self):
        def target(a, b=2, c=False):
            pass
        cmd = Command(target)
        p = cmd.parser
        assert p.prog == cmd.name
        assert len(cmd.options) == 3

    def test_usage(self):
        def target(aaa, bbb=2, ccc=False):
            pass
        cmd = Command(target)
        u = cmd.usage
        print u
        assert 'aaa' in u
        assert '--bbb BBB' in u
        assert '-b BBB' in u
        assert '--ccc' in u
        assert '-ccc CCC' not in u
        assert '-c' in u
        assert '-c CCC' not in u

