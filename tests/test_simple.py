from reddit_topics_aggregator.simple import reverse


def test_reverse():
    assert reverse("foo") == "oof"
