import actions

class TestActions:
    def test_uppercase(self):
        assert actions.uppercase("hello world") == "HELLO WORLD"

    def test_lowercase(self):
        assert actions.lowercase("HELLO WORLD") == "hello world"

    def test_reverse(self):
        assert actions.reverse("Hello world") == "dlrow olleH"

    def test_shuffle(self):
        pass

    def test_random(self):
        result = actions.random("Hello world") != "Hello world"
        assert result != None and result != "Hello world"
