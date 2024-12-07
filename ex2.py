from fastapi import FastAPI
import time

app = FastAPI()

# Our super simple cache - just a list of strings
# In real apps you'd use Database - example my email validation tool, show how I cache
movie_cache = []

# Simulate a slow database query
def get_movie_from_database(movie_name: str) -> str:
    """Pretend this is a slow database query"""
    time.sleep(2)  # Pretend this takes 2 seconds
    return f"Found movie: {movie_name}"

# Version 1: No caching (slow every time)
@app.get("/movie/slow/{movie_name}")
async def get_movie_slow(movie_name: str):
    """Get movie without using cache"""
    # This will be slow every single time!
    result = get_movie_from_database(movie_name)
    return {
        "result": result,
        "took": "2 seconds",
        "from_cache": False
    }

# Version 2: With simple caching (fast after first time)
@app.get("/movie/fast/{movie_name}")
async def get_movie_fast(movie_name: str):
    """Get movie using simple cache"""
    # First, check if movie is in our cache
    if movie_name in movie_cache:
        return {
            "result": f"Found movie: {movie_name}",
            "took": "0 seconds",
            "from_cache": True
        }
    
    # If not in cache, get it the slow way
    result = get_movie_from_database(movie_name)
    
    # Save in cache for next time
    movie_cache.append(movie_name)
    
    return {
        "result": result,
        "took": "2 seconds",
        "from_cache": False
    }

# See what's in our cache
@app.get("/cache/list")
async def show_cache():
    """Show what's in our cache"""
    return {
        "cached_movies": movie_cache,
        "total_cached": len(movie_cache)
    }