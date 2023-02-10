"""Generic marks applicable to a variety of protocols."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, TypeVar, Union

from typing_extensions import TypeAlias

from combadge.core.mark import MethodMark, ParameterMark, make_method_mark_decorator
from combadge.support.rest.abc import RequiresMethod, RequiresPath, SupportsQueryParams

T = TypeVar("T")


class PathMark(MethodMark[RequiresPath]):
    """
    Specifies a URL path.

    Example:
        >>> @path("/hello/world")
        >>> def call() -> None: ...

        >>> @path("/hello/{name}")
        >>> def call(name: str) -> None: ...

        >>> @path(lambda name, **_: f"/hello/{name}")
        >>> def call(name: str) -> None: ...

    Notes:
        - Always refer to parameters with their names. Positional arguments, e.g. `{0}` are
          intentionally unsupported.
    """

    _factory: Callable[..., str]
    __slots__ = ("_factory",)

    def __init__(self, path_or_factory: Union[str, Callable[..., str]]) -> None:  # noqa: D107
        if callable(path_or_factory):
            self._factory = path_or_factory
        else:
            self._factory = path_or_factory.format

    def prepare_request(self, request: RequiresPath, _arguments: Dict[str, Any]) -> None:  # noqa: D102
        request.path = self._factory(**_arguments)


path = make_method_mark_decorator(PathMark)


@dataclass
class RestMethodMark(MethodMark[RequiresMethod]):
    """Specifies HTTP/REST method."""

    method: str  # TODO: enum?

    def prepare_request(self, request: RequiresMethod, _arguments: Dict[str, Any]) -> None:  # noqa: D102
        request.method = self.method


method = make_method_mark_decorator(RestMethodMark)


@dataclass
class QueryParameterMark(ParameterMark[SupportsQueryParams]):
    """Designates parameter as a service call's query parameter."""

    name: str
    __slots__ = ("name",)

    def prepare_request(self, request: SupportsQueryParams, value: Any) -> None:  # noqa: D102
        request.query_params.append((self.name, value))


QueryParam: TypeAlias = QueryParameterMark
