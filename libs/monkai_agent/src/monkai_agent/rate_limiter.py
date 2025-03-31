import time
from threading import Lock
from collections import deque
from typing import Optional

class RateLimiter:
    """A thread-safe rate limiter using the token bucket algorithm."""
    
    def __init__(self, max_calls: int, time_window: float):
        """
        Initialize the rate limiter.
        
        Args:
            max_calls: Maximum number of calls allowed in the time window
            time_window: Time window in seconds
        """
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = deque()
        self.lock = Lock()
        
    def acquire(self, block: bool = True) -> bool:
        """
        Acquire a token from the rate limiter.
        
        Args:
            block: Whether to block until a token is available
            
        Returns:
            True if a token was acquired, False otherwise
        """
        with self.lock:
            now = time.time()
            
            # Remove expired timestamps
            while self.calls and now - self.calls[0] >= self.time_window:
                self.calls.popleft()
                
            if len(self.calls) < self.max_calls:
                self.calls.append(now)
                return True
                
            if not block:
                return False
                
            # Calculate sleep time
            sleep_time = self.time_window - (now - self.calls[0])
            time.sleep(sleep_time)
            
            # Try again after sleeping
            return self.acquire(block=False)
            
    def release(self):
        """Release is a no-op for this implementation."""
        pass 