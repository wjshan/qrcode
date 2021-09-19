import typing

from .base import SerializerAble
from typing import SupportsInt, SupportsBytes, List
import re
from ..version_serializers import Version


class NumericSerializer(SerializerAble):
    flag = '0001'

    @staticmethod
    def counting_indicator_map(version_num: int) -> int:
        if version_num <= 9:
            counting = 10
        elif version_num <= 26:
            counting = 12
        else:
            counting = 14
        return counting

    def encode(self) -> str:
        raw_array: typing.Iterable = self.chunk_string(self.raw_data, 3)
        raw_data = []
        for raw in raw_array:
            raw_data.append(self.bin(int(raw), len(raw) * 3 + 1))
        return self.flag + self.counting_indicator + "".join(raw_data)

    @classmethod
    def get_len(cls, version: Version, raw_data: str) -> int:
        counting = cls.counting_indicator_map(version.version_num)
        mod = len(raw_data) % 3
        r = mod and mod * 3 + 1
        return 4 + counting + 10 * len(raw_data) // 3 + r
