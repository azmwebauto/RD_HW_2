import asyncio


class Client(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        print("Connected to server")

    def data_received(self, data):
        print(f"Data received: {data.decode()}")

    def connection_lost(self, exc):
        print("The server closed the connection")
        self.transport.close()


async def main():
    loop = asyncio.get_running_loop()
    future = loop.create_future()

    transport, protocol = await loop.create_connection(Client, '127.0.0.1', 8000)

    try:
        await future
    except Exception:
        transport.abort()


if __name__ == '__main__':
    asyncio.run(main())
