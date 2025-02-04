from bot import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.config import Config
from bot.utils import process_new_pairs

if __name__ == "__main__":
    app = Bot()
    sc = AsyncIOScheduler()

    seconds = 1

    sc.add_job(
        process_new_pairs,
        args=(app,),
        trigger="interval",
        seconds=seconds,
        max_instances=1,
    )

    sc.start()
    app.run()
