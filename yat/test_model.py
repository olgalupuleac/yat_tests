from model import *
import pytest
import sys
from io import StringIO


def get_value(number):
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    Print(number).evaluate(Scope())
    res = int(sys.stdout.getvalue())
    sys.stdout = old_stdout
    return res


class TestPrint():

    def test_print_number(self, monkeypatch):
        monkeypatch.setattr(sys, "stdout", StringIO())
        Print(Number(42)).evaluate(Scope())
        assert sys.stdout.getvalue() == "42\n"

    def test_print_reference(self, monkeypatch):
        monkeypatch.setattr(sys, "stdout", StringIO())
        scope = Scope()
        scope['x'] = Number(11)
        Print(Reference('x')).evaluate(scope)
        assert sys.stdout.getvalue() == "11\n"

    def test_get_value(self):
        assert get_value(Print(Number(78)).evaluate(Scope())) == 78


class TestNumber():

    def test_number(self):
        assert get_value(Number(56)) == 56


class TestOperations():

    def test_add(self):
        add = get_value(BinaryOperation(
            Number(5), '+', Number(2)).evaluate(Scope()))
        assert add == 7

    def test_sub(self):
        sub = get_value(BinaryOperation(
            Number(5), '-', Number(2)).evaluate(Scope()))
        assert sub == 3

    def test_neg(self):
        positive = get_value(UnaryOperation('-', Number(5)).evaluate(Scope()))
        assert positive == -5
        zero = get_value(UnaryOperation('-', Number(0)).evaluate(Scope()))
        assert zero == 0
        negative = get_value(UnaryOperation('-', Number(-9)).evaluate(Scope()))
        assert negative == 9

    def test_mult(self):
        mult = get_value(BinaryOperation(Number(7), '*', Number(-2)
                                         ).evaluate(Scope()))
        assert mult == -14

    def test_exact_div(self):
        div = get_value(BinaryOperation(
            Number(8), '/', Number(-2)).evaluate(Scope()))
        assert div == -4

    def test_div_with_rem(self):
        div = get_value(BinaryOperation(
            Number(9), '/', Number(5)).evaluate(Scope()))
        assert div == 1

    def test_mod(self):
        mod = get_value(BinaryOperation(
            Number(8), '%', Number(5)).evaluate(Scope()))
        assert mod == 3

    def test_div_and_mod(self):
        div = get_value(BinaryOperation(Number(-11), '/', Number(5)
                                        ).evaluate(Scope()))
        mod = get_value(BinaryOperation(Number(-11), '%', Number(5)
                                        ).evaluate(Scope()))
        assert -11 == 5 * div + mod

    def test_less_true(self):
        less = get_value(BinaryOperation(Number(1),
                                         '<',
                                         Number(2)).evaluate(Scope()))
        assert less != 0

    def test_gr_or_eql_true(self):
        gr_or_eql = get_value(BinaryOperation(Number(2),
                                              '>=',
                                              Number(1)).evaluate(Scope()))
        assert gr_or_eql != 0

    def test_less_or_eql_true(self):

        less_or_eql = get_value(BinaryOperation(Number(2),
                                                '<=',
                                                Number(2)).evaluate(Scope()))
        assert less_or_eql != 0

    def test_greater_true(self):

        greater = get_value(BinaryOperation(Number(4),
                                            '>',
                                            Number(2)).evaluate(Scope()))
        assert greater != 0

    def test_not_eql_true(self):

        not_eql = get_value(BinaryOperation(Number(1),
                                            '!=',
                                            Number(2)).evaluate(Scope()))
        assert not_eql != 0

    def test_eql_true(self):

        eql = get_value(BinaryOperation(Number(1),
                                        '==',
                                        Number(1)).evaluate(Scope()))
        assert eql != 0

    def test_bool_and_true(self):

        bool_and = get_value(BinaryOperation(Number(8),
                                             '&&',
                                             Number(1)).evaluate(Scope()))
        assert bool_and != 0

    def test_bool_or_true(self):

        bool_or = get_value(BinaryOperation(Number(-5),
                                            '||',
                                            Number(0)).evaluate(Scope()))
        assert bool_or != 0

    def test_bool_not_true(self):

        bool_not = get_value(UnaryOperation('!',
                                            Number(0)).evaluate(Scope()))
        assert bool_not != 0

    def test_less_false(self):

        less = get_value(BinaryOperation(Number(2),
                                         '<',
                                         Number(1)).evaluate(Scope()))
        assert less == 0

    def test_gr_or_eql_false(self):

        gr_or_eql = get_value(BinaryOperation(Number(1),
                                              '>=',
                                              Number(3)).evaluate(Scope()))
        assert gr_or_eql == 0

    def test_less_or_eql_false(self):

        less_or_eql = get_value(BinaryOperation(Number(7),
                                                '<=',
                                                Number(2)).evaluate(Scope()))
        assert less_or_eql == 0

    def test_greater_false(self):

        greater = get_value(BinaryOperation(Number(4),
                                            '>',
                                            Number(6)).evaluate(Scope()))
        assert greater == 0

    def test_not_eql_false(self):

        not_eql = get_value(BinaryOperation(Number(1),
                                            '!=',
                                            Number(1)).evaluate(Scope()))
        assert not_eql == 0

    def test_eql_false(self):

        eql = get_value(BinaryOperation(Number(1),
                                        '==',
                                        Number(8)).evaluate(Scope()))
        assert eql == 0

    def test_bool_and_false(self):

        bool_and = get_value(BinaryOperation(Number(8),
                                             '&&',
                                             Number(0)).evaluate(Scope()))
        assert bool_and == 0

    def test_bool_or_false(self):

        bool_or = get_value(BinaryOperation(Number(0),
                                            '||',
                                            Number(0)).evaluate(Scope()))
        assert bool_or == 0

    def test_bool_not_false(self):

        bool_not = get_value(UnaryOperation('!',
                                            Number(7)).evaluate(Scope()))
        assert bool_not == 0


