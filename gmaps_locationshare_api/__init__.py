from aiohttp import ClientSession
from undetected_playwright.async_api import async_playwright
from gmaps_locationshare_api.utils import _parse_raw_data
import os
import pickle


class Client:
    def __init__(self, persist: bool = False, persist_directory=None):
        self._session = None
        self.persist = persist
        self.persist_directory = os.getcwd() if persist_directory is None else persist_directory

    async def __aenter__(self):
        await self._login()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.close()

    async def _login(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False, args=["--disable-blink-features=AutomationControlled"])
            context = await browser.new_context()
            page = await context.new_page()
            to_login = False
            if not self.persist:
                to_login = True
            else:
                if os.path.isfile(self.persist_directory + "/cookies.pkl"):
                    with open(self.persist_directory + "/cookies.pkl", "rb") as fd:
                        cookies = pickle.load(fd)
                    await context.add_cookies(cookies)
                else:
                    to_login = True

            await page.goto("https://www.google.com/maps")
            if not to_login:
                try:
                    await page.is_visible("#gb > div > div > div.gb_Pd.gb_Xf.gb_D > div.gb_b.gb_v.gb_Xf.gb_D > div",
                                          timeout=5000)
                except TimeoutError:
                    to_login = True

            if to_login:
                try:
                    await page.click("#gb_70", timeout=10000)
                except TimeoutError:
                    raise Exception("Unable to login. Please restart")
                await page.wait_for_url("https://www.google.com/maps**")

            cookies = await context.cookies("https://www.google.com")
            self._session = ClientSession(cookies={k: v for k, v in list(map(lambda x: (x["name"], x["value"]),
                                                                             cookies))})
            if self.persist:
                with open(f"{self.persist_directory}/cookies.pkl", "wb") as fd:
                    pickle.dump(cookies, fd)

    async def refresh_session(self):
        to_login = False
        async with async_playwright() as p:
            if os.path.isfile(self.persist_directory + "/cookies.pkl"):
                browser = await p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
                context = await browser.new_context()
                with open(self.persist_directory + "/cookies.pkl", "rb") as fd:
                    cookies = pickle.load(fd)
                await context.add_cookies(cookies)
                page = await context.new_page()

                await page.goto("https://www.google.com/maps")
                try:
                    await page.is_visible("#gb > div > div > div.gb_Pd.gb_Xf.gb_D > div.gb_b.gb_v.gb_Xf.gb_D > div",
                                          timeout=5000)
                    cookies = await context.cookies("https://www.google.com")
                    await self._session.close()
                    self._session = ClientSession(cookies={k: v for k, v in list(map(lambda x: (x["name"], x["value"]),
                                                                                     cookies))})
                    if self.persist:
                        with open(f"{self.persist_directory}/cookies.pkl", "wb") as fd:
                            pickle.dump(cookies, fd)
                except TimeoutError:
                    to_login = True
            else:
                to_login = True
        if to_login:
            print("Warning: Unable to automatically refresh session. Defaulted to manual login")
            await self._login()

    async def _get_raw_data(self):
        payload = {'authuser': 2,
                   'hl': 'en',
                   'gl': 'us',
                   'pb': ('!1m7!8m6!1m3!1i14!2i8413!3i5385!2i6!3x4095'
                          '!2m3!1e0!2sm!3i407105169!3m7!2sen!5e1105!12m4'
                          '!1e68!2m2!1sset!2sRoadmap!4e1!5m4!1e4!8m2!1e0!'
                          '1e1!6m9!1e12!2i2!26m1!4b1!30m1!'
                          '1f1.3953487873077393!39b1!44e1!50e0!23i4111425')}
        res = await self._session.get("https://www.google.com/maps/rpc/locationsharing/read", params=payload)
        return await res.text()

    async def get_data(self):
        return _parse_raw_data(await self._get_raw_data())
