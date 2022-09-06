import dis

from aioconsole import aprint
from classes import discordgateway
import asyncio




async def main():
    tokens = open("tokens.txt").read().splitlines()
    tasks = []
    for token in tokens:
        dg = discordgateway(token)
        task = asyncio.create_task(dg.simple_connect())
        tasks.append(task)

    await asyncio.gather(*tasks, return_exceptions=True)




def test():
    lines_seen = set()
    outfile = open("tokens.txt", "w")
    for line in open("false_tokens.txt", "r"):
        if line not in lines_seen:
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()

asyncio.run(main())
