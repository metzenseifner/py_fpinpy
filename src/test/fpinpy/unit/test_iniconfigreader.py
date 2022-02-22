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
from fpinpy import IniConfigReader, Result, Success, Failure

class Test_InitConfigReader():
    class Test_init():
        def test_factory_of_string(self):
            sut = IniConfigReader.of("[topsecret.server.com]\nPort=48484")
            assert_that(sut.successValue(), instance_of(IniConfigReader))
        def test_factory_of_dict(self):
            sut = IniConfigReader.of({"topsecret.server.com": {"Port": 21212}})
            assert_that(sut.successValue(), instance_of(IniConfigReader))
        @pytest.mark.skip
        def test_factory_of_path(self):
            """ Belongs in integration test """
            pass #sut = IniConfigReader.of()
    class Test_getProperty():
        def test_getProperty_when_exists(self):
            sut = IniConfigReader.of({"topsecret.server.com": {"Port": 21212}})
            assert_that(sut.flatMap(lambda parser: parser.getProperty('topsecret.server.com', 'Port')).getOrElse(None), equal_to('21212'))
        def test_getProperty_when_missing(self):
            sut = IniConfigReader.of({"topsecret.server.com": {"Port": 21212}})
            assert_that(sut.flatMap(lambda parser: parser.getProperty('public.server.com', 'Port')), instance_of(Failure))
    class Test_getSection():
        def test_getSection_when_exists_multiple(self):
            sut = IniConfigReader.of({"topsecret.server.com": {"Port": 21212, "Username": "Schmoe"}})
            assert_that(str(sut.flatMap(lambda parser: parser.getSection('topsecret.server.com'))
                .getOrElse(None)), equal_to("[('port', '21212'), ('username', 'Schmoe'), NIL]"))
        def test_getSection_when_exists_one(self):
            sut = IniConfigReader.of({"topsecret.server.com": {"Port": 21212}})
            assert_that(str(sut.flatMap(lambda parser: parser.getSection('topsecret.server.com'))
                .getOrElse(None)), equal_to("[('port', '21212'), NIL]"))
        def test_getSection_when_exists_empty(self):
            sut = IniConfigReader.of({"topsecret.server.com": {}})
            assert_that(str(sut.flatMap(lambda parser: parser.getSection('topsecret.server.com'))
                .getOrElse(None)), equal_to("[NIL]"))
        def test_getSection_when_missing(self):
            sut = IniConfigReader.of({"topsecret.server.com": {"Port": 21212}})
            assert_that(sut.flatMap(lambda parser: parser.getSection('public.server.com')), instance_of(Failure))
