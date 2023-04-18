from curator.strings import construct_permalink


def test_construct_permalink(mock_message):
    permalink = construct_permalink(mock_message, 1000000000000000000)
    assert (
        permalink
        == "https://discord.com/channels/9876543210123456789/1000000000000000000/1234567890987654321"
    )


def test_construct_permalink_without_guild(mock_message_without_guild):
    permalink = construct_permalink(mock_message_without_guild, 1000000000000000000)
    assert permalink is None
