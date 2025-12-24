import sys
import os
import pytest
from .utils.driver_factory import get_driver

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()
