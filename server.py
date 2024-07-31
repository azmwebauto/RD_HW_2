import asyncio
import logging
import random


class Server(asyncio.Protocol):
    def __init__(self):
        self.clients = []

    def connection_made(self, transport):
        self.transport = transport
        peername = transport.get_extra_info('peername')
        print(f"Connection from {peername}")
        self.clients.append(transport)

    def connection_lost(self, exc):
        print("Connection lost")
        try:
            self.clients.remove(self.transport)
        except Exception as e:
            logging.exception(e)


async def generate_weather_data(server_protocol):
    while True:
        data = await create_data()
        for client in server_protocol.clients:
            try:
                client.write(data.encode())
            except Exception as e:
                logging.exception(e)
                server_protocol.clients.remove(client)
                client.close()  # Ensure the transport is closed

        await asyncio.sleep(random.randint(1, 3))


async def create_data():
    temperature = random.uniform(-10, 35)
    humidity = random.uniform(0, 100)
    data = f"Humidity: {humidity:.2f} %, Temperature: {temperature:.2f} C"
    # print(data)
    return data


async def main():
    loop = asyncio.get_running_loop()
    server_protocol = Server()

    server = await loop.create_server(
        lambda: server_protocol,
        '127.0.0.1', 8000
    )
    print('Server started.')
    await asyncio.create_task(generate_weather_data(server_protocol))

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
