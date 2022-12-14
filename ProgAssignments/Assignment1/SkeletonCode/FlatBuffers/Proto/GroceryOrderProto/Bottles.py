# automatically generated by the FlatBuffers compiler, do not modify

# namespace: GroceryOrderProto

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class Bottles(object):
    __slots__ = ['_tab']

    @classmethod
    def SizeOf(cls):
        return 12

    # Bottles
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Bottles
    def Sprite(self): return self._tab.Get(flatbuffers.number_types.Uint32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(0))
    # Bottles
    def Gingerale(self): return self._tab.Get(flatbuffers.number_types.Uint32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(4))
    # Bottles
    def Sevenup(self): return self._tab.Get(flatbuffers.number_types.Uint32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(8))

def CreateBottles(builder, sprite, gingerale, sevenup):
    builder.Prep(4, 12)
    builder.PrependUint32(sevenup)
    builder.PrependUint32(gingerale)
    builder.PrependUint32(sprite)
    return builder.Offset()
