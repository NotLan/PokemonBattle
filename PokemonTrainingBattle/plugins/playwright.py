import inspect
import logging
import os
from abc import ABC
from pathlib import Path
from typing import Any, List, Optional

import pytest
from playwright.sync_api import ConsoleMessage, Page, Request, Response

logger = logging.getLogger(__name__)


def _function_has_argument(function: Any, argument: str) -> bool:
    return argument in inspect.signature(function).parameters


_logger_supports_attachments = _function_has_argument(logger.warning, "attachment")
_failed_node_ids = []


class AbstractPage(ABC):
    critical_elements: Optional[List] = []
    url = ""

    def __init__(self, page: Page, critical_elements: Optional[List] = None, url: Optional[str] = None):
        self.page = page
        if critical_elements:
            self.critical_elements = critical_elements
        if url:
            self.url = url

    def navigate(self):
        assert self.url, "No url set to navigate to"
        self.page.goto(self.url)


def log_screenshot(page: Page, nodeid: str):
    screenshot_dir = Path(os.getenv("SCREENSHOT_DIR", os.getcwd()))
    screenshot_dir.mkdir(exist_ok=True)
    filename = f"{slugify(nodeid)}.png"
    screenshot = page.screenshot(path=str(screenshot_dir / filename))
    if _logger_supports_attachments:
        try:
            # noinspection PyArgumentList
            logger.warning(
                f"Attached file: {filename}", attachment={"name": filename, "data": screenshot, "mime": "image/png"}  # type: ignore
            )
        except BaseException as e:
            logger.exception("Something went wrong while logging screenshot to reportportal", exc_info=e)


def tracing_start(page: Page):
    """
    This function starts the tracing and enables Screenshots/Snapshots
    """
    page.context.tracing.start(
        screenshots=True,
        snapshots=True,
    )


def tracing_stop(page: Page, nodeid: str, save: bool):
    """
    This function stops the tracing and, depending on pass/failure, sets a path for the .zip to be created
    """
    tracing_dir = Path(os.getenv("TRACING_DIR", os.getcwd()))
    tracing_dir.mkdir(exist_ok=True)
    filename = f"{slugify(nodeid)}.zip"
    path = str(tracing_dir / filename)
    if save:
        page.context.tracing.stop(path=path)
        if _logger_supports_attachments:
            try:
                with open(path, "rb") as f:
                    # noinspection PyArgumentList
                    logger.warning(
                        f"Attached file: {filename}",
                        attachment={"name": filename, "data": f.read(), "mime": "application/zip"},  # type: ignore
                    )
            except BaseException as e:
                logger.exception("Something went wrong while logging trace zip to reportportal", exc_info=e)
    else:
        page.context.tracing.stop()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: Any, call: Any):
    outcome = yield
    result = outcome.get_result()
    if call.when == "call":
        if result.failed:
            _failed_node_ids.append(item.nodeid)
        if call.excinfo is not None and "page" in item.funcargs:
            page = item.funcargs["page"]
            log_screenshot(page, item.nodeid)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_setup(item: Any):
    yield
    if "page" in item.funcargs:
        page = item.funcargs["page"]
        page.on("request", on_request)
        page.on("response", on_response)
        page.on("console", on_console)


def on_request(request: Request):
    pass


def on_response(response: Response):
    if response.status >= 400:
        logging.warning(f"network response: {response.status} {response.url}")


def on_console(msg: ConsoleMessage):
    if msg.type == "error":
        logging.warning(f"console.error: {msg.text}")


@pytest.fixture(scope="function")
def enable_tracing(page, request: Any):
    """
    This fixture can be added to a test to enable tracing for better triaging
    """
    tracing_start(page)
    yield
    tracing_stop(page, request.node.nodeid, request.node.nodeid in _failed_node_ids)
