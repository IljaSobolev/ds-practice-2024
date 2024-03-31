from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Order(_message.Message):
    __slots__ = ("id", "title", "author")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    id: int
    title: str
    author: str
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., author: _Optional[str] = ...) -> None: ...

class EnqueueOrderRequest(_message.Message):
    __slots__ = ("order", "priority")
    ORDER_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    order: Order
    priority: int
    def __init__(self, order: _Optional[_Union[Order, _Mapping]] = ..., priority: _Optional[int] = ...) -> None: ...

class EnqueueOrderResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...
