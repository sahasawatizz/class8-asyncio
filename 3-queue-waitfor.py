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

#consume work
async def consumer(queue):
    print(f'{time.ctime()} Consumer: Running')
    #consume work
    while True:
        #get a unit of work
        try:
            get_await = queue.get()
            item = await asyncio.wait_for(get_await,0.5)
        except asyncio.TimeoutError:
            print(f'{time.ctime()} Consumer: gave up waiting')
            continue
        if item is None:
            break
        print(f'{time.ctime()} >got {item}')
    print(f'{time.ctime()} Consumer: Done')

async def main ():
    queue = asyncio.Queue()
    await asyncio.gather(producer(queue),consumer(queue))

asyncio.run(main())
