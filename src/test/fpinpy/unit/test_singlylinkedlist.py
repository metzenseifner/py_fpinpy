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
        def test_that_direct_construction_fails(self):
            assert_that(Cons, raises(RuntimeError))
        def test_factory_some(self):
            sut = SinglyLinkedList.list(1, 2, 3)
            assert_that(sut, instance_of(Cons))
        def test_factory_singleton(self):
            sut = SinglyLinkedList.list(1)
            assert_that(sut, instance_of(Cons))
    class Test_Nil:
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
        def test_str(self):
            sut = SinglyLinkedList.list(1, 2, 3)
            assert_that(str(sut), equal_to("[1, 2, 3, NIL]"))

class Test_foldLeft():
    class Test_Cons:
        def test_foldLeft_some(self):
            sut = SinglyLinkedList.list(1, 2, 3).foldLeft(0, lambda x, y: x + y)
            assert_that(sut, equal_to(6))
        def test_foldLeft_singleton(self):
            sut = SinglyLinkedList.list(1).foldLeft(0, lambda x, y: x + y)
            assert_that(sut, equal_to(1))
    class Test_Nil:
        def test_foldLeft(self):
            sut = SinglyLinkedList.list().foldLeft(0, lambda x, y: x + y)
            assert_that(str(sut), equal_to("[NIL]"))
