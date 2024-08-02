import asyncio
import random


def create_data() -> str:
    temperature = random.uniform(-10, 35)
    humidity = random.uniform(0, 100)
    data = f"Humidity: {humidity:.2f} %, Temperature: {temperature:.2f} C"
    # print(data)
    return data


class Server(asyncio.Protocol):
    clients = []

    def connection_made(self, transport):
        self.transport = transport
        self.clients.append(self.transport)
        peername = self.transport.get_extra_info('peername')
        print(f"Connection from {peername}")

    def connection_lost(self, exc):
        self.clients.remove(self.transport)
        print("Connection lost")

    @classmethod
    def generate_weather_data(cls):
        data = create_data()
        for client in cls.clients:
            client.write(data.encode())


async def main():
    loop = asyncio.get_running_loop()
    server_protocol = Server

    await loop.create_server(server_protocol, '127.0.0.1', 8000)
    print('Server started.')
    while True:
        server_protocol.generate_weather_data()
        await asyncio.sleep(random.randint(1, 3))


if __name__ == '__main__':
    asyncio.run(main())
