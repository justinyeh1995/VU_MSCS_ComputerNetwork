# automatically generated by the FlatBuffers compiler, do not modify

# namespace: ResponseProto

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class ResponseMessage(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = ResponseMessage()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsResponseMessage(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # ResponseMessage
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # ResponseMessage
    def Type(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # ResponseMessage
    def Code(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int8Flags, o + self._tab.Pos)
        return 0

    # ResponseMessage
    def Content(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

def ResponseMessageStart(builder): builder.StartObject(3)
def Start(builder):
    return ResponseMessageStart(builder)
def ResponseMessageAddType(builder, type): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(type), 0)
def AddType(builder, type):
    return ResponseMessageAddType(builder, type)
def ResponseMessageAddCode(builder, code): builder.PrependInt8Slot(1, code, 0)
def AddCode(builder, code):
    return ResponseMessageAddCode(builder, code)
def ResponseMessageAddContent(builder, content): builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(content), 0)
def AddContent(builder, content):
    return ResponseMessageAddContent(builder, content)
def ResponseMessageEnd(builder): return builder.EndObject()
def End(builder):
    return ResponseMessageEnd(builder)