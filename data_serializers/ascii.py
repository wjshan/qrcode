from .base import SerializerAble
from ..version_serializers import Version


class AscIISerializer(SerializerAble):
    flag = '0100'

    @staticmethod
    def counting_indicator_map(version_num: int) -> int:
        if version_num <= 9:
            return 8
        else:
            return 16

    def encode(self, **kwargs) -> str:
        character = ''
        for _chr in self.raw_data:
            character += self.bin(ord(_chr), 8)
        return self.flag + self.counting_indicator + character

    @classmethod
    def get_len(cls, version: Version, raw_data: str) -> int:
        counting = cls.counting_indicator_map(version.version_num)
        mod = len(raw_data) % 3
        r = mod and mod * 3 + 1
        return 4 + counting + 10 * len(raw_data) // 3 + r


