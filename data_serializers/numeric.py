import typing

from .base import SerializerAble


class NumericSerializer(SerializerAble):
    flag = '0001'

    @property
    def counting_indicator(self):
        """计算字符计数指示符"""
        if self.version.version_num <= 9:
            counting = 10
        elif self.version.version_num <= 26:
            counting = 12
        else:
            counting = 14
        return self.bin(len(self.raw_data), counting)

    def encode(self) -> str:
        raw_array: typing.Iterable = self.chunk_string(self.raw_data, 3)
        raw_data = []
        for raw in raw_array:
            raw_data.append(self.bin(int(raw), len(raw) * 3 + 1))
        return self.flag + self.counting_indicator + "".join(raw_data)
