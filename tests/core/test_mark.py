from typing import Any, List, Type

import pytest
from typing_extensions import get_args as get_type_args

from combadge.core.mark import MethodMark, ParameterMark, _extract_parameter_marks
from combadge.support.marks import Body
from combadge.support.soap.marks import OperationNameMethodMark


def test_get_method_marks() -> None:
    def method() -> None:
        pass

    marks = MethodMark.extract(method)
    assert marks == []

    mark = OperationNameMethodMark("test")
    marks.append(mark)
    assert MethodMark.extract(method) == [mark]


@pytest.mark.parametrize(
    ("type_", "expected"),
    [
        (int, []),
        (Body[int], [get_type_args(Body)[1]]),
    ],
)
def test_extract_parameter_marks(type_: Type[Any], expected: List[ParameterMark]) -> None:
    assert _extract_parameter_marks(type_) == expected