class TestScope():

    def test_simple(self):
        scope = Scope()
        scope['a'] = Number(10)
        assert get_value(scope['a']) == 10

    def test_scope_function(self):
        scope = Scope()
        foo = Function([], [])
        FunctionDefinition(
            'a', foo).evaluate(scope)
        assert scope['a'] is foo

    def test_scope_get_item_from_parent(self):
        parent = Scope()
        parent['b'] = Number(10)
        scope = Scope(parent)
        assert get_value(scope['b']) == 10

    def test_scope_parent_diff_item_same_name(self):
        parent = Scope()
        parent['b'] = Number(10)
        scope = Scope(parent)
        scope['b'] = Number(20)
        assert get_value(scope['b']) == 20
        assert get_value(parent['b']) == 10

    def test_scope_set_item_in_parent(self):
        parent = Scope()
        parent['b'] = Number(10)
        scope = Scope(parent)
        parent['b'] = Number(20)
        assert get_value(scope['b']) == 20


class TestReference():

    def test_reference_number(self):
        scope = Scope()
        scope['name'] = Number(7)
        assert get_value(Reference('name').evaluate(scope)) == 7

    def test_reference_function(self):
        scope = Scope()
        foo = Function([], [])
        FunctionDefinition('name', foo).evaluate(scope)
        assert Reference('name').evaluate(scope) is foo


class TestRead():

    def test_read(self, monkeypatch):
        scope = Scope()
        monkeypatch.setattr(sys, "stdin", StringIO("7"))
        Read('x').evaluate(scope)
        assert get_value(Reference('x').evaluate(scope)) == 7


class TestConditional():

    def test_if(self):
        assert 1 == get_value(Conditional(BinaryOperation(
            Number(2),
            '<=',
            Number(4)
        ), [Number(1)],
            [Number(0)]).evaluate(Scope()))

    def test_else(self):
        assert 0 == get_value(Conditional(BinaryOperation(
            Number(2),
            '<=',
            Number(0)
        ), [Number(1)],
            [Number(0)]).evaluate(Scope()))

    def test_empty_if(self):
        Conditional(BinaryOperation(
            Number(2),
            '<=',
            Number(4)
        ), [],
            []).evaluate(Scope())

    def test_empty_else(self):
        Conditional(BinaryOperation(
            Number(2),
            '<=',
            Number(0)
        ), [],
            []).evaluate(Scope())

    def test_none_if(self):
        Conditional(BinaryOperation(
            Number(2),
            '<=',
            Number(4)
        ), None,
            []).evaluate(Scope())

    def test_none_else(self):
        Conditional(BinaryOperation(
            Number(2),
            '<=',
            Number(0)
        ), [],
            None).evaluate(Scope())

    def test_two_elements_in_if_list(self):
        assert 1 == get_value(Conditional(BinaryOperation(
            Number(2),
            '<=',
            Number(4)
        ), [Number(8),
            Number(1)],
            [Number(0)]).evaluate(Scope()))


class TestFunction():

    def test_simple_func_without_args(self):
        scope = Scope()
        foo = Function([], [Number(4)])
        FunctionDefinition('foo', foo).evaluate(scope)
        assert scope['foo'] is foo
        assert 4 == get_value(FunctionCall(FunctionDefinition(
            'foo', foo), []).evaluate(scope))

    def test_two_elements_in_func_body(self):
        scope = Scope()
        foo = Function([], [Number(4), Number(-9)])
        FunctionDefinition('foo', foo).evaluate(scope)
        assert -9 == get_value(FunctionCall(FunctionDefinition(
            'foo', foo), []).evaluate(scope))

    def test_func_with_args(self):
        assert 12 == get_value(FunctionCall(
            FunctionDefinition('foo',
                               Function(['x'], [
                                   BinaryOperation(
                                       Reference('x'), '+', Number(5))])), [
                Number(7)]).evaluate(Scope()))

    def test_func_in_func(self):
        scope = Scope()
        FunctionDefinition('foo',
                           Function([], [
                               FunctionDefinition('bar', Function([], [
                                   BinaryOperation(
                                       Number(67),
                                       '*',
                                       Number(283))
                               ]))
                           ])
                           ).evaluate(scope)
        assert 283 * \
            67 == get_value(FunctionCall(FunctionCall(Reference('foo'),
                                                      []), []).evaluate(scope))

    def test_empty_function(self):
        FunctionCall(FunctionDefinition('foo',
                                        Function(['x'], [])),
                     [Number(5)]).evaluate(Scope())
