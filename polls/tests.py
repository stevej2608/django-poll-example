import asyncio
import os
import sys
import datetime
from functools import partial

from channels.testing import ChannelsLiveServerTestCase
from channels.testing.live import make_application
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from django.db import connections
from django.utils import timezone
from django.test.utils import modify_settings

from playwright.sync_api import sync_playwright
from reactpy_django.utils import strtobool

from .models import Question, Choice

GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS", "False")
CLICK_DELAY = 250 if strtobool(GITHUB_ACTIONS) else 25  # Delay in miliseconds.


async def create_question(question_text, choices, days=30):

    @sync_to_async
    def _create_question(question_text, days):
        return Question.objects.create(
            question_text="What is the capital of France?",
            pub_date=timezone.now()
        )

    @sync_to_async
    def _create_choice(question, choice):
        return Choice.objects.create(
            choice_text=choice,
            question=question,
            votes = 0
        )


    time = timezone.now() + datetime.timedelta(days=days)
    question = await _create_question(question_text, time)

    for choice in choices:
        await _create_choice(question, choice)

    return question


class ComponentTests(ChannelsLiveServerTestCase):
    from django.db import DEFAULT_DB_ALIAS
    from reactpy_django import config

    databases = {"default"}

    @classmethod
    def setUpClass(cls):
        # Repurposed from ChannelsLiveServerTestCase._pre_setup
        for connection in connections.all():
            if cls._is_in_memory_db(cls, connection):
                raise ImproperlyConfigured(
                    "ChannelLiveServerTestCase can not be used with in memory databases"
                )
        cls._live_server_modified_settings = modify_settings(
            ALLOWED_HOSTS={"append": cls.host}
        )
        cls._live_server_modified_settings.enable()
        get_application = partial(
            make_application,
            static_wrapper=cls.static_wrapper if cls.serve_static else None,
        )
        cls._server_process = cls.ProtocolServerProcess(cls.host, get_application)
        cls._server_process.start()
        cls._server_process.ready.wait()
        cls._port = cls._server_process.port.value


        # Open a Playwright browser window
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        cls.playwright = sync_playwright().start()
        headless = strtobool(os.environ.get("PLAYWRIGHT_HEADLESS", GITHUB_ACTIONS))
        cls.browser = cls.playwright.chromium.launch(headless=bool(headless))
        # cls.page = cls.browser.new_page()

    @classmethod
    def tearDownClass(cls):
        from reactpy_django import config

        # Close the Playwright browser
        cls.playwright.stop()

        # Repurposed from ChannelsLiveServerTestCase._post_teardown
        cls._server_process.terminate()
        cls._server_process.join()
        cls._live_server_modified_settings.disable()
        for db_name in {"default", config.REACTPY_DATABASE}:
            call_command(
                "flush",
                verbosity=0,
                interactive=False,
                database=db_name,
                reset_sequences=False,
            )

    def new_page(self, slug:str):

        server_url = self.live_server_url

        class MessageWriter(object):

            def __init__(self, slug):
                self._page = ComponentTests.browser.new_page()
                self._page.goto(f"{server_url}{slug}")

            def __enter__(self):
                return self._page

            def __exit__(self, *args):
                self._page.close()

        return MessageWriter(slug)


    def test_no_questions(self):
        with self.new_page('/polls/') as page:
            elem = page.locator("h2")
            elem.wait_for()
            self.assertEqual("No polls available.", elem.text_content())


    def test_question(self):

        # Add test question to the database

        asyncio.run(create_question("What is the capital of France?", ['London', 'Paris', 'New York']))

        with self.new_page('/polls/') as page:

            # Confirm test the question is listed and select it for voting
        
            elem = page.locator("p")
            elem.wait_for()
            self.assertEqual("What is the capital of France?", elem.text_content())
            page.locator('"Vote Now"').click()

            # Wait for the question detils page to appear

            vote_btn = page.locator('"Vote"')
            vote_btn.wait_for()

            # Check the first choice (London) radion button and vote

            paris_checkbox = page.query_selector("input[value='1']")
            assert paris_checkbox
            paris_checkbox.click()
            vote_btn.click()

            # We should have been returned to the index page, select the results page

            results_btn = page.locator('"Results"')
            results_btn.wait_for()
            results_btn.click()

            # Wait for results page

            back_btn = page.locator('"Back To Polls"')
            back_btn.wait_for()

            # confirm the London vote

            results = page.query_selector("ul.results")
            assert results
            assert results.text_content() == 'London1 voteParis0 votesNew York0 votes'
