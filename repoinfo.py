#!/usr/bin/env python3

import argparse
import asyncio
import os
import sys

import aiohttp


def get_auth():
    client_id = os.getenv("GH_CLIENT_ID")
    client_secret = os.getenv("GH_CLIENT_SECRET")

    if client_id and client_secret:
        return aiohttp.BasicAuth(client_id, client_secret)

    return None


async def main():
    parser = argparse.ArgumentParser(
        description="Fetch git repository info for each repository given."
    )
    parser.add_argument(
        "repositories", nargs="+", help="GitHub repos (e.g.: username/repo)"
    )
    parser.add_argument(
        "-s",
        "--sort",
        choices=["name", "watchers", "forks", "size"],
        help="field to sort output on, where FIELD is one of: name, watchers, forks, size",
        metavar="FIELD",
    )
    args = parser.parse_args()

    headers = {
        "Accept": "application/vnd.github.v3+json",
    }
    prefix = "https://api.github.com/repos/"

    async with aiohttp.ClientSession(headers=headers, auth=get_auth()) as session:
        repos = []
        for repo in args.repositories:
            repo = repo.replace("https://github.com/", "")
            async with session.get(prefix + repo) as response:
                if response.status != 200:
                    print(
                        f"HTTP Error {response.status}: {response.reason}",
                        file=sys.stderr,
                    )
                    body = await response.text()
                    if body:
                        print(body, file=sys.stderr)
                    continue

                data = await response.json()
                size = data.get("size", 0)
                watchers = data.get("watchers", 0)
                forks = data.get("forks", 0)
                name = data.get("full_name", repo)
                repos.append(
                    {
                        "name": name,
                        "size": size,
                        "watchers": watchers,
                        "forks": forks,
                    }
                )

        if args.sort:
            repos = sorted(repos, key=lambda repo: repo[args.sort])

        print(
            "NAME                                               WATCHERS FORKS    SIZE"
        )

        for repo in repos:
            print("{name:50} {watchers:8} {forks:8} {size:20}".format(**repo))


if __name__ == "__main__":
    asyncio.run(main())
