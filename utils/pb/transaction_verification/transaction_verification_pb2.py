# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: transaction_verification.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1etransaction_verification.proto\x12\x0cverification\"A\n\nCreditCard\x12\x0e\n\x06number\x18\x01 \x01(\t\x12\x16\n\x0e\x65xpirationDate\x18\x02 \x01(\t\x12\x0b\n\x03\x63vv\x18\x03 \x01(\t\"C\n\x13VerificationRequest\x12,\n\ncreditCard\x18\x01 \x01(\x0b\x32\x18.verification.CreditCard\"(\n\x14VerificationResponse\x12\x10\n\x08response\x18\x01 \x01(\t2f\n\x13VerificationService\x12O\n\x06Verify\x12!.verification.VerificationRequest\x1a\".verification.VerificationResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'transaction_verification_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_CREDITCARD']._serialized_start=48
  _globals['_CREDITCARD']._serialized_end=113
  _globals['_VERIFICATIONREQUEST']._serialized_start=115
  _globals['_VERIFICATIONREQUEST']._serialized_end=182
  _globals['_VERIFICATIONRESPONSE']._serialized_start=184
  _globals['_VERIFICATIONRESPONSE']._serialized_end=224
  _globals['_VERIFICATIONSERVICE']._serialized_start=226
  _globals['_VERIFICATIONSERVICE']._serialized_end=328
# @@protoc_insertion_point(module_scope)
