from model import *
import pytest
import sys
from io import StringIO
from random import randint


class TestNumber():

    def test_number(self):
        n = randint(-50, 50)
        assert type(Number(n).value) == int
        assert Number(n).value == n


class TestOperations():

    def test_add(self):
        scope = Scope()
        add = BinaryOperation(Number(5), '+', Number(2)).evaluate(scope).value
        assert type(add) == int
        assert add == 7

    def test_sub(self):
        scope = Scope()
        sub = BinaryOperation(Number(5), '-', Number(2)).evaluate(scope).value
        assert type(sub) == int
        assert sub == 3

    def test_neg(self):
        scope = Scope()
        pos = UnaryOperation('-', Number(5)).evaluate(scope).value
        assert type(pos) == int
        assert pos == -5
        null = UnaryOperation('-', Number(0)).evaluate(scope).value
        assert type(null) == int
        assert null == 0
        neg = UnaryOperation('-', Number(-9)).evaluate(scope).value
        assert type(neg) == int
        assert neg == 9

    def test_mult(self):
        scope = Scope()
        mult = BinaryOperation(Number(7), '*', Number(-2)
                               ).evaluate(scope).value
        assert type(mult) == int
        assert mult == -14

    def test_div(self):
        scope = Scope()
        div = BinaryOperation(Number(8), '/', Number(-2)).evaluate(scope).value
        assert type(div) == int
        assert div == -4

    def test_mod(self):
        scope = Scope()
        mod = BinaryOperation(Number(8), '%', Number(5)).evaluate(scope).value
        assert type(mod) == int
        assert mod == 3

    def test_div_and_mod(self):
        scope = Scope()
        div = BinaryOperation(Number(-11), '/', Number(5)
                              ).evaluate(scope).value
        mod = BinaryOperation(Number(-11), '%', Number(5)
                              ).evaluate(scope).value
        assert -11 == 5 * div + mod

    def test_logical_ops_true(self):
        scope = Scope()
        less = BinaryOperation(Number(1),
                               '<',
                               Number(2)).evaluate(scope).value
        assert type(less) == int
        assert less == 1
        gr_or_eql = BinaryOperation(Number(2),
                                    '>=',
                                    Number(1)).evaluate(scope).value
        assert type(gr_or_eql) == int
        assert gr_or_eql == 1
        less_or_eql = BinaryOperation(Number(2),
                                      '<=',
                                      Number(2)).evaluate(scope).value
        assert type(less_or_eql) == int
        assert less_or_eql == 1
        greater = BinaryOperation(Number(4),
                                  '>',
                                  Number(2)).evaluate(scope).value
        assert type(greater) == int
        assert greater == 1
        not_eql = BinaryOperation(Number(1),
                                  '!=',
                                  Number(2)).evaluate(scope).value
        assert type(not_eql) == int
        assert not_eql == 1
        eql = BinaryOperation(Number(1),
                              '==',
                              Number(1)).evaluate(scope).value
        assert type(eql) == int
        assert eql == 1
        bool_and = BinaryOperation(Number(8),
                                   '&&',
                                   Number(1)).evaluate(scope).value
        assert type(bool_and) == int
        assert bool_and == 1
        bool_or = BinaryOperation(Number(-5),
                                  '||',
                                  Number(0)).evaluate(scope).value
        assert type(bool_or) == int
        assert bool_or != 0
        bool_not = UnaryOperation('!',
                                  Number(0)).evaluate(scope).value
        assert type(bool_not) == int
        assert bool_not == 1

    def test_logical_ops_false(self):
        scope = Scope()
        less = BinaryOperation(Number(2),
                               '<',
                               Number(1)).evaluate(scope).value
        assert type(less) == int
        assert less == 0
        gr_or_eql = BinaryOperation(Number(1),
                                    '>=',
                                    Number(3)).evaluate(scope).value
        assert type(gr_or_eql) == int
        assert gr_or_eql == 0
        less_or_eql = BinaryOperation(Number(7),
                                      '<=',
                                      Number(2)).evaluate(scope).value
        assert type(less_or_eql) == int
        assert less_or_eql == 0
        greater = BinaryOperation(Number(4),
                                  '>',
                                  Number(6)).evaluate(scope).value
        assert type(greater) == int
        assert greater == 0
        not_eql = BinaryOperation(Number(1),
                                  '!=',
                                  Number(1)).evaluate(scope).value
        assert type(not_eql) == int
        assert not_eql == 0
        eql = BinaryOperation(Number(1),
                              '==',
                              Number(8)).evaluate(scope).value
        assert type(eql) == int
        assert eql == 0
        bool_and = BinaryOperation(Number(8),
                                   '&&',
                                   Number(0)).evaluate(scope).value
        assert type(bool_and) == int
        assert bool_and == 0
        bool_or = BinaryOperation(Number(0),
                                  '||',
                                  Number(0)).evaluate(scope).value
        assert type(bool_or) == int
        assert bool_or == 0
        bool_not = UnaryOperation('!',
                                  Number(7)).evaluate(scope).value
        assert type(bool_not) == int
        assert bool_not == 0


