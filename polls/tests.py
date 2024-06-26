import asyncio
import os
import sys
import datetime
from functools import partial

from channels.testing import ChannelsLiveServerTestCase
from channels.testing.live import make_application
from asgiref.sync import sync_to_async

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from django.db import connections
from django.utils import timezone
from django.test.utils import modify_settings
from django.urls import reverse
from django.contrib.auth import get_user_model

from playwright.sync_api import sync_playwright

from reactpy_django import config
from reactpy_django.utils import strtobool

from .models import Question, Choice


GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS", "True")
CLICK_DELAY = 250 if strtobool(GITHUB_ACTIONS) else 25  # Delay in miliseconds.


async def create_question(question_text, choices, days=30):

    @sync_to_async
    def _create_question(question_text, days):
        return Question.objects.create(
            question_text=question_text,
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


async def create_admin(request, user='admin', email='admin@example.com', password='superadmin'):
    User.objects.create_superuser(user, email=email, password=password)

    user = authenticate(username=user, password=password)

    if user is not None and user.is_superuser:
        login(request, user)
        # User is now logged in
        return True
    else:
        # Authentication failed or user is not a superuser
        return False



# Slimmed down version of test harness used by reactpy-django
# See https://github.com/reactive-python/reactpy-django/blob/main/tests/test_app/tests/test_components.py

class ComponentTests(ChannelsLiveServerTestCase):

    databases = {"default"}

    @classmethod
    def setUpClass(cls):

        # Repurposed from ChannelsLiveServerTestCase._pre_setup

        for connection in connections.all():
            if cls._is_in_memory_db(cls, connection): # type: ignore
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

        # Create an admin user

        cls.admin_user = get_user_model().objects.create_superuser( # type: ignore
            username='admin', email='admin@example.com', password='adminpass'
        )


        # Open a Playwright browser window

        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

        cls.playwright = sync_playwright().start()
        headless = strtobool(os.environ.get("PLAYWRIGHT_HEADLESS", GITHUB_ACTIONS))
        cls.browser = cls.playwright.chromium.launch(
            headless=bool(headless),
            timeout=3000
            )


    @classmethod
    def tearDownClass(cls):

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

    def _pre_setup(self):
        """Handled manually in `setUpClass` to speed things up."""

    def _post_teardown(self):
        """Handled manually in `tearDownClass` to prevent TransactionTestCase from doing
        database flushing. This is needed to prevent a `SynchronousOnlyOperation` from
        occurring due to a bug within `ChannelsLiveServerTestCase`."""


    def setUp(self):
        pass

    def wait_page_stable(self, page):
        page.wait_for_load_state("networkidle")
        page.wait_for_load_state("domcontentloaded")


    def page_goto(self, page, slug:str):
        server_url = self.live_server_url
        page.goto(f"{server_url}{slug}")
        self.wait_page_stable(page)


    def new_page(self, slug:str = "/"):

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


    def login_as_admin(self, page):

        self.page_goto(page, '/admin/')

        # https://playwright.dev/python/docs/auth

        page.get_by_label("username").fill("admin")
        page.get_by_label("password").fill("adminpass")
        page.locator("[type=submit]").click()


    def test_404(self):
        with self.new_page('/polls/99/') as page:
            elem = page.locator("h1")
            elem.wait_for()
            self.assertEqual("404 Not Found", elem.text_content())

    def test_401(self):
        with self.new_page('/polls/1/results/') as page:
            elem = page.locator("h1")
            elem.wait_for()
            self.assertEqual("401 Authorization Required", elem.text_content())


    def test_no_questions(self):
        with self.new_page('/polls/') as page:
            elem = page.locator("h2")
            elem.wait_for()
            self.assertEqual("No polls available.", elem.text_content())


    def test_question(self):

        # Add test question to the database

        asyncio.run(create_question("What is the capital of France?", ['London', 'Paris', 'New York']))
        asyncio.run(create_question("What is the capital of Germany?", ['London', 'Berlin', 'New York']))


        with self.new_page(reverse("polls:index")) as page:

            # # We need to login as amin because we're going to 
            # # access the protected results page


            # self.login_as_admin(page)

            self.page_goto(page, reverse("polls:index"))

            # Confirm test the question is listed and select it for voting

            elem = page.locator("p").locator("nth=1")
            elem.wait_for()
            self.assertEqual("What is the capital of France?", elem.text_content())
            page.locator('"Vote Now"').locator("nth=1").click()

            # Wait for the question details page to appear

            vote_btn = page.locator('"Vote"')
            vote_btn.wait_for()

            # Check the first choice (London) radio button and vote

            paris_checkbox = page.query_selector("input[value='2']")
            assert paris_checkbox
            paris_checkbox.click()
            vote_btn.click()

            # We should have been returned to the index
            # page, select the results page. This will fail because 
            # we're not authorized to look at the results page

            results_btn = page.locator('"Results"').locator("nth=1")
            results_btn.wait_for()
            results_btn.click()

            # Wait for not authorized

            elem = page.locator("h1")
            elem.wait_for()
            self.assertEqual("401 Authorization Required", elem.text_content())

            # We need to login as admin to access the results page

            self.login_as_admin(page)
            self.page_goto(page, reverse("polls:index"))

            # Goto the results page for the 'capital of France?' question

            results_btn = page.locator('"Results"').locator("nth=1")
            results_btn.click()

            self.wait_page_stable(page)

            # Confirm the Paris vote

            results = page.query_selector("ul.results")
            assert results
            assert results.text_content() == 'London0 votesParis1 voteNew York0 votes'
