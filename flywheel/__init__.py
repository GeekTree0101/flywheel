""" flywheel """
try:
    from ._version import *  # pylint: disable=F0401,W0401
except ImportError:
    __version__ = 'unknown'

import boto.dynamodb.types
from boto.dynamodb2.types import (STRING, NUMBER, BINARY, STRING_SET,
                                  NUMBER_SET, BINARY_SET)
from decimal import Inexact, Rounded, Decimal


# HACK to force conversion of floats to Decimals
boto.dynamodb.types.DYNAMODB_CONTEXT.traps[Inexact] = False
boto.dynamodb.types.DYNAMODB_CONTEXT.traps[Rounded] = False


def float_to_decimal(f):
    """ Monkey-patched replacement for boto's broken version """
    n, d = f.as_integer_ratio()
    numerator, denominator = Decimal(n), Decimal(d)
    ctx = boto.dynamodb.types.DYNAMODB_CONTEXT
    return ctx.divide(numerator, denominator)

boto.dynamodb.types.float_to_decimal = float_to_decimal


from .fields import Field, Composite, GlobalIndex, Binary
from .models import Model, ValidationError
from .engine import Engine
