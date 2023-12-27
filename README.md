# Google Maps location share API

A fully asynchronous API client for Google Map's location share functionality.

## Install

You must install the following libraries:
- `aiohttp` (asynchronous HTTP)
- `playwright` (asynchronous webdriver)
- `undetected-playwright-patch` ([Bypass Google's bot detection](https://github.com/kaliiiiiiiiii/undetected-playwright-python))
- `pickle` (session persistence)

It is recommended to install the following libraries:
- `asyncio` (Running asynchronous code)

Run `pip install gmaps-locationshare-api` to install.

## How it works

Playwright obtains a session via a manual log-in attempt by the user.
The client also has the ability to persist a session between different instances by
locally caching session cookies, and session refresh capabilities.

The client then uses said session to call Google's internal location share API to obtain relevant data.

## Documentation

Sample usages are in `main.py`

`class Client(persist: bool = False, persist_directory: str = None)`
- `persist`: Whether or not the session is locally cached to be used by subsequent invocation of `Client` in the same or a different program instance.
- `persist_directory`: Cache location. Note that the cache location must be consistent for all clients that wishes to use the cached session.

`Client.refresh_session()`: Refresh session cookies to prevent stale sessions.

`Client.get_data() -> [Person]`: Get current location share data. Each call represent one reading at the current time, it doesn't not contain historical readings.

Relevant type definitions are in `gmaps_locationshare_api/types.py`