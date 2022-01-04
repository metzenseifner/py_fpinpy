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

from fpinpy import Result, Success, Failure, Empty

@pytest.fixture(scope="function")
def effect():
    def effect(value):
        effect.local_storage = value
    yield effect

def liskov_subtitution(*arg, **kwargs):
    def a(method):
        return method
    return a

class TestInstantiation:
    class Result:
        def test_that_direct_construction_of_Result_yields_exception(self):
            with pytest.raises(RuntimeError):
                result = Result(1)
    class Success():
        def test_that_direct_construction_of_Success_yields_exception(self):
            with pytest.raises(RuntimeError):
                result = Success(1)
    
    class Failure():
        def test_that_direct_construction_of_Failure_yields_exception(self):
            with pytest.raises(RuntimeError):
                result = Failure(1)
    
    #def test_that_direct_construction_of_Empty_yields_exception(self):
    #    with pytest.raises(RuntimeError):
    #        result = Empty(1)

    def test_that_factory_of_yields_Success_on_good_value(self):
        sut = Result.of(1)
        assert_that(sut.isSuccess(), equal_to(True))
        assert_that(sut, instance_of(Success))

    def test_that_factory_of_yields_Failure_on_bad_value(self):
        sut = Result.of(None)
        assert_that(sut.isFailure(), equal_to(True))
        assert_that(sut, instance_of(Failure))

    def test_that_factory_empty_yields_Empty(self):
        sut = Result.empty()
        assert_that(sut.isEmpty(), equal_to(True))
        assert_that(sut, instance_of(Empty))
    
    def test_failure_factory_on_string_input(self):
        sut = Result.failure("oops").forEachOrFail(lambda x: None)
        assert_that(sut.successValue(), equal_to("oops"))

    def test_failure_factory_on_exception_input(self):
        sut = Result.failure(RuntimeError("oops")).forEachOrFail(lambda x: None)
        assert_that(sut.successValue(), equal_to("oops"))

    def test_failure_factory_on_string_and_exception_input(self):
        sut = Result.failure("oops", exception=ValueError).forEachOrFail(lambda x: None)
        assert_that(sut.successValue(), equal_to("oops"))

    def test_failure_factory_on_Failure_input(self):
        sut = Result.failure(Result.failure("oops")).forEachOrFail(lambda x: None)
        assert_that(sut.successValue(), equal_to("oops"))

    @liskov_subtitution
    def test_that_type_of_Success_is_Result(self):
        sut = Result.success(1).__class__.__bases__
        assert_that(sut, has_item(Result))

    @liskov_subtitution
    def test_that_type_of_Failure_is_Result(self):
        sut = Result.success(1).__class__.__bases__
        assert_that(sut, has_item(Result))
    
    @liskov_subtitution
    def test_that_type_of_Failure_is_Result(self):
        sut = Result.success(1).__class__.__bases__
        assert_that(sut, has_item(Result))

class TestFunctor():

    class Test_Success():
        def test_that_Success_when_map_succeeds_yields_success(self):
            sut = Result.of(1).map(lambda x: x + 1)
            assert_that(sut.successValue(), equal_to(2))
            assert_that(sut.isSuccess(), equal_to(True))
            assert_that(sut.isFailure(), equal_to(False))
            assert_that(sut.isEmpty(), equal_to(False))

        def test_that_Success_when_map_fails_yields_failure(self):
            sut = Result.of(1).map(lambda x: x / 0)
            assert_that(sut.isSuccess(), equal_to(False))
            assert_that(sut.isFailure(), equal_to(True))
            assert_that(sut.isEmpty(), equal_to(False))

    class Test_Failure():
        def test_that_Failure_when_map_always_yields_failure(self):
            sut = Result.failure(1).map(lambda x: x + 1)
            assert_that(sut.isSuccess(), equal_to(False))
            assert_that(sut.isFailure(), equal_to(True))
            assert_that(sut.isEmpty(), equal_to(False))

    class Test_Empty():
        def test_that_Empty_when_map_succeeds_yields_empty(self):
            sut = Result.empty().map(lambda x: x + 1)
            assert_that(sut.isSuccess(), equal_to(False))
            assert_that(sut.isFailure(), equal_to(False))
            assert_that(sut.isEmpty(), equal_to(True))

