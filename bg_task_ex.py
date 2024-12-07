from fastapi import FastAPI, BackgroundTasks
from time import sleep
import time
import asyncio

app = FastAPI()


# Simulating slow operations
async def send_welcome_email(user_email: str):
    # Pretend this takes 3 seconds to send an email
    await asyncio.sleep(3)
    print(f"✉️ Welcome email sent to {user_email}")

async def update_analytics(user_email: str):
    # Pretend this takes 2 seconds to update analytics
    await asyncio.sleep(2)
    print(f"📊 Analytics updated for {user_email}")

async def notify_team(user_email: str):
    # Pretend this takes 1 second to notify team
    await asyncio.sleep(1)
    print(f"👥 Team notified about new user: {user_email}")



# BAD WAY: Making user wait for everything
@app.post("/signup-slow")
async def signup_without_background_tasks(email: str):
    start_time = time.time()

    # User has to wait for ALL of these to complete
    await send_welcome_email(email)      # 3 seconds
    await update_analytics(email)        # 2 seconds
    await notify_team(email)            # 1 second
    
    total_time = time.time() - start_time

    return {
        "message": "Signup complete! But that took 6 seconds 😭",
        "email": email,
        "time_taken": f"{total_time:.1f} seconds",
    }



# GOOD WAY: Using background tasks
@app.post("/signup-fast")
async def signup_with_background_tasks(email: str, background_tasks: BackgroundTasks):

    start_time = time.time()

    # Add tasks to be run in the background
    background_tasks.add_task(send_welcome_email, email)
    background_tasks.add_task(update_analytics, email)
    background_tasks.add_task(notify_team, email)
    

    total_time = time.time() - start_time

    return {
        "message": "Signup complete! That was instant! 🚀",
        "email": email,
        "time_taken": f"{total_time:.1f} seconds",
    }


