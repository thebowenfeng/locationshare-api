from gmaps_locationshare_api import Client
import asyncio


async def main():
    async with Client(persist=True) as c:
        print(await c.get_data())
        await c.refresh_session()
        print(await c.get_data())


asyncio.run(main())

