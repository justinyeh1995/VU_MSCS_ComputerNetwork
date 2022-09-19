# automatically generated by the FlatBuffers compiler, do not modify

# namespace: GroceryOrderProto

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class Veggies(object):
    __slots__ = ['_tab']

    @classmethod
    def SizeOf(cls):
        return 20

    # Veggies
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Veggies
    def Tomato(self): return self._tab.Get(flatbuffers.number_types.Float32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(0))
    # Veggies
    def Cucumber(self): return self._tab.Get(flatbuffers.number_types.Float32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(4))
    # Veggies
    def Potato(self): return self._tab.Get(flatbuffers.number_types.Float32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(8))
    # Veggies
    def Bokchoy(self): return self._tab.Get(flatbuffers.number_types.Float32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(12))
    # Veggies
    def Broccoli(self): return self._tab.Get(flatbuffers.number_types.Float32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(16))

def CreateVeggies(builder, tomato, cucumber, potato, bokchoy, broccoli):
    builder.Prep(4, 20)
    builder.PrependFloat32(broccoli)
    builder.PrependFloat32(bokchoy)
    builder.PrependFloat32(potato)
    builder.PrependFloat32(cucumber)
    builder.PrependFloat32(tomato)
    return builder.Offset()
