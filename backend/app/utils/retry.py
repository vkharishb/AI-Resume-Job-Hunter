from collections.abc import Awaitable, Callable
from typing import TypeVar

from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

T = TypeVar("T")


def external_retry(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
    return retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        retry=retry_if_exception_type((TimeoutError, ConnectionError)),
    )(func)
