import client
import boat
import asyncio


async def main(n, t):
    await boat.Server(n, t).run()
    await client.main(t)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    n = 3
    t = 1
    loop.run_until_complete(boat.Server(n, t).run())
    loop.run_until_complete(client.main(t))
