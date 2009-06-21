#
# Simple tests, mostly borrowed from Lib/test/test_unicode.py
# With apologies to PEP 8
#

import datetime
d = datetime.date(2007, 8, 18)

class fooclass:
    bar = "baz"

# classes we'll use for testing
class C:
    def __init__(self, x=100):
        self._x = x
    def __format__(self, spec):
        return spec

class CX:
    def __init__(self, x=100):
        self._x = x
    def __format__(self, spec):
        return spec

class CY:
    def __init__(self, x=100):
        self._x = x
    def __format__(self, spec):
        return spec

class D:
    def __init__(self, x):
        self.x = x
    def __format__(self, spec):
        return str(self.x)

# class with __str__, but no __format__
class E:
    def __init__(self, x):
        self.x = x
    def __str__(self):
        return 'E(' + self.x + ')'

# class with __repr__, but no __format__ or __str__
class F:
    def __init__(self, x):
        self.x = x
    def __repr__(self):
        return 'F(' + self.x + ')'

# class with __format__ that forwards to string, for some format_spec's
class G:
    def __init__(self, x):
        self.x = x
    def __str__(self):
        return "string is " + self.x
    def __format__(self, format_spec):
        if format_spec == 'd':
            return 'G(' + self.x + ')'
        return object.__format__(self, format_spec)

# class that returns a bad type from __format__
class H:
    def __format__(self, format_spec):
        return 1.0

class I(datetime.date):
    def __format__(self, format_spec):
        return self.strftime(format_spec)

class J(int):
    def __format__(self, format_spec):
        return int.__format__(self * 2, format_spec)

def errorTuple(a, b, c):
    return (b, c, a)

