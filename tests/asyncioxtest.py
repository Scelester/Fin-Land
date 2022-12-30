import asyncio


async def main():
    print("Nothing")
    await asyncio.sleep(10)

loop = asyncio.new_event_loop()

asyncio.run_coroutine_threadsafe(main(), loop)