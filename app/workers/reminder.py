import asyncio
import logging
import sys
import os

# Add project root to the Python path to avoid circular import issues
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.db.session import AsyncSessionLocal as SessionLocal
from app.db.crud import get_overdue_tasks

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def check_overdue_tasks():
    """
    Checks for overdue tasks and logs them.
    """
    logging.info("Worker running: Checking for overdue tasks...")
    db = SessionLocal()
    try:
        overdue_tasks = await get_overdue_tasks(db)
        if not overdue_tasks:
            logging.info("No overdue tasks found.")
        else:
            logging.info(f"Found {len(overdue_tasks)} overdue tasks.")
            for task in overdue_tasks:
                logging.warning(
                    f"Reminder: Task '{task.title}' for user '{task.owner.email}' was due on {task.due_date}."
                )
    finally:
        await db.close()

async def main():
    """
    Main worker loop that runs periodically.
    """
    while True:
        await check_overdue_tasks()
        logging.info("Worker sleeping for 30 seconds...")
        await asyncio.sleep(30)

if __name__ == "__main__":
    logging.info("Starting reminder worker...")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Reminder worker stopped.")
