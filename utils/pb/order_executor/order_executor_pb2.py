# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: order_executor.proto
# Protobuf Python Version: 4.25.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14order_executor.proto\"\xab\x06\n\x05Order\x12\x19\n\x04user\x18\x01 \x01(\x0b\x32\x0b.Order.User\x12%\n\ncreditCard\x18\x02 \x01(\x0b\x32\x11.Order.CreditCard\x12\x13\n\x0buserComment\x18\x03 \x01(\t\x12\x1a\n\x05items\x18\x04 \x03(\x0b\x32\x0b.Order.Item\x12\x14\n\x0c\x64iscountCode\x18\x05 \x01(\t\x12\x16\n\x0eshippingMethod\x18\x06 \x01(\t\x12\x13\n\x0bgiftMessage\x18\x07 \x01(\t\x12-\n\x0e\x62illingAddress\x18\x08 \x01(\x0b\x32\x15.Order.BillingAddress\x12\x14\n\x0cgiftWrapping\x18\t \x01(\x08\x12\"\n\x1atermsAndConditionsAccepted\x18\n \x01(\x08\x12\x1f\n\x17notificationPreferences\x18\x0b \x03(\t\x12\x1d\n\x06\x64\x65vice\x18\x0c \x01(\x0b\x32\r.Order.Device\x12\x1f\n\x07\x62rowser\x18\r \x01(\x0b\x32\x0e.Order.Browser\x12\x12\n\nappVersion\x18\x0e \x01(\t\x12\x18\n\x10screenResolution\x18\x0f \x01(\t\x12\x10\n\x08referrer\x18\x10 \x01(\t\x12\x16\n\x0e\x64\x65viceLanguage\x18\x11 \x01(\t\x1a%\n\x04User\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontact\x18\x02 \x01(\t\x1a\x41\n\nCreditCard\x12\x0e\n\x06number\x18\x01 \x01(\t\x12\x16\n\x0e\x65xpirationDate\x18\x02 \x01(\t\x12\x0b\n\x03\x63vv\x18\x03 \x01(\t\x1a&\n\x04Item\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08quantity\x18\x02 \x01(\x03\x1a[\n\x0e\x42illingAddress\x12\x0e\n\x06street\x18\x01 \x01(\t\x12\x0c\n\x04\x63ity\x18\x02 \x01(\t\x12\r\n\x05state\x18\x03 \x01(\t\x12\x0b\n\x03zip\x18\x04 \x01(\t\x12\x0f\n\x07\x63ountry\x18\x05 \x01(\t\x1a\x31\n\x06\x44\x65vice\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\r\n\x05model\x18\x02 \x01(\t\x12\n\n\x02os\x18\x03 \x01(\t\x1a(\n\x07\x42rowser\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t\"\x19\n\x08Response\x12\r\n\x05\x65rror\x18\x01 \x01(\x08\" \n\x07Request\x12\x15\n\x05order\x18\x01 \x01(\x0b\x32\x06.Order2\x0f\n\rOrderExecutorb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'order_executor_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_ORDER']._serialized_start=25
  _globals['_ORDER']._serialized_end=836
  _globals['_ORDER_USER']._serialized_start=506
  _globals['_ORDER_USER']._serialized_end=543
  _globals['_ORDER_CREDITCARD']._serialized_start=545
  _globals['_ORDER_CREDITCARD']._serialized_end=610
  _globals['_ORDER_ITEM']._serialized_start=612
  _globals['_ORDER_ITEM']._serialized_end=650
  _globals['_ORDER_BILLINGADDRESS']._serialized_start=652
  _globals['_ORDER_BILLINGADDRESS']._serialized_end=743
  _globals['_ORDER_DEVICE']._serialized_start=745
  _globals['_ORDER_DEVICE']._serialized_end=794
  _globals['_ORDER_BROWSER']._serialized_start=796
  _globals['_ORDER_BROWSER']._serialized_end=836
  _globals['_RESPONSE']._serialized_start=838
  _globals['_RESPONSE']._serialized_end=863
  _globals['_REQUEST']._serialized_start=865
  _globals['_REQUEST']._serialized_end=897
  _globals['_ORDEREXECUTOR']._serialized_start=899
  _globals['_ORDEREXECUTOR']._serialized_end=914
# @@protoc_insertion_point(module_scope)