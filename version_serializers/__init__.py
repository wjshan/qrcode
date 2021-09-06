from typing import Optional


class Version(object):
    def __init__(self, version_num: int = None):
        self.version_num: Optional[int] = version_num
