from typing import Any, Type

from httpx import AsyncClient, Response
from pydantic import BaseModel, parse_obj_as

from combadge.core.binder import BaseBoundService, Signature
from combadge.core.interfaces import SupportsBindServiceMethod, SupportsServiceMethodCall
from combadge.core.request import build_request
from combadge.core.typevars import ResponseT
from combadge.support.rest.request import Request


class HttpxBackend(SupportsBindServiceMethod):
    """
    Async HTTPX backend for REST APIs.

    See Also:
        - https://www.python-httpx.org/
    """

    _client: AsyncClient
    __slots__ = ("_client",)

    def __init__(self, client: AsyncClient) -> None:  # noqa: D107
        self._client = client

    async def __call__(self, request: Request, response_type: Type[ResponseT]) -> ResponseT:
        """Call the backend."""
        response: Response = await self._client.request(
            request.method,
            request.path,
            json=request.body_dict(),
            params=request.query_params,
        )
        response.raise_for_status()
        return parse_obj_as(response_type, response.json())

    def bind_method(self, signature: Signature) -> SupportsServiceMethodCall:  # noqa: D102
        async def resolved_method(service: BaseBoundService, *args: Any, **kwargs: Any) -> BaseModel:
            request = build_request(Request, signature, service, args, kwargs)
            return await self(request, signature.return_type)

        return resolved_method  # type: ignore[return-value]