from random import random
import asyncio
import time

async def producer(queue):
    print(f'{time.ctime()} Producer: Running')
    #generate work
    for i in range(10):
        #generate a value
        value = random()
        #block to simulate work
        await asyncio.sleep(value)
        #add to queue
        await queue.put(value)
    #send all done signal
    await queue.put(None)
    print(f'{time.ctime()} Producer: Done')

#coroutine to consume work
async def consumer(queue):
    print('Consumer: Running')
    #consume work
    while True:
        #get a unit of work with out blocking
        try:
            item = queue.get_nowait()
        except asyncio.QueueEmpty:
            print(f'{time.ctime()} Consumer: got nothing,waiting a while')
            await asyncio.sleep(0.5)
            continue
        #check for stop
        if item is None:
            break
        #report
        print(f'{time.ctime()} >got {item}')
    print(f'{time.ctime()} Consumer: Done')

async def main ():
    queue = asyncio.Queue()
    await asyncio.gather(producer(queue),consumer(queue))

asyncio.run(main())
