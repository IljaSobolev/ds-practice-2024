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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11order_queue.proto\x12\norderqueue\"\xed\x06\n\x05Order\x12$\n\x04user\x18\x01 \x01(\x0b\x32\x16.orderqueue.Order.User\x12\x30\n\ncreditCard\x18\x02 \x01(\x0b\x32\x1c.orderqueue.Order.CreditCard\x12\x13\n\x0buserComment\x18\x03 \x01(\t\x12%\n\x05items\x18\x04 \x03(\x0b\x32\x16.orderqueue.Order.Item\x12\x14\n\x0c\x64iscountCode\x18\x05 \x01(\t\x12\x16\n\x0eshippingMethod\x18\x06 \x01(\t\x12\x13\n\x0bgiftMessage\x18\x07 \x01(\t\x12\x38\n\x0e\x62illingAddress\x18\x08 \x01(\x0b\x32 .orderqueue.Order.BillingAddress\x12\x14\n\x0cgiftWrapping\x18\t \x01(\x08\x12\"\n\x1atermsAndConditionsAccepted\x18\n \x01(\x08\x12\x1f\n\x17notificationPreferences\x18\x0b \x03(\t\x12(\n\x06\x64\x65vice\x18\x0c \x01(\x0b\x32\x18.orderqueue.Order.Device\x12*\n\x07\x62rowser\x18\r \x01(\x0b\x32\x19.orderqueue.Order.Browser\x12\x12\n\nappVersion\x18\x0e \x01(\t\x12\x18\n\x10screenResolution\x18\x0f \x01(\t\x12\x10\n\x08referrer\x18\x10 \x01(\t\x12\x16\n\x0e\x64\x65viceLanguage\x18\x11 \x01(\t\x1a%\n\x04User\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontact\x18\x02 \x01(\t\x1a\x41\n\nCreditCard\x12\x0e\n\x06number\x18\x01 \x01(\t\x12\x16\n\x0e\x65xpirationDate\x18\x02 \x01(\t\x12\x0b\n\x03\x63vv\x18\x03 \x01(\t\x1a&\n\x04Item\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08quantity\x18\x02 \x01(\x03\x1a[\n\x0e\x42illingAddress\x12\x0e\n\x06street\x18\x01 \x01(\t\x12\x0c\n\x04\x63ity\x18\x02 \x01(\t\x12\r\n\x05state\x18\x03 \x01(\t\x12\x0b\n\x03zip\x18\x04 \x01(\t\x12\x0f\n\x07\x63ountry\x18\x05 \x01(\t\x1a\x31\n\x06\x44\x65vice\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\r\n\x05model\x18\x02 \x01(\t\x12\n\n\x02os\x18\x03 \x01(\t\x1a(\n\x07\x42rowser\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t\"7\n\x13\x45nqueueOrderRequest\x12 \n\x05order\x18\x01 \x01(\x0b\x32\x11.orderqueue.Order\"\'\n\x14\x45nqueueOrderResponse\x12\x0f\n\x07message\x18\x01 \x01(\t2_\n\nOrderQueue\x12Q\n\x0c\x45nqueueOrder\x12\x1f.orderqueue.EnqueueOrderRequest\x1a .orderqueue.EnqueueOrderResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'order_queue_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_ORDER']._serialized_start=34
  _globals['_ORDER']._serialized_end=911
  _globals['_ORDER_USER']._serialized_start=581
  _globals['_ORDER_USER']._serialized_end=618
  _globals['_ORDER_CREDITCARD']._serialized_start=620
  _globals['_ORDER_CREDITCARD']._serialized_end=685
  _globals['_ORDER_ITEM']._serialized_start=687
  _globals['_ORDER_ITEM']._serialized_end=725
  _globals['_ORDER_BILLINGADDRESS']._serialized_start=727
  _globals['_ORDER_BILLINGADDRESS']._serialized_end=818
  _globals['_ORDER_DEVICE']._serialized_start=820
  _globals['_ORDER_DEVICE']._serialized_end=869
  _globals['_ORDER_BROWSER']._serialized_start=871
  _globals['_ORDER_BROWSER']._serialized_end=911
  _globals['_ENQUEUEORDERREQUEST']._serialized_start=913
  _globals['_ENQUEUEORDERREQUEST']._serialized_end=968
  _globals['_ENQUEUEORDERRESPONSE']._serialized_start=970
  _globals['_ENQUEUEORDERRESPONSE']._serialized_end=1009
  _globals['_ORDERQUEUE']._serialized_start=1011
  _globals['_ORDERQUEUE']._serialized_end=1106
# @@protoc_insertion_point(module_scope)
