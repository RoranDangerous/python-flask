from werkzeug.routing import BaseConverter

class RegexConverter(BaseConverter):
    """
    Regex Converter. Used to match params in the url.
    """
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]