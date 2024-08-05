import asyncio


class Client(asyncio.Protocol):

    def connection_made(self, transport):
        self.transport = transport
        self.loop = asyncio.get_event_loop()
        self._checker = self.loop.create_task(self.check_connection())
        print("Connected to server")

    def data_received(self, data):
        print(f"Data received: {data.decode()}")

    def connection_lost(self, exc):
        print("The server closed the connection")
        self._checker.cancel()  # Cancel the periodic connection check task
        if exc:
            print(f"Connection lost with error: {exc}")
        else:
            print("Connection closed cleanly")
        self.transport.close()
        self.loop.stop()  # Stop the event loop

    async def check_connection(self):
        try:
            while True:
                # print('check connection here')
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            pass


async def main():
    loop = asyncio.get_running_loop()

    client = Client
    transport, protocol = await loop.create_connection(client, '127.0.0.1', 8000)

    try:
        await asyncio.Future()
    except Exception as e:
        print(f"Exception in main: {e}")
        transport.abort()
    finally:
        transport.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception:
        print("Client stopped")
