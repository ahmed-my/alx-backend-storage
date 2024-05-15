#!/usr/bin/env python3
'''Module to obtain the HTML content of a particular URL.
'''
import requests
import redis
import time
from functools import wraps


# Initialize Redis client
redis_client = redis.StrictRedis(host='localhost',
                                 port=6379, db=0, decode_responses=True)


def cache_page(expiration=10):
    """
    Decorator to cache the page content for a given expiration time.

    Args:
        expiration (int): The time in seconds for cache content to be valid.

    Returns:
        decorator (function): The caching decorator.
    """
    def decorator(func):
        '''using the decorator
        '''
        @wraps(func)
        def wrapper(url, *args, **kwargs):
            '''using the wrapper
            '''
            cache_key = f"cache:{url}"
            count_key = f"count:{url}"

            # Check if the URL is already cached
            cached_content = redis_client.get(cache_key)
            if cached_content:
                # Increment the count for the URL
                redis_client.incr(count_key)
                return cached_content

            # If not cached, fetch the content and cache it
            result = func(url, *args, **kwargs)
            redis_client.setex(cache_key, expiration, result)
            redis_client.incr(count_key)
            return result
        return wrapper
    return decorator


@cache_page(expiration=10)
def get_page(url: str) -> str:
    """
    Fetch the HTML content of the given URL and return it.

    Args:
        url (str): The URL of the page to fetch.

    Returns:
        str: The HTML content of the page.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    response = requests.get(url)
    response.raise_for_status()  # Raise an HTTPError for bad responses
    return response.text


if __name__ == "__main__":
    # Testing the function
    test_url = "http://slowwly.robertomurray.co.uk/delay/5000/url/" \
        "https://www.example.com"
    print("Fetching URL for the first time...")
    print(get_page(test_url))

    time.sleep(1)  # Wait for 1 second

    print("Fetching URL for the second time (should be cached)...")
    print(get_page(test_url))
