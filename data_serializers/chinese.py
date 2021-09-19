from .base import SerializerAble
import codecs
from ..version_serializers import Version


class ChineseSerializer(SerializerAble):
    flag = '1101'

    @staticmethod
    def counting_indicator_map(version_num: int) -> int:
        if version_num <= 9:
            return 8
        elif version_num <= 26:
            return 10
        else:
            return 12

    def encode(self, **kwargs) -> str:
        """
        1. 对于第一字节值在0xA1到0xAA范围，第二字节值在0xA1到0xFE范围的字符
            1）第一字节值减去0xA1
            2）将1）的结果乘以0x60
            3）第二字节值减去0xA1
            4）将2）的结果加上3）的结果
            5）将结果转换为13位二进制串
        2. 对于第一字节值在0xBO到0xFA范围，第二字节值在0xA1到0xFE范围的字符
            1）第一字节值减去0xA6
            2）将1）的结果乘以0x60
            3）第二字节值减去0xA1
            4）将2）的结果加上3）的结果
            5）将结果转换为13位二进制串
        """
        character = ""
        for _c in self.raw_data:
            c1, c2 = _c.encode('gb2312')
            if 0xA1 <= c1 <= 0xAA:
                c1 -= 0xA1
            else:
                c1 -= 0xA6
            c1 *= 0x60
            c2 -= 0xA1
            character += self.bin(c1 + c2, 13)
        return character

    @classmethod
    def get_len(cls, version: Version, raw_data: str) -> int:
        counting = cls.counting_indicator_map(version.version_num)
        return 4 + 4 + counting + 13 * len(raw_data)
