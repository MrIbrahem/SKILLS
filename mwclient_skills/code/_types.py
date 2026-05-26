from http.cookiejar import CookieJar
from typing import Mapping, Tuple, Union

Cookies = Union[Mapping[str, str], CookieJar]

Namespace = Union[str, int]

VersionTuple = Tuple[Union[int, str], ...]

__all__ = ["Cookies", "Namespace", "VersionTuple"]
