from fastapi import FastAPI
import time

app = FastAPI()


# Simulate a slow database query that takes 2 seconds
def get_movie_from_database(movie_name: str):
    time.sleep(2) 
    return f"Found movie: {movie_name}"


# Version 1: No caching (slow every time)
@app.get("/movie/slow/{movie_name}")
async def get_movie_slow(movie_name: str):
    """Get movie without using cache"""
    # This will be slow every single time!
    start_time = time.time()

    result = get_movie_from_database(movie_name)

    total_time = time.time() - start_time

    return {
        "result": result,
        "time_taken": f"{total_time:.1f} seconds",
        "from_cache": False
    }



movie_cache = []

# Version 2: With simple caching (fast after first time)
@app.get("/movie/fast/{movie_name}")
async def get_movie_fast(movie_name: str):
    """Get movie using simple cache"""

    start_time = time.time()

    # First, check if movie is in our cache
    if movie_name in movie_cache:
        total_time = time.time() - start_time
        return {
            "result": f"Found movie: {movie_name}",
            "time_taken": f"{total_time:.1f} seconds",
            "from_cache": True
        }
    

    # If not in cache, get it the slow way
    result = get_movie_from_database(movie_name)
    
    # Save in cache for next time
    movie_cache.append(movie_name)


    total_time = time.time() - start_time
    
    return {
        "result": result,
        "time_taken": f"{total_time:.1f} seconds",
        "from_cache": False
    }


