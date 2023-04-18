import pytest

from tests.mocks.discord import MockGuild, MockMessage


@pytest.fixture()
def mock_message():
    return MockMessage(1234567890987654321, MockGuild(9876543210123456789))


@pytest.fixture()
def mock_message_without_guild():
    return MockMessage(1234567890987654321)
