"""Mixins for HTTP-related request classes."""

from abc import ABC
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class SupportsHeaders(ABC):
    """HTTP request headers."""

    headers: List[Tuple[str, Any]] = field(default_factory=list)


@dataclass
class SupportsUrlPath(ABC):
    """Request URL path."""

    url_path: Optional[str] = None

    def get_url_path(self) -> str:
        """Get validated URL path."""
        if not (url_path := self.url_path):
            raise ValueError("an HTTP request requires a non-empty URL path")
        return url_path


@dataclass
class SupportsMethod(ABC):
    """HTTP request method."""

    method: Optional[str] = None

    def get_method(self) -> str:
        """Get a validated HTTP method."""
        if not (method := self.method):
            raise ValueError("an HTTP request requires a non-empty method")
        return method


@dataclass
class SupportsQueryParams(ABC):
    """HTTP request query parameters."""

    query_params: List[Tuple[str, Any]] = field(default_factory=list)


@dataclass
class SupportsJson(ABC):
    """HTTP request JSON body."""

    json_: Dict[str, Any] = field(default_factory=dict)
    """Used with [Json][combadge.support.http.markers.Json] and [JsonField][combadge.support.http.markers.JsonField]."""


@dataclass
class SupportsFormData(ABC):
    """
    HTTP request [form data][1].

    [1]: https://developer.mozilla.org/en-US/docs/Learn/Forms/Sending_and_retrieving_form_data
    """

    form_data: Dict[str, List[Any]] = field(default_factory=dict)
    """
    Used with [FormData][combadge.support.http.markers.FormData]
    and [FormField][combadge.support.http.markers.FormField].
    """

    def append_form_field(self, name: str, value: Any) -> None:  # noqa: D102
        self.form_data.setdefault(name, []).append(value)
