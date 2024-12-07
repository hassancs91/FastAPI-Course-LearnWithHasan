from fastapi import FastAPI
import asyncio
import time

app = FastAPI()

# Simulating a slow operation
def make_coffee():
    time.sleep(2)  # Pretend this takes 2 seconds
    return "☕ Coffee ready!"

def make_toast():
    time.sleep(3)  # Pretend this takes 3 seconds
    return "🍞 Toast ready!"



# Traditional synchronous way - Total time: 5 seconds
@app.get("/breakfast-sync")
def prepare_breakfast_sync():
    start_time = time.time()
    
    # We wait for coffee to finish before starting toast
    coffee = make_coffee()
    toast = make_toast()
    
    total_time = time.time() - start_time
    return {
        "meals": [coffee, toast],
        "time_taken": f"{total_time:.1f} seconds"
    }

# Modern asynchronous way - Total time: 3 seconds
async def async_make_coffee():
    await asyncio.sleep(2)  # Simulating async database query
    return "☕ Coffee ready!"

async def async_make_toast():
    await asyncio.sleep(3)  # Simulating async database query
    return "🍞 Toast ready!"

@app.get("/breakfast-async")
async def prepare_breakfast_async():
    start_time = time.time()
    
    # Start both tasks at the same time!
    coffee_task = async_make_coffee()
    toast_task = async_make_toast()
    
    # Wait for both to complete
    coffee, toast = await asyncio.gather(coffee_task, toast_task)
    
    total_time = time.time() - start_time
    return {
        "meals": [coffee, toast],
        "time_taken": f"{total_time:.1f} seconds"
    }