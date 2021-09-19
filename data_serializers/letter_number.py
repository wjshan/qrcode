from .base import SerializerAble
from ..version_serializers import Version

codec_map = {
    "0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "A": 10, "B": 11, "C": 12,
    "D": 13, "E": 14, "F": 15, "G": 16, "H": 17, "I": 18, "J": 19, "L": 20, "K": 21, "M": 22, "N": 23, "O": 24,
    "P": 25, "Q": 26, "R": 27, "S": 28, "T": 29, "U": 30, "V": 31, "W": 32, "X": 33, "Y": 34, "Z": 35, " ": 36,
    "$": 37, "%": 38, "*": 39, "+": 40, "-": 41, ".": 42, "/": 43, ":": 44,
}


class LetterNumberSerializer(SerializerAble):
    flag = '0010'

    @staticmethod
    def counting_indicator_map(version_num: int) -> int:
        if version_num <= 9:
            return 9
        elif version_num <= 26:
            return 11
        else:
            return 13

    def encode(self, **kwargs) -> str:
        raw_iter = self.chunk_string(self.raw_data, 2)
        character = ''
        for group in raw_iter:
            if len(group) == 2:
                chr1, chr2 = group
                _sub_chr = self.bin(codec_map[chr1] * 45 + codec_map[chr2], 11)
            else:
                _sub_chr = self.bin(codec_map[group[0]], 6)
            character += _sub_chr
        return self.flag + self.counting_indicator + character

    @classmethod
    def get_len(cls, version: Version, raw_data: str) -> int:
        return 4 + cls.counting_indicator_map(version.version_num) + 11 * (len(raw_data) // 2) + 6 * (len(raw_data) % 2)
