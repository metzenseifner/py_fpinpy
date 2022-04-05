#!/usr/bin/env python3
#
# Copyright 2022 Jonathan L. Komar
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
import pytest
from hamcrest import *

from fpinpy import SinglyLinkedList, Nil, Cons
from fpinpy.result import Result, Failure, Success

class Test_Initialization:
    class Test_Cons:
        @pytest.mark.skip(reason="Not implemented yet. Probably using a metaclass.")
        def test_that_direct_construction_fails(self):
            assert_that(calling(Cons).with_args(1, SinglyLinkedList.list(2,3)), raises(RuntimeError))
        def test_factory_some(self):
            sut = SinglyLinkedList.list(1, 2, 3)
            assert_that(sut, instance_of(Cons))
        def test_factory_singleton(self):
            sut = SinglyLinkedList.list(1)
            assert_that(sut, instance_of(Cons))
    class Test_Nil:
        @pytest.mark.skip(reason="Not implemented yet. Probably using a metaclass.")
        def test_that_direct_construction_fails(self):
            assert_that(Nil, raises(RuntimeError))
        def test_factory(self):
            sut = SinglyLinkedList.list()
            assert_that(sut, instance_of(Nil))

class Test_head():
    class Test_Cons:
        def test_head(self):
            sut = SinglyLinkedList.list(1, 2, 3)
            assert_that(sut.head(), equal_to(1))
    class Test_Nil:
        def test_head(self):
            sut = SinglyLinkedList.list()
            assert_that(sut.head, raises(RuntimeError))

class Test_tail():
    class Test_Cons:
        def test_tail(self):
            sut = SinglyLinkedList.list(1, 2, 3)
            assert_that(sut.head(), equal_to(1))
    class Test_Nil:
        def test_tail(self):
            sut = SinglyLinkedList.list()
            assert_that(sut.tail, raises(RuntimeError))

class Test_isEmpty():
    class Test_Cons:
        def test_isEmpty_some_case(self):
            sut = SinglyLinkedList.list(1, 2, 3)
            assert_that(sut.isEmpty(), equal_to(False))
        def test_isEmpty_singleton_case(self):
            sut = SinglyLinkedList.list(1)
            assert_that(sut.isEmpty(), equal_to(False))
    class Test_Nil:
        def test_isEmpty_empty_case(self):
            sut = SinglyLinkedList.list()
            assert_that(sut.isEmpty(), equal_to(True))

class Test_str():
    class Test_Cons:
        def test_str_some(self):
            sut = str(SinglyLinkedList.list(1, 2, 3))
            assert_that(sut, equal_to("[1, 2, 3, NIL]"))
    class Test_Nil:
        def test_str(self):
            sut = str(SinglyLinkedList.list())
            assert_that(sut, equal_to("[NIL]"))

#class Test_repr():
#    class Test_Cons:
#        sut = repr(SinglyLinkedList.list(1, 2, 3))
#        assert_that(sut, equal_to("Cons(1, Cons(2, Cons(3, NIL)))"))
#    class Test_Nil:
#        sut = repr(SinglyLinkedList.list())
#        assert_that(sut, equal_to("Nil"))

class Test_setHead():
    class Test_Cons:
        def test_setHead_some_case(self):
            sut = SinglyLinkedList.list(1,2,3).setHead(4)
            assert_that(str(sut), equal_to("[4, 2, 3, NIL]"))
        def test_setHead_singleton_case(self):
            sut = SinglyLinkedList.list(1).setHead(4)
            assert_that(str(sut), equal_to("[4, NIL]"))
    class Test_Nil:
        def test_setHead_fails(self):
            sut = SinglyLinkedList.list()
            assert_that(calling(sut.setHead).with_args(4), raises(RuntimeError))

class Test_foldLeft():
    class Test_Cons:
        def test_foldLeft_some(self):
            sut = SinglyLinkedList.list(2, 3, 4).foldLeft(0, lambda x: lambda y: x + y)
            assert_that(sut, equal_to(9))
            sut = SinglyLinkedList.list(3, 4, 5).foldLeft(1, lambda x: lambda y: x * y)
            assert_that(sut, equal_to(60))
        def test_setHead_singleton_case(self):
            sut = SinglyLinkedList.list(1).foldLeft(0, lambda x: lambda y: x + y)
            assert_that(sut, equal_to(1))
        def test_foldLeft_singleton(self):
            sut = SinglyLinkedList.list(1).foldLeft(0, lambda x: lambda y: x + y)
            assert_that(sut, equal_to(1))
    class Test_Nil:
        def test_foldLeft_keeps_identity(self):
            sut = SinglyLinkedList.list().foldLeft(0, lambda x: lambda y: x + y)
            assert_that(str(sut), equal_to("0"))
        def test_foldLeft_keeps_identity(self):
            sut = SinglyLinkedList.list().foldLeft(0, lambda x: lambda y: x > y)
            assert_that(str(sut), equal_to("0"))

