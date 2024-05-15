#!/usr/bin/env python3
''' A python script
'''
import redis
import uuid
from typing import Any, Callable, Union



class Cache:
    def __init__(self):
        """Initialize the Cache with a Redis client and flush the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the given data in Redis with a random key and return the key.

        Args:
            data: The data to be stored in Redis.

        Returns:
            str: The key under which the data is stored.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
