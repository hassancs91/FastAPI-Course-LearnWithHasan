from fastapi import FastAPI
import time
import asyncio

app = FastAPI()


# Simulating a slow operation
def make_coffee():
    time.sleep(2)  # Pretend this takes 2 seconds
    return "☕ Coffee ready!"

def make_toast():
    time.sleep(3)  # Pretend this takes 3 seconds
    return "🍞 Toast ready!"


@app.get("/prepare-slow")
def prepare_breakfast_slow():

    start_time = time.time()
    
    # We wait for coffee to finish before starting toast
    coffee = make_coffee()
    toast = make_toast()
    
    total_time = time.time() - start_time
    
    return {
        "meals": [coffee, toast],
        "time_taken": f"{total_time:.1f} seconds"
    }



# asynchronous way 
async def async_make_coffee():
    await asyncio.sleep(2)
    return "☕ Coffee ready!"

async def async_make_toast():
    await asyncio.sleep(3)
    return "🍞 Toast ready!"



@app.get("/breakfast-fast")
async def prepare_breakfast_fast():
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

