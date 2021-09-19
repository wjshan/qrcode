from .base import SerializerAble


class ECISerializer(SerializerAble):
    flag = '0111'

    def encode(self, **kwargs) -> str:
        pass
