#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import redis
import requests
from functools import wraps
from typing import Callable
import time


redis_store = redis.Redis()
'''The module-level Redis instance.
'''


def data_cacher(method: Callable) -> Callable:
    '''Caches the output of fetched data.
    '''
    @wraps(method)
    def invoker(url) -> str:
        '''The wrapper function for caching the output.
        '''
        redis_store.incr(f'count:{url}')
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return invoker


@data_cacher
def get_page(url: str) -> str:
    '''Returns the content of a URL after caching the request's response,
    and tracking the request.
    '''
    return requests.get(url).text


if __name__ == "__main__":
    test_url = "http://slowwly.robertomurray.co.uk/delay/5000/url/" \
        "https://www.example.com"

    # Measure the time taken for the first request
    start_time = time.time()
    print(get_page(test_url))
    print(f"Time taken for first request: {time.time() - start_time} seconds")

    # Measure the time taken for the second request
    start_time = time.time()
    print(get_page(test_url))
    print(f"Time taken for second request: {time.time() - start_time} seconds")
