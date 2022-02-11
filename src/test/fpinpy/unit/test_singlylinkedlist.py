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
        def test_foldLeft(self):
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
