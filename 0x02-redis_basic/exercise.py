#!/usr/bin/env python3
"""this is module for redis"""
from functools import wraps
import redis
from typing import Union, Callable
import uuid


class Cache:
    """main class for redis"""
    def __init__(self):
        """init method for redis"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @staticmethod
    def count_calls(func: Callable) -> Callable:
        """count calls method for redis"""
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            """wrapper method for redis"""
            key = func.__qualname__
            count = self._redis.incr(key)
            self._redis.set(key, count)
            return func(self, *args, **kwargs)
        return wrapper
    
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """sotre method for redis"""
        key = str(uuid.uuid4())
        if isinstance(data, str):
            self._redis.set(key, data)
        elif isinstance(data, bytes):
            self._redis.set(key, data)
        elif isinstance(data, int):
            self._redis.set(key, str(data))
        elif isinstance(data, float):
            self._redis.set(key, str(data))
        return key
    
    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float]:
        """get method for redis"""
        value = self._redis.get(key)
        if value is None:
            return None
        if fn is not None:
            return fn(value)
        else:
            return value

    def get_str(self, key: str) -> str:
        """get str method for redis"""
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """get int method for redis"""
        return self.get(key, int)