class Test_foldRight():
    class Test_Cons:
        def test_foldRight_commutative_operation_foldLeft_Equivalence_some(self):
            aux = SinglyLinkedList.list(2, 3, 4).foldLeft(0, lambda x: lambda y: x + y)
            sut = SinglyLinkedList.list(2, 3, 4).foldRight(0, lambda x: lambda y: x + y)
            assert_that(sut, equal_to(aux))
            assert_that(sut, equal_to(9))
        def test_foldRight_noncommutative_operation_foldLeft_Equivalence_some(self):
            op = SinglyLinkedList.cons
            # swap operands to: o(y,x) because foldLeft does <accumulator> <op> <leftmost operand> <op> <next operand> ...
            # The initial value of <accumulator is Nil, which we immediately want as tail <x> in cons(y, x).
            # The cons call looks like cons(y, [2, NIL]), yielding [3, 4, NIL]. And so forth...
            aux = SinglyLinkedList.list(2, 3, 4).foldLeft(SinglyLinkedList.list(), lambda x: lambda y: op(y, x))
            sut = SinglyLinkedList.list(2, 3, 4).foldRight(SinglyLinkedList.list(), lambda x: lambda y: op(x, y))
            assert_that(str(aux), equal_to("[4, 3, 2, NIL]"))
            assert_that(str(sut), equal_to("[2, 3, 4, NIL]"))
            assert_that(str(sut), equal_to(str(aux.reverse())))
        def test_foldRight_singleton(self):
            sut = SinglyLinkedList.list(2).foldLeft(0, lambda x: lambda y: x + y)
            assert_that(str(sut), equal_to("2"))
    class Test_Nil:
        def test_foldRight_keeps_identity(self):
            sut = SinglyLinkedList.list().foldLeft(0, lambda x: lambda y: x + y)
            assert_that(str(sut), equal_to("0"))

class Test_drop():
    class Test_Cons:
        def test_drop_some(self):
            sut = SinglyLinkedList.list(1,2,3).drop(2)
            assert_that(str(sut), equal_to('[3, NIL]'))
            assert_that(sut, instance_of(Cons))
        def test_drop_singleton(self):
            sut = SinglyLinkedList.list(1).drop(1)
            assert_that(str(sut), equal_to('[NIL]'))
            assert_that(sut, instance_of(Nil))
        def test_drop_too_many_yields_empty(self):
            sut = SinglyLinkedList.list(1).drop(2)
            assert_that(str(sut), equal_to('[NIL]'))
            assert_that(sut, instance_of(Nil))
    class Test_Nil:
        def test_drop_one(self):
            sut = SinglyLinkedList.list().drop(1)
            assert_that(str(sut), equal_to('[NIL]'))
        def test_drop_two(self):
            sut = SinglyLinkedList.list().drop(2)
            assert_that(str(sut), equal_to('[NIL]'))

class Test_filter():
    class Test_Cons:
        def test_filter_some(self):
            sut = SinglyLinkedList.list(1,2,3,4).filter(lambda h: h > 2)
            assert_that(str(sut), equal_to('[3, 4, NIL]'))
        def test_filter_singleton(self): # TODO
            pass
    class Test_Nil:
        def test_filter(self): # TODO
            pass

class Test_forEach():
    class Test_Cons:
        def test_forEach_some(self):
            sut = None
            def effect(x):
                nonlocal sut
                sut = x
            SinglyLinkedList.list(1,2,3,4).forEach(effect)
            assert_that(sut, equal_to(4))
        def test_forEach_singleton(self):
            sut = None
            def effect(x):
                nonlocal sut
                sut = x
            SinglyLinkedList.list(2).forEach(effect)
            assert_that(sut, equal_to(2))
    class Test_Nil:
        def test_forEach_singleton(self):
            sut = None
            def effect(x):
                nonlocal sut
                sut = x
            SinglyLinkedList.list().forEach(effect)
            assert_that(sut, equal_to(None))

class Test_map():
    class Test_Cons:
        def test_map_some(self):
            sut = SinglyLinkedList.list(2, 3).map(lambda x: x * 2)
            assert_that(str(sut), equal_to('[4, 6, NIL]'))
        def test_map(singleton):
            sut = SinglyLinkedList.list(2).map(lambda x: x * 2)
            assert_that(str(sut), equal_to('[4, NIL]'))
    class Test_Nil:
        def test_map(self):
            sut = SinglyLinkedList.list().map(lambda x: x * 2)
            assert_that(str(sut), equal_to('[NIL]'))

class Test_reverse():
    class Test_Cons:
        def test_reverse_some(self):
            sut = SinglyLinkedList.list(1, 2, 3).reverse()
            assert_that(str(sut), equal_to('[3, 2, 1, NIL]'))
        def test_reverse_singleton(self):
            sut = SinglyLinkedList.list(1).reverse()
            assert_that(str(sut), equal_to('[1, NIL]'))
    class Test_Nil:
        def test_reverse(self):
            sut = SinglyLinkedList.list().reverse()

