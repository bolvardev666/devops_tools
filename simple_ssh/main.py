import asyncio
import time
from os.path import exists

import asyncssh
from contextlib import asynccontextmanager

class SSHClient:
    def __init__(self):
        self.host = '1.1.1.1'
        self.port = 22
        self.user = 'root'
        self.password = ''

    @asynccontextmanager
    async def connect_ssh(self):
        try:
            async with asyncssh.connect(
                host=self.host,
                port=self.port,
                username=self.user,
                password=self.password,
                known_hosts=None
            ) as conn:
                yield conn
        except asyncssh.Error as e:
            raise e


    async def run_command(self, command) -> str:
        async with self.connect_ssh() as conn:
            result = await conn.run(command,check=True)
            return result.stdout






ssh_client = SSHClient()


while True:
    command = input("\n#: ")
    if command in ['exit', 'quit','\\q',':q']:
        break
    print(asyncio.run(ssh_client.run_command(command)).strip('\n'), end='')
    time.sleep(1)





