# automatically generated by the FlatBuffers compiler, do not modify

# namespace: HealthStatusProto

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class Contents(object):
    __slots__ = ['_tab']

    @classmethod
    def SizeOf(cls):
        return 24

    # Contents
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Contents
    def Dispenser(self): return self._tab.Get(flatbuffers.number_types.Int8Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(0))
    # Contents
    def Icemaker(self): return self._tab.Get(flatbuffers.number_types.Uint32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(4))
    # Contents
    def Lightbulb(self): return self._tab.Get(flatbuffers.number_types.Int8Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(8))
    # Contents
    def FridgeTemp(self): return self._tab.Get(flatbuffers.number_types.Uint32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(12))
    # Contents
    def FreezerTemp(self): return self._tab.Get(flatbuffers.number_types.Uint32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(16))
    # Contents
    def SensorStatus(self): return self._tab.Get(flatbuffers.number_types.Int8Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(20))

def CreateContents(builder, dispenser, icemaker, lightbulb, fridgeTemp, freezerTemp, sensorStatus):
    builder.Prep(4, 24)
    builder.Pad(3)
    builder.PrependInt8(sensorStatus)
    builder.PrependUint32(freezerTemp)
    builder.PrependUint32(fridgeTemp)
    builder.Pad(3)
    builder.PrependInt8(lightbulb)
    builder.PrependUint32(icemaker)
    builder.Pad(3)
    builder.PrependInt8(dispenser)
    return builder.Offset()