class Test_length():
    class Test_Cons:
        def test_length_some(self):
            sut = SinglyLinkedList.list(1, 2, 3).length()
            assert_that(sut, equal_to(3))
        def test_length_singleton(self):
            sut = SinglyLinkedList.list(2).length()
            assert_that(sut, equal_to(1))
    class Test_Nil:
        def test_length(self):
            sut = SinglyLinkedList.list().length()
            assert_that(sut, equal_to(0))

class Test_SinglyLinkedListIterator:
    class Test_Forward:
        def test_forward_some(self):
            sut = iter(SinglyLinkedList.list(1, 2, 3))
            assert_that(next(sut), equal_to(1))
            assert_that(next(sut), equal_to(2))
            assert_that(next(sut), equal_to(3))
            assert_that(calling(next).with_args(sut), raises(StopIteration))
    class Test_Backward:
        def test_backward_some(self):
            sut = reversed(SinglyLinkedList.list(1, 2, 3))
            assert_that(next(sut), equal_to(3))
            assert_that(next(sut), equal_to(2))
            assert_that(next(sut), equal_to(1))
            assert_that(calling(next).with_args(sut), raises(StopIteration))

class Test_traverse:
    # TODO Expand tests to include all cases. sequence was considered more important.
    class Test_static:
        def test_traverse_some(self):
            sut = SinglyLinkedList.traverse(SinglyLinkedList.list(1, 2, 3), lambda x: Result.of(x + 1))
            assert_that(str(sut), equal_to("Result([2, 3, 4, NIL])"))
        def test_traverse_singleton(self):
            sut = SinglyLinkedList.traverse(SinglyLinkedList.list(2), lambda x: Result.of(x + 1))
            assert_that(str(sut), equal_to("Result([3, NIL])"))
        def test_traverse_empty(self):
            sut = SinglyLinkedList.traverse(SinglyLinkedList.list(), lambda x: Result.of(x + 1))
            assert_that(str(sut), equal_to("Result([NIL])"))

class Test_sequence:
    class Test_static:
        def test_sequence_some_when_contains_failure(self):
            sut = SinglyLinkedList.sequence(
                SinglyLinkedList.list(Result.of(1), 
                Result.failure(RuntimeError(2)), 
                Result.of(3)))
            assert_that(sut, instance_of(Failure))
        def test_sequence_some_when_contains_empty(self):
            sut = SinglyLinkedList.sequence(
                SinglyLinkedList.list(Result.of(1), 
                Result.empty(), 
                Result.of(3)))
            assert_that(sut, instance_of(Failure))
        def test_sequence_singleton(self):
            sut = SinglyLinkedList.sequence(SinglyLinkedList.list(Result.of(1)))
            assert_that(str(sut), equal_to("Result([1, NIL])"))
        def test_sequence_empty(self):
            sut = SinglyLinkedList.sequence(SinglyLinkedList.list())
            assert_that(str(sut), equal_to("Result([NIL])"))

class Test_flattenResult:
    class Test_Cons:
        def test_flattenResult_some(self):
            sut = SinglyLinkedList.flattenResult(SinglyLinkedList.list(Result.of(1), Result.empty(), Result.failure(2), Result.of(3)))
            assert_that(str(sut), equal_to("[1, [NIL], [NIL], 3, NIL]"))
    class Test_Nil:
        def test_flattenResult(self):
            sut = SinglyLinkedList.flattenResult(SinglyLinkedList.list())
            assert_that(str(sut), equal_to("[NIL]"))

class Test_flatten:
    def test_flatten_some_with_some(self):
        sut = SinglyLinkedList.flatten(SinglyLinkedList.list(SinglyLinkedList.list(1,2,3), SinglyLinkedList.list(4,5,6)))
        assert_that(str(sut), equal_to("[1, 2, 3, 4, 5, 6, NIL]"))
    def test_flatten_some_with_none(self):
        sut = SinglyLinkedList.flatten(SinglyLinkedList.list(SinglyLinkedList.list(1,2,3), SinglyLinkedList.list()))
        assert_that(str(sut), equal_to("[1, 2, 3, NIL]"))
    def test_flatten_none_with_some(self):
        sut = SinglyLinkedList.flatten(SinglyLinkedList.list(SinglyLinkedList.list(), SinglyLinkedList.list(4,5,6)))
        assert_that(str(sut), equal_to("[4, 5, 6, NIL]"))

class Test_flatMap:
    def test_flatMap(self):
        sut = SinglyLinkedList.list(1,2,3).flatMap(lambda a: SinglyLinkedList.list(a, -a))
        assert_that(str(sut), equal_to("[1, -1, 2, -2, 3, -3, NIL]"))

class Test_toPyList:
    class Test_Cons:
        def test_toPyList_some(self):
            sut = SinglyLinkedList.list(1,2,3).toPyList()
            assert_that(sut, equal_to([1,2,3]))
        def test_toPyList_singleton(self):
            sut = SinglyLinkedList.list(1).toPyList()
            assert_that(sut, equal_to([1]))
    class Test_Nil:
        def test_toPyList_none(self):
            sut = SinglyLinkedList.list().toPyList()
            assert_that(sut, equal_to([]))
