from random import random
import asyncio
import time

async def producer(queue,id):
    print(f'{time.ctime()} Producer: Running')
    for i in range(10):
        value = random()
        await asyncio.sleep((id+1)*0.1)
        await queue.put(value)
    print(f'{time.ctime()} Producer{id}: Done')

async def consumer(queue):
    print(f'{time.ctime()} Consumer: Running')
    while True:
        item = await queue.get()
        print(f'{time.ctime()}>got{item}')
        if item:
            await asyncio.sleep(item)
        queue.task_done()
async def main ():
    queue = asyncio.Queue(2)
    _ =asyncio.create_task(consumer(queue))
    producers = [producer(queue,i) for i in range(5)]
    await asyncio.gather(*producers)
    await queue.join()

asyncio.run(main())

