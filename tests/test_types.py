import sys

sys.path.append('../')
from facebot import types


def test_message():
    u = types.Message(text="hello", metadata="test")
    assert u.text == "hello"
    assert u.metadata == "test"


def test_quickreplie():
    q1 = types.QuickReplie(
        title="title", image_url="http://example.com/image.png")
    q2 = types.QuickReplie(content_type="location", title="title",
                          image_url="http://example.com/image.png")
    assert q1.title == "title"
    assert q1.image_url == "http://example.com/image.png"
    assert hasattr(q2, "title") == False
    assert q2.image_url == "http://example.com/image.png"


def test_quickreplies():
    q1 = types.QuickReplie(
        title="title", image_url="http://example.com/image.png")
    q2 = types.QuickReplie(content_type="location", title="title",
                          image_url="http://example.com/image.png")
    qs = types.QuickReplies()
    qs.add(q1)
    qs.add(q2)
    assert qs.quick_replies[0].title == "title"
    assert hasattr(qs.quick_replies[1], "title") == False