tests = (
    ("{}", "foo", "foo"),
    ("{}", ("foo",), "foo"),
    ("{} {foo} {}", (1, dict(foo="bar")), IndexError),
    ("{} {foo} {}", (1, 2, dict(foo="bar")), "1 bar 2"),
    ('', (), ''),
    ('a', (), 'a'),
    ('ab', (), 'ab'),
    ('a{{', (), 'a{'),
    ('a}}', (), 'a}'),
    ('{{b', (), '{b'),
    ('}}b', (), '}b'),
    ('a{{b', (), 'a{b'),
    ("My name is {0}", ('Fred'), "My name is Fred"),
    ("My name is {0[name]}", (dict(name='Fred'), {}),
     "My name is Fred"),
    ("My name is {0} :-{{}}", ('Fred'),
     "My name is Fred :-{}"),
    ("The year is {0.year}", (d),
     "The year is 2007"),
    ('{0.bar}', fooclass(), "baz"),
    ('{foo._x}', dict(foo=CY(20)), '20'),

    ('', (), ''),
    ('abc', (), 'abc'),
    ('{0}', ('abc'), 'abc'),
    ('{0:}', ('abc'), 'abc'),
    ('X{0}', ('abc'), 'Xabc'),
    ('{0}X', ('abc'), 'abcX'),
    ('X{0}Y', ('abc'), 'XabcY'),
    ('{1}', (1, 'abc'), 'abc'),
    ('X{1}', (1, 'abc'), 'Xabc'),
    ('{1}X', (1, 'abc'), 'abcX'),
    ('X{1}Y', (1, 'abc'), 'XabcY'),
    ('{0}', (-15), '-15'),
    ('{0}{1}', (-15, 'abc'), '-15abc'),
    ('{0}X{1}', (-15, 'abc'), '-15Xabc'),
    ('{{', (), '{'),
    ('}}', (), '}'),
    ('{{}}', (), '{}'),
    ('{{x}}', (), '{x}'),
    ('{{{0}}}', (123), '{123}'),
    ('{{{{0}}}}', (), '{{0}}'),
    ('}}{{', (), '}{'),
    ('}}x{{', (), '}x{'),
    
    # weird field names
    ("{0[foo-bar]}", ({'foo-bar':'baz'}, {}), 'baz'),
    ("{0[foo bar]}", ({'foo bar':'baz'}, {}), 'baz'),
    ("{0[ ]}", ({' ':3}, {}), '3'),
    
    ('{foo._x}', dict(foo=C(20)), '20'),
    ('{1}{0}', (D(10), D(20)), '2010'),
    ('{0._x.x}', (C(D('abc'))), 'abc'),
    ('{0[0]}', (['abc', 'def']), 'abc'),
    ('{0[1]}', (['abc', 'def']), 'def'),
    ('{0[1][0]}', (['abc', ['def']]), 'def'),
    ('{0[1][0].x}', (['abc', [D('def')]]), 'def'),
    
    # strings
    ('{0:.3s}', ('abc'), 'abc'),
    ('{0:.3s}', ('ab'), 'ab'),
    ('{0:.3s}', ('abcdef'), 'abc'),
    ('{0:.0s}', ('abcdef'), ''),
    ('{0:3.3s}', ('abc'), 'abc'),
    ('{0:2.3s}', ('abc'), 'abc'),
    ('{0:2.2s}', ('abc'), 'ab'),
    ('{0:3.2s}', ('abc'), 'ab '),
    ('{0:x<0s}', ('result'), 'result'),
    ('{0:x<5s}', ('result'), 'result'),
    ('{0:x<6s}', ('result'), 'result'),
    ('{0:x<7s}', ('result'), 'resultx'),
    ('{0:x<8s}', ('result'), 'resultxx'),
    ('{0: <7s}', ('result'), 'result '),
    ('{0:<7s}', ('result'), 'result '),
    ('{0:>7s}', ('result'), ' result'),
    ('{0:>8s}', ('result'), '  result'),
    ('{0:^8s}', ('result'), ' result '),
    ('{0:^9s}', ('result'), ' result  '),
    ('{0:^10s}', ('result'), '  result  '),
    # ('{0:10000}', ('a'), 'a' + ' ' * 9999),
    # ('{0:10000}', (''), ' ' * 10000),
    # ('{0:10000000}', (''), ' ' * 10000000),
    
    # format specifiers for user defined type
    ('{0:abc}', (C()), 'abc'),
    
    # !r, !s and !a coercions
    ('{0!s}', ('Hello'), 'Hello'),
    ('{0!s:}', ('Hello'), 'Hello'),
    ('{0!s:15}', ('Hello'), 'Hello          '),
    ('{0!s:15s}', ('Hello'), 'Hello          '),
    ('{0!r}', ('Hello'), "'Hello'"),
    ('{0!r:}', ('Hello'), "'Hello'"),
    ('{0!r}', (F('Hello')), 'F(Hello)'),
    ('{0!r}', ('\u0378'), "'\\u0378'"), # nonprintable
    ('{0!r}', ('\u0374'), "'\u0374'"),  # printable
    ('{0!r}', (F('\u0374')), 'F(\u0374)'),
    ('{0!a}', ('Hello'), "'Hello'"),
    ('{0!a}', ('\u0378'), "'\\u0378'"), # nonprintable
    ('{0!a}', ('\u0374'), "'\\u0374'"), # printable
    ('{0!a:}', ('Hello'), "'Hello'"),
    ('{0!a}', (F('Hello')), 'F(Hello)'),
    ('{0!a}', (F('\u0374')), 'F(\\u0374)'),

    # test fallback to object.__format__
    ('{0}', ({}, {}), '{}'),
    ('{0}', ([]), '[]'),
    ('{0}', ([1]), '[1]'),
    ('{0}', (E('data')), 'E(data)'),
    ('{0:^10}', (E('data')), ' E(data)  '),
    ('{0:^10s}', (E('data')), ' E(data)  '),
    ('{0:d}', (G('data')), 'G(data)'),
    ('{0:>15s}', (G('data')), ' string is data'),
    ('{0!s}', (G('data')), 'string is data'),

    ("{0:date: %Y-%m-%d}", (I(year=2007,
                              month=8,
                              day=27)),
     "date: 2007-08-27"),

    # test deriving from a builtin type and overriding __format__
    ("{0}", (J(10)), "20"),


    # string format specifiers
    ('{0:}', ('a'), 'a'),

    # computed format specifiers
    ("{0:.{1}}", ('hello world', 5), 'hello'),
    ("{0:.{1}s}", ('hello world', 5), 'hello'),
    ("{0:.{precision}s}", ('hello world', dict(precision=5)), 'hello'),
    ("{0:{width}.{precision}s}",
     ('hello world', dict(width=10, precision=5)), 'hello     '),
    ("{0:{width}.{precision}s}",
     ('hello world', dict(width='10', precision='5')), 'hello     '),

    ('{}', (10), '10'),
    ('{:5}', ('s'), 's    '),
    ('{!r}', ('s'), "'s'"),
    ('{._x}', (CX(10)), '10'),
    ('{[1]}', ([1, 2]), '2'),
    ('{[a]}', ({'a':4, 'b':2}, {}), '4'),
    ('a{}b{}c', (0, 1), 'a0b1c'),

    ('a{:{}}b', ('x', '^10'), 'a    x     b'),
    ('a{:{}x}b', (20, '#'), 'a0x14b'),

    # can mix and match auto-numbering and named
    ('{f}{}', (4, dict(f='test')), 'test4'),
    ('{}{f}', (4, dict(f='test')), '4test'),
    ('{:{f}}{g}{}', (1, 3, dict(g='g', f=2)), ' 1g3'),
    ('{f:{}}{}{g}', (2, 4, dict(f=1, g='g')), ' 14g'),




    # test various errors
    errorTuple(ValueError, '{', ()),
    errorTuple(ValueError, '}', ()),
    errorTuple(ValueError, 'a{', ()),
    errorTuple(ValueError, 'a}', ()),
    errorTuple(ValueError, '{a', ()),
    errorTuple(ValueError, '}a', ()),
    errorTuple(IndexError, '{0}', ()),
    errorTuple(IndexError, '{1}', ('abc')),
    errorTuple(KeyError,   '{x}', ()),
    errorTuple(ValueError, '}{', ()),
    errorTuple(ValueError, '{', ()),
    errorTuple(ValueError, '}', ()),
    errorTuple(ValueError, 'abc{0:{}', ()),
    errorTuple(ValueError, '{0', ()),
    errorTuple(IndexError, '{0.}', ()),
    errorTuple(ValueError, '{0.}', (0)),
    errorTuple(IndexError, '{0[}', ()),
    errorTuple(ValueError, '{0[}', ([])),
    errorTuple(KeyError,   '{0]}', ()),
    errorTuple(ValueError, '{0.[]}', (0)),
    errorTuple(ValueError, '{0..foo}', (0)),
    errorTuple(ValueError, '{0[0}', (0)),
    errorTuple(ValueError, '{0[0:foo}', (0)),
    errorTuple(KeyError,   '{c]}', ()),
    errorTuple(ValueError, '{{ {{{0}}', (0)),
    errorTuple(ValueError, '{0}}', (0)),
    errorTuple(KeyError,   '{foo}', (dict(bar=3), {})),
    errorTuple(ValueError, '{0!x}', (3)),
    errorTuple(ValueError, '{0!}', (0)),
    errorTuple(ValueError, '{0!rs}', (0)),
    errorTuple(ValueError, '{!}', ()),
    errorTuple(IndexError, '{:}', ()),
    errorTuple(IndexError, '{:s}', ()),
    errorTuple(IndexError, '{}', ()),

    # issue 6089
    errorTuple(ValueError, '{0[0]x}', ([None])),
    errorTuple(ValueError, '{0[0](10)}', ([None])),

    # can't have a replacement on the field name portion
    errorTuple(TypeError, '{0[{1}]}', ('abcdefg', 4)),

    # exceed maximum recursion depth
    errorTuple(ValueError, '{0:{1:{2}}}', ('abc', 's', '')),
    errorTuple(ValueError,
               '{0:{1:{2:{3:{4:{5:{6}}}}}}}',
               (0, 1, 2, 3, 4, 5, 6, 7)),
    errorTuple(ValueError, '{0:-s}', ('')),

    # can't mix and match numbering and auto-numbering
    errorTuple(ValueError, '{}{1}', (1, 2)),
    errorTuple(ValueError, '{1}{}', (1, 2)),
    errorTuple(ValueError, '{:{1}}', (1, 2)),
    errorTuple(ValueError, '{0:{}}', (1, 2)),
)
tests = [test for test in tests if test]

success = 0
counter = 1
for test in tests:
    try:
        print("** test %d of %d" % (counter, len(tests)))
        print(">>> %s" % str(test))
        a = test[0] @ test[1]
        b = test[2]
        if a == b:
            print("==> %s" % a)
            success += 1
        else:
            print("XXX %s != %s" % (a, b))
    except Exception as e:
        if type(e) == test[2]:
            print("==> %s: %s" % (e.__class__.__name__, e))
            success += 1
        else:
            print("!!! %s: %s" % (e.__class__.__name__, e))
    print("")
    counter += 1

print("=" * 70)
print("%d out of %d = %.02f%%"
      % (success,
         len(tests),
         float(success) / len(tests) * 100.))