class TestScopeAndRef():

    def test_scope(self):
        parent = Scope()
        parent['a'] = Function([], [])
        parent['b'] = Number(10)
        scope = Scope(parent)
        assert scope['b'].value == 10
        scope['b'] = Number(20)
        assert scope['b'].value == 20
        assert parent['b'].value == 10
        assert type(scope['a']) == Function
        scope['a'] = Number(0)
        assert scope['a'].value == 0
        assert type(parent['a']) == Function
        parent['c'] = Number(7)
        assert scope['c'].value == 7
        scope['d'] = Number(6)

    def test_reference(self):
        scope = Scope()
        scope['name'] = Number(7)
        assert Reference('name').evaluate(scope).value == 7
        FunctionDefinition('name', Function([], [])).evaluate(scope)
        assert type(Reference('name').evaluate(scope)) == Function


class TestReadAndPrint():

    def test_read(self, monkeypatch):
        monkeypatch.setattr(sys, "stdin", StringIO("7"))
        scope = Scope()
        assert type(Read('x').evaluate(scope)) == Number
        assert Reference('x').evaluate(scope).value == 7

    def test_print_number(self, monkeypatch):
        monkeypatch.setattr(sys, "stdout", StringIO())
        scope = Scope()
        assert type(Print(Number(42)).evaluate(scope)) == Number
        assert sys.stdout.getvalue() == "42\n"

    def test_print_reference(self, monkeypatch):
        monkeypatch.setattr(sys, "stdout", StringIO())
        scope = Scope()
        scope['x'] = Number(11)
        assert type(Print(Reference('x')).evaluate(scope)) == Number
        assert sys.stdout.getvalue() == "11\n"

    def test_print_print(self, monkeypatch):
        monkeypatch.setattr(sys, "stdout", StringIO())
        scope = Scope()
        Print(Print(Number(5))).evaluate(scope)
        assert sys.stdout.getvalue() == "5\n5\n"


class TestConditional():

    def test_if(self):
        scope = Scope()
        assert 1 == Conditional(BinaryOperation(
            Number(2),
            '<=',
            Number(4)
        ), [Number(1)],
            [Number(0)]).evaluate(scope).value

    def test_else(self):
        scope = Scope()
        assert 0 == Conditional(BinaryOperation(
            Number(2),
            '<=',
            Number(0)
        ), [Number(1)],
            [Number(0)]).evaluate(scope).value

    def test_empty_if(self):
        scope = Scope()
        Conditional(BinaryOperation(
            Number(2),
            '<=',
            Number(4)
        ), [],
            []).evaluate(scope)

    def test_empty_else(self):
        scope = Scope()
        Conditional(BinaryOperation(
            Number(2),
            '<=',
            Number(0)
        ), [],
            []).evaluate(scope)


class TestFunction():

    def test_simple_func_without_args(self):
        scope = Scope()
        FunctionDefinition('foo', Function([], [Number(4)])).evaluate(scope)
        assert type(scope['foo']) == Function
        res = FunctionCall(FunctionDefinition(
            'foo', Function([], [Number(4)])), []).evaluate(scope)
        assert res.value == 4

    def test_func_with_args(self):
        scope = Scope()
        assert 12 == FunctionCall(FunctionDefinition('foo', Function(['x'], [
            BinaryOperation(
                Reference('x'), '+', Number(5))])), [
            Number(7)]).evaluate(scope).value

    def test_func_in_func(self):
        scope = Scope()
        a = randint(-100, 100)
        b = randint(-100, 100)
        FunctionDefinition('foo',
                           Function([], [
                               FunctionDefinition('bar', Function([], [
                                   BinaryOperation(
                                       Number(a),
                                       '*',
                                       Number(b))
                               ]))
                           ])
                           ).evaluate(scope)
        assert a * \
            b == FunctionCall(FunctionCall(Reference('foo'),
                                           []), []).evaluate(scope).value

    def test_empty_function(self):
        scope = Scope()
        FunctionCall(FunctionDefinition('foo',
                                        Function(['x'], [])),
                     [Number(5)]).evaluate(scope)
