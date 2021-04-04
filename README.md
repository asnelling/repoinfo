# repoinfo

A simple CLI to retrieve various info (number of watchers, number of forks,
and size) for GitHub repositories.

## Usage

```Shell
./repoinfo.py [-h] repositories [repositories ...]
```

### Positional Arguments

- `repositories`: GitHub repos to get info for (in user/repo format)

### Optional Arguments

- `-h`, `--help`: show usage information

## Example

```Shell
$ ./repoinfo.py sindresorhus/awesome vinta/awesome-python timofurrer/awesome-asyncio herrjemand/awesome-webauthn
NAME                        WATCHERS FORKS SIZE
sindresorhus/awesome          156425 20318 1271
vinta/awesome-python           95518 18667 6596
timofurrer/awesome-asyncio      2918   228  116
herrjemand/awesome-webauthn      393    49  152
```

## Rate Limiting

The GitHub API imposes strict
[rate limiting](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting)
for unauthenticated requests. For increased limits, provide an
[OAuth2 key/secret](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#oauth2-keysecret)
in the `GH_CLIENT_ID` and `GH_CLIENT_SECRET` environment variables when running `repoinfo`.
