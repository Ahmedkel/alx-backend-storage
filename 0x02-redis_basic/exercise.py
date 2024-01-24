#!/usr/bin/env python3
"""this is module for redis"""
from functools import wraps
import redis
from typing import Union, Callable, Optional, List
import uuid


def count_calls(method: Callable) -> Callable:
    """count calls method for redis"""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper method for redis"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """call history method for redis"""
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper method for redis"""
        self._redis.rpush(inputs, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(result))
        return result
    return wrapper


def replay(redis_instance: redis.Redis, method: Callable) -> List[str]:
    """replay method for redis"""
    method_name = method.__qualname__

    input_key = method_name + ":inputs"
    output_key = method_name + ":outputs"

    input_history = redis_instance.lrange(input_key, 0, -1)
    output_history = redis_instance.lrange(output_key, 0, -1)

    print(f"{method_name} was called {len(input_history)} times:")
    for input_data, output_data in zip(input_history, output_history):
        print(f"{method_name}(*{input_data.decode('utf-8')}) -> "
              f"{output_data.decode('utf-8')}")


class Cache:
    """main class for redis"""
    def __init__(self):
        """init method for redis"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """store method for redis"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """get method for redis"""
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """get str method for redis"""
        data = self._redis.get(key)
        return data.decode("utf-8")

    def get_int(self, key: str) -> int:
        """get int method for redis"""
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0
        return value
