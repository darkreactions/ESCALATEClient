from typing import Protocol, overload, Literal, Any, Dict, List
import requests


class BaseClientProtocol(Protocol):

    _selected_lab: "list[Any]"

    @overload
    def get(
        self,
        endpoint: str = ...,
        data: Dict[str, str] = ...,
        resource_id: str = ...,
        related_endpoint: str = ...,
        parse_json: Literal[True] = ...,
        content_type: str = ...,
    ) -> "list[Any]":
        ...

    @overload
    def get(
        self,
        endpoint: str = ...,
        data: Dict[str, str] = ...,
        resource_id: str = ...,
        related_endpoint: str = ...,
        parse_json: Literal[False] = ...,
        content_type: str = ...,
    ) -> requests.Response:
        ...

    def get(
        self,
        endpoint: str = "",
        data: Dict[str, str] = {},
        resource_id: str = "",
        related_endpoint: str = "",
        parse_json: bool = True,
        content_type: str = "application/json",
    ) -> "list[Any] | requests.Response":
        ...

    def get_or_create(
        self,
        endpoint: str,
        resource_id: str = "",
        related_endpoint: str = "",
        data: Dict[str, Any] = {},
    ) -> "List[ResponseData]":
        ...


RTName = str
ResponseData = Dict[str, Any]
RTResponse = ResponseData
RMTName = str
RMTResponse = ResponseData
RMTResponseList = List[RMTResponse]