class TestApplicativeFunctor():
    class Test_Success():
        def test_Success_when_flatMap_succeeds_yields_success(self):
            func_from_a_to_Result_a = lambda a: Result.of(a)
            sut = Result.of(1).flatMap(func_from_a_to_Result_a)
            assert_that(sut.successValue(), equal_to(1))

        def test_Success_when_flatMap_fails_yields_failure(self):
            func_from_a_to_Result_a = lambda a: Result.of(a/0)
            sut = Result.of(1).flatMap(func_from_a_to_Result_a)
            assert_that(sut.isFailure(), equal_to(True))

    class Test_Failure():
        def test_Failure_when_flatMap_always_yields_failure(self):
            func_from_a_to_Result_a = lambda a: Result.of(a/0)
            sut = Result.of(1).flatMap(func_from_a_to_Result_a)
            assert_that(sut.isFailure(), equal_to(True))

    class Test_Empty():
        def test_Empty_when_flatMap_succeeds_yields_success(self):
            func_from_a_to_Result_a = lambda a: Result.empty()
            sut = Result.of(1).flatMap(func_from_a_to_Result_a)
            assert_that(sut.isEmpty(), equal_to(True))

class Test_getOrElse():
    class Test_Success():
        def test_when_getOrElse_of_value_applied_to_Success(self):
            sut = Result.of(1).getOrElse(2)
            assert_that(sut, equal_to(1))

        def test_when_getOrElse_of_function_applied_to_Success(self):
            sut = Result.of(1).getOrElse(lambda: 2)
            assert_that(sut, equal_to(1))

    class Test_Failure():
        def test_when_getOrElse_of_value_applied_to_Failure(self):
            sut = Result.failure("bad input").getOrElse(2)
            assert_that(sut, equal_to(2))

    class Test_Empty():
        def test_when_getOrElse_applied_to_Empty(self):
            sut = Result.empty().getOrElse(2)
            assert_that(sut, equal_to(2))

class Test_forEachOrException():

    class Test_Success():
        def test_forEachOrException(self, effect):
            sut = Result.success(1).forEachOrException(effect)
            assert_that(sut.isEmpty(), equal_to(True))

    class Test_Failure():
        def test_forEachOrException(self, effect):
            sut = Result.failure("oops").forEachOrException(effect)
            assert_that(sut.isSuccess(), equal_to(True))

    class Test_Empty():
        def test_forEachOrException(self, effect):
            sut = Result.empty().forEachOrException(effect)
            assert_that(sut.isEmpty(), equal_to(True))

@pytest.mark.usefixtures('effect')
class Test_forEachOrFail():

    class Test_Success():
        def test_forEachOrFail(self, effect):
            sut = Result.of(1).forEachOrFail(lambda x: effect(x))
            assert_that(sut.isEmpty(), equal_to(True))
            # Test that effect was applied
            assert_that(effect.local_storage, equal_to(1))
    
    class Test_Failure():
        def test_forEachOrFail(self, effect):
            sut = Result.failure("oops").forEachOrFail(lambda x: effect(x))
            assert_that(sut.successValue(), equal_to("oops"))

    class Test_Empty():
        def test_forEachOrFail(self, effect):
            sut = Result.empty().forEachOrFail(lambda x: effect(x))
            assert_that(sut.isEmpty(), equal_to(True))
            # Test that effect was not applied
            assert_that(effect, is_not(has_property('local_storage')))

class Test_mapFailure():
    class Test_Success():
        def test_mapFailure(self):
            sut = Result.success(1).mapFailure("new error message")
            assert_that(sut.isSuccess(), equal_to(True))
            
    class Test_Failure():
        def test_mapFailure(self):
            sut = Result.failure("oops").mapFailure("oh well")
            assert_that(sut.isFailure(), equal_to(True))
            assert_that(str(sut.failureValue()), equal_to("oh well"))

    class Test_Emtpy():
        def test_mapFailure(self):
            sut = Result.empty().mapFailure("new error message")
            assert_that(sut.isEmpty(), equal_to(True))
