# automatically generated by the FlatBuffers compiler, do not modify

# namespace: GroceryOrderProto

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class Meat(object):
    __slots__ = ['_tab']

    @classmethod
    def SizeOf(cls):
        return 8

    # Meat
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Meat
    def Type(self): return self._tab.Get(flatbuffers.number_types.Int8Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(0))
    # Meat
    def Quantity(self): return self._tab.Get(flatbuffers.number_types.Float32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(4))

def CreateMeat(builder, type, quantity):
    builder.Prep(4, 8)
    builder.PrependFloat32(quantity)
    builder.Pad(3)
    builder.PrependInt8(type)
    return builder.Offset()
