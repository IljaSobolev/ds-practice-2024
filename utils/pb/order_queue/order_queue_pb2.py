# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: order_queue.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11order_queue.proto\x12\norderqueue\"2\n\x05Order\x12\n\n\x02id\x18\x01 \x01(\x05\x12\r\n\x05title\x18\x02 \x01(\t\x12\x0e\n\x06\x61uthor\x18\x03 \x01(\t\"I\n\x13\x45nqueueOrderRequest\x12 \n\x05order\x18\x01 \x01(\x0b\x32\x11.orderqueue.Order\x12\x10\n\x08priority\x18\x02 \x01(\x05\"\'\n\x14\x45nqueueOrderResponse\x12\x0f\n\x07message\x18\x01 \x01(\t2_\n\nOrderQueue\x12Q\n\x0c\x45nqueueOrder\x12\x1f.orderqueue.EnqueueOrderRequest\x1a .orderqueue.EnqueueOrderResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'order_queue_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_ORDER']._serialized_start=33
  _globals['_ORDER']._serialized_end=83
  _globals['_ENQUEUEORDERREQUEST']._serialized_start=85
  _globals['_ENQUEUEORDERREQUEST']._serialized_end=158
  _globals['_ENQUEUEORDERRESPONSE']._serialized_start=160
  _globals['_ENQUEUEORDERRESPONSE']._serialized_end=199
  _globals['_ORDERQUEUE']._serialized_start=201
  _globals['_ORDERQUEUE']._serialized_end=296
# @@protoc_insertion_point(module_scope)
