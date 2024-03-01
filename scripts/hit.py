"""
Class Hit for representing a concordance line.
"""

import pprint

# are these configurable using crystal???
NOSKE_HEADER_SEP = ','

class Hit:
    """Represent a concordance hit: header, left context, kwic, right context."""
    def __init__(self):
        self.header = []
        self.left = []
        self.kwic = []
        self.right = []

    FIELD_SEP = '\t'
    FORMAT_LIST_SEP = ' '

    def set_header(self, header_string):
        """Stores header fields as a list."""
        self.header = header_string.split(NOSKE_HEADER_SEP)

    @staticmethod
    def format_token(tok): # token = list of features!
        """Format features of a token as printed python list."""
        MAX_LINE_LENGTH = 100000 # hope that its enough
        return pprint.pformat(tok, width=MAX_LINE_LENGTH, compact=True)

    @staticmethod
    def format_text(text): # text = list of tokens!
        """Format tokens of a text by joining them."""
        return Hit.FORMAT_LIST_SEP.join(Hit.format_token(tok) for tok in text)

    # XXX vhogy ez így tűnik jónak, h "kívülről" kezeli, nem `self`-ként, hm..
    # XXX talán, hogy az osztályon kívül is definiálhassunk ilyen fgveket, hm..
    @staticmethod
    def orig_fields(hit):
        """
        Default processing function for `get_data_record()`.
        Give original NoSkE format but cut into fields.
        """
        return hit.header + [hit.format_text(member) for member in [hit.left, hit.kwic, hit.right]]

    def get_data_record(self, func=None):
        """Return a .tsv data record applying `func` to `self`."""
        if func is None: func = Hit.orig_fields
        fields = func(self)
        return Hit.FIELD_SEP.join(fields)

    def __str__(self):
        return self.get_data_record(Hit.orig_fields);
    # the next three are the same now:
    #print(hit)
    #print(hit.get_data_record())
    #print(hit.get_data_record(Hit.orig_fields))

