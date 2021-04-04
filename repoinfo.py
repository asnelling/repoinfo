#!/usr/bin/env python3

import argparse
import asyncio

import aiohttp


async def main():
    parser = argparse.ArgumentParser(description="Fetch git repository info for each repository given.")
    parser.add_argument('repositories', nargs='+', help='GitHub repos (e.g.: username/repo)')
    args = parser.parse_args()

    headers = {
        'Accept': 'application/vnd.github.v3+json',
    }
    prefix = 'https://api.github.com/repos/'

    async with aiohttp.ClientSession(headers=headers) as session:
        print("NAME                                               WATCHERS FORKS    SIZE")
        for repo in args.repositories:
            repo = repo.replace("https://github.com/", "")
            async with session.get(prefix + repo) as response:
                data = await response.json()
                size = data.get('size', 0)
                watchers = data.get('watchers', 0)
                forks = data.get('forks', 0)
                full_name = data.get('full_name', repo)
                print(f"{full_name:50} {watchers:8} {forks:8} {size:20}")


if __name__ == "__main__":
    asyncio.run(main())