import math

from ..version_serializers import Version
from typing import Union, Optional, SupportsBytes, Iterable


class SerializerAble(object):
    """
    用于将传入的字符串数据变为码字
    """

    def __init__(self, version: Version, raw_data: str):
        self.version: Version = version
        self.raw_data: str = raw_data

    @staticmethod
    def counting_indicator_map(version_num: int)->int:
        return 0

    @property
    def counting_indicator(self):
        """计算字符计数指示符"""
        counting = self.counting_indicator_map(self.version.version_num)
        return self.bin(len(self.raw_data), counting)

    @property
    def flag(self) -> SupportsBytes:
        """模式指示符"""
        raise NotImplementedError

    def encode(self, **kwargs) -> str:
        """生成码字"""
        raise NotImplementedError

    @classmethod
    def decode(cls, version: Version, raw_data: str, **kwargs) -> 'SerializerAble':
        """解析码字"""
        raise cls(version=version, raw_data=raw_data)

    @staticmethod
    def bin(number: int, format_size=0):
        """将数字转化为二进制字符，并在左侧填充对其"""
        return bin(number)[2:].rjust(format_size, '0')

    @staticmethod
    def chunk_string(string_data: str, length: int = None) -> Iterable:
        length = length or len(string_data)
        if length <= 0:
            return []
        split_size = math.ceil(len(string_data) / length)
        return (string_data[i * length:(i + 1) * length] for i in range(split_size))

    @classmethod
    def get_len(cls, version: Version, raw_data: str) -> int:
        return 0
