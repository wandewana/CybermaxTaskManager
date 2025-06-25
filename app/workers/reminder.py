import asyncio
import logging
import sys
import os

# Add project root to the Python path to avoid circular import issues
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import json
import time
from app.db.redis import redis_client

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def reminder_worker():
    while True:
        now = int(time.time())
        # Get all tasks that are now due from Redis
        tasks = await redis_client.zrangebyscore("overdue_tasks_schedule", 0, now)

        for task_json in tasks:
            task = json.loads(task_json)
            logging.warning(f"Reminder: Task '{task['title']}' is overdue!")
            # Remove from schedule once processed
            await redis_client.zrem("overdue_tasks_schedule", task_json)

        await asyncio.sleep(10)

async def main():
    logging.info("Starting Redis-based reminder worker...")
    await reminder_worker()

if __name__ == "__main__":
    logging.info("Starting reminder worker...")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Reminder worker stopped.")
