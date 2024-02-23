"""
csql version to support corpling research of "Brüsszel".
"""

import argparse
import pprint
import sys


# are these configurable using crystal???
NOSKE_SEP = '/'
NOSKE_KWIC_BEG = '<coll>'
NOSKE_KWIC_END = '</coll>'

# globals set by main() based on command line params
CAN_CONTAIN_NOSKE_SEP = None
NO_OF_FIELDS = None


# azért kell szórakozni, mert
#  (1) az értékben lehet NOSKE_SEP, és ezt sehogy sem kezeli a formátum!!!
#  (2) az értékben lehet szóköz, és ezt sehogy sem kezeli a formátum!!!
# és ezt a NoSkE XML download funkciója sem kezeli!
# ejnye!


class Hit:
    """Represent a concordance hit: header, left context, kwic, right context."""
    def __init__(self):
        self.header = ''
        self.left = []
        self.kwic = []
        self.right = []

    @staticmethod
    def format_list(lst):
        MAX_LINE_LENGTH = 100000 # hope that its enough
        return pprint.pformat(lst, width=MAX_LINE_LENGTH, compact=True)

    def __str__(self):
        s = ''
        s += self.header
        for member in [self.left, self.kwic, self.right]:
            s += '\t'
            s += ' '.join(self.format_list(tok) for tok in member)
        return s


# XXX rusnya -- 100%, hogy szépíthető, egyszerűsíthető
def handle_noske_seps_split2fields(word):
    """Split word-string to fields, handling (non-extremal) NOSKE_SEPs smartly."""
    if word in (NOSKE_KWIC_BEG, NOSKE_KWIC_END): # XXX hogy kezeljük a KWIC-t?
        ret = word
    else:
        fields = word.split(NOSKE_SEP)

        additional = len(fields) - NO_OF_FIELDS
        how_many_can_contain = len(CAN_CONTAIN_NOSKE_SEP)
        add_per_field = int(additional / how_many_can_contain)

        r = range(1, 4) # XXX any number of '/'s should be allowed not just 3
        possible_additional = list(
            map(lambda x: x * how_many_can_contain, r))

        if additional == 0:
            ret = fields
        elif additional in possible_additional:
            out = []
            fields_iter = iter(fields)
            for idx in range(NO_OF_FIELDS):
                if idx in CAN_CONTAIN_NOSKE_SEP:
                    x = []
                    for j in range(add_per_field + 1):
                        x.append(next(fields_iter))
                    out.append(NOSKE_SEP.join(x))
                else:
                    out.append(next(fields_iter))
            ret = out
        else:
            ret = f'ERROR:[{fields}]'
    return ret


def matches(wt, ft):
    """Whether `wt` and `ft` are the same token alone and with attribs."""
    return ft.startswith(f'{wt}/') or wt == ft
    # 1st cond: `nyolc` vs `nyolc/nyolc/NUM/Case=Nom`
    #      and  `Brüsszel/percben` vs `Brüsszel/percben/Brüsszel/perc/NOUN/Ca...`
    # 2nd cond: the case of '</cond>'


# XXX rusnya -- 100%, hogy szépíthető, egyszerűsíthető
def handle_spaces_process_parallel(word_file, full_file):
    """
    Process `word_file` (containing just the 'word' attrib for easier alignment)
    and `full_file` (the same with all attribs needed) in parallel.
    The two files should be: (1) equal length; (2) without header.
    """
    for wline, fline in zip(word_file, full_file):

        # fix
        wline = wline.replace(f'{NOSKE_KWIC_BEG}', f' {NOSKE_KWIC_BEG} ')
        wline = wline.replace(f'{NOSKE_KWIC_END}', f' {NOSKE_KWIC_END} ')
        fline = fline.replace(f'{NOSKE_KWIC_BEG}', f' {NOSKE_KWIC_BEG} ')
        fline = fline.replace(f'{NOSKE_KWIC_END}', f' {NOSKE_KWIC_END} ')

        wtoks = iter(wline.rstrip('\n').split())
        ftoks = iter(fline.rstrip('\n').split())

        hit = Hit()

        # 1st token: header
        hit.header = next(wtoks)
        next(ftoks) # XXX ua kell lennie, ellenőrzés nincs

        # 2ns token: '|'
        next(wtoks), next(ftoks)

        tokens = []

        # XXX ebből lehetne egy collect() nevű more_itertools-t csinálni
        # XXX tuti, hogy lehet vhogy egyszerűsíteni -- de hogy?
        wt, ft = next(wtoks), next(ftoks)
        # gyüjtést kezd + továbblép mindkettőben
        ftok_joined = [ft]
        try: ft = next(ftoks)
        except StopIteration: break
        try: wt = next(wtoks)
        except StopIteration: pass
        while wtoks and ftoks:
            if matches(wt, ft):
                # store összegyűjtött
                tokens.append(handle_noske_seps_split2fields('++'.join(ftok_joined)))
                # gyüjtést kezd + továbblép mindkettőben
                ftok_joined = [ft]
                try: ft = next(ftoks)
                except StopIteration: break
                try: wt = next(wtoks)
                except StopIteration: pass
            else:
                # gyűjt
                ftok_joined.append(ft)
                # továbblép a gyűjtősben
                try: ft = next(ftoks)
                except StopIteration: break
        # store összegyűjtött
        tokens.append(handle_noske_seps_split2fields('++'.join(ftok_joined)))

        status = 'left'
        for token in tokens:
            if token == NOSKE_KWIC_BEG:
                status = 'kwic'
            elif token == NOSKE_KWIC_END:
                status = 'right'
            else:
                getattr(hit, status).append(token)

        yield hit


def main():
    """Main."""
    args = get_args()

    global CAN_CONTAIN_NOSKE_SEP
    CAN_CONTAIN_NOSKE_SEP = list(map(int, args.can_contain_noske_sep.split(',')))
    # XXX feltesszük, hogy ezek mindig ugyanannyi plusz NOSKE_SEP-et tartalmaznak...

    global NO_OF_FIELDS
    NO_OF_FIELDS = args.number_of_fields

    FILE = args.file

    # XXX SHOULD BE: (1) equal length; (2) without header
    word_file = f'{FILE}_word.txt' # just the 'word' attrib (for easier alignment)
    full_file = f'{FILE}_full.txt' # the same with all attribs needed

    with open(word_file, "r") as wfile, open(full_file, "r") as ffile:
        hits = handle_spaces_process_parallel(wfile, ffile)
        for hit in hits:
            print(hit)


def get_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '-f', '--file',
        help='filename',
        required=True,
        type=str,
        default=argparse.SUPPRESS
    )
    parser.add_argument(
        '-n', '--number-of-fields',
        help="number of fields",
        required=True,
        type=int,
        default=argparse.SUPPRESS
    )
    parser.add_argument(
        '-s', '--can-contain-noske-sep',
        help=f"field numbers counted from 0 that can contain '{NOSKE_SEP}' separated by comma",
        required=True,
        type=str,
        default=argparse.SUPPRESS
    )
    return parser.parse_args()


if __name__ == '__main__':
    main()
