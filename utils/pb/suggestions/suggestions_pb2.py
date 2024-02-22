# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: suggestions.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11suggestions.proto\x12\x0bsuggestions\"\xa4\x07\n\x0c\x43heckoutData\x12,\n\x04user\x18\x01 \x01(\x0b\x32\x1e.suggestions.CheckoutData.User\x12\x38\n\ncreditCard\x18\x02 \x01(\x0b\x32$.suggestions.CheckoutData.CreditCard\x12\x13\n\x0buserComment\x18\x03 \x01(\t\x12-\n\x05items\x18\x04 \x03(\x0b\x32\x1e.suggestions.CheckoutData.Item\x12\x14\n\x0c\x64iscountCode\x18\x05 \x01(\t\x12\x16\n\x0eshippingMethod\x18\x06 \x01(\t\x12\x13\n\x0bgiftMessage\x18\x07 \x01(\t\x12@\n\x0e\x62illingAddress\x18\x08 \x01(\x0b\x32(.suggestions.CheckoutData.BillingAddress\x12\x14\n\x0cgiftWrapping\x18\t \x01(\x08\x12\"\n\x1atermsAndConditionsAccepted\x18\n \x01(\x08\x12\x1f\n\x17notificationPreferences\x18\x0b \x03(\t\x12\x30\n\x06\x64\x65vice\x18\x0c \x01(\x0b\x32 .suggestions.CheckoutData.Device\x12\x32\n\x07\x62rowser\x18\r \x01(\x0b\x32!.suggestions.CheckoutData.Browser\x12\x12\n\nappVersion\x18\x0e \x01(\t\x12\x18\n\x10screenResolution\x18\x0f \x01(\t\x12\x10\n\x08referrer\x18\x10 \x01(\t\x12\x16\n\x0e\x64\x65viceLanguage\x18\x11 \x01(\t\x1a%\n\x04User\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontact\x18\x02 \x01(\t\x1a\x41\n\nCreditCard\x12\x0e\n\x06number\x18\x01 \x01(\t\x12\x16\n\x0e\x65xpirationDate\x18\x02 \x01(\t\x12\x0b\n\x03\x63vv\x18\x03 \x01(\t\x1a&\n\x04Item\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08quantity\x18\x02 \x01(\x03\x1a[\n\x0e\x42illingAddress\x12\x0e\n\x06street\x18\x01 \x01(\t\x12\x0c\n\x04\x63ity\x18\x02 \x01(\t\x12\r\n\x05state\x18\x03 \x01(\t\x12\x0b\n\x03zip\x18\x04 \x01(\t\x12\x0f\n\x07\x63ountry\x18\x05 \x01(\t\x1a\x31\n\x06\x44\x65vice\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\r\n\x05model\x18\x02 \x01(\t\x12\n\n\x02os\x18\x03 \x01(\t\x1a(\n\x07\x42rowser\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t\"D\n\x11SuggestionRequest\x12/\n\x0c\x63heckoutData\x18\x01 \x01(\x0b\x32\x19.suggestions.CheckoutData\"7\n\nSuggestion\x12\n\n\x02id\x18\x01 \x01(\x03\x12\r\n\x05title\x18\x02 \x01(\t\x12\x0e\n\x06\x61uthor\x18\x03 \x01(\t\"B\n\x12SuggestionResponse\x12,\n\x0bsuggestions\x18\x01 \x03(\x0b\x32\x17.suggestions.Suggestion2_\n\x11SuggestionService\x12J\n\x07Suggest\x12\x1e.suggestions.SuggestionRequest\x1a\x1f.suggestions.SuggestionResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'suggestions_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_CHECKOUTDATA']._serialized_start=35
  _globals['_CHECKOUTDATA']._serialized_end=967
  _globals['_CHECKOUTDATA_USER']._serialized_start=637
  _globals['_CHECKOUTDATA_USER']._serialized_end=674
  _globals['_CHECKOUTDATA_CREDITCARD']._serialized_start=676
  _globals['_CHECKOUTDATA_CREDITCARD']._serialized_end=741
  _globals['_CHECKOUTDATA_ITEM']._serialized_start=743
  _globals['_CHECKOUTDATA_ITEM']._serialized_end=781
  _globals['_CHECKOUTDATA_BILLINGADDRESS']._serialized_start=783
  _globals['_CHECKOUTDATA_BILLINGADDRESS']._serialized_end=874
  _globals['_CHECKOUTDATA_DEVICE']._serialized_start=876
  _globals['_CHECKOUTDATA_DEVICE']._serialized_end=925
  _globals['_CHECKOUTDATA_BROWSER']._serialized_start=927
  _globals['_CHECKOUTDATA_BROWSER']._serialized_end=967
  _globals['_SUGGESTIONREQUEST']._serialized_start=969
  _globals['_SUGGESTIONREQUEST']._serialized_end=1037
  _globals['_SUGGESTION']._serialized_start=1039
  _globals['_SUGGESTION']._serialized_end=1094
  _globals['_SUGGESTIONRESPONSE']._serialized_start=1096
  _globals['_SUGGESTIONRESPONSE']._serialized_end=1162
  _globals['_SUGGESTIONSERVICE']._serialized_start=1164
  _globals['_SUGGESTIONSERVICE']._serialized_end=1259
# @@protoc_insertion_point(module_scope)
