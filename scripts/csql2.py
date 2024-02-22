"""
csql version to support corpling research of "Brüsszel".
"""

import argparse
import sys


NOSKE_SEP = '/' # is this configurable using crystal???


# azért kell szórakozni, mert
#  (1) az értékben lehet NOSKE_SEP, és ezt sehogy sem kezeli a formátum!!!
#  (2) az értékben lehet szóköz, és ezt sehogy sem kezeli a formátum!!!
# ejnye!


def matches(wt, ft):
    """Whether `wt` and `ft` are the same token alone and with attribs."""
    return ft.startswith(f'{wt}/') or wt == ft
    # 1st cond: `nyolc` vs `nyolc/nyolc/NUM/Case=Nom`
    #      and  `Brüsszel/percben` vs `Brüsszel/percben/Brüsszel/perc/NOUN/Ca...`
    # 2nd cond: the case of '</cond>'


# XXX rusnya lett -- 100%, hogy egyszerűsíthető
def split2fields(s, no_of_fields, can_contain_noske_sep):
    """Split string to fields, handling NOSKE_SEPs smartly."""
    if s == '<coll>' or s == '</coll>': # XXX hogy kezeljük a KWIC-t?
        ret = s
    else:
        fields = s.split(NOSKE_SEP)

        additional = len(fields) - no_of_fields
        how_many_can_contain = len(can_contain_noske_sep)
        add_per_field = int(additional / how_many_can_contain)

        r = range(1, 4) # XXX any number of '/'s should be allowed not just 3
        possible_additional = list(
            map(lambda x: x * how_many_can_contain, r))

        if additional == 0:
            ret = fields
        elif additional in possible_additional:
            out = []
            fields_iter = iter(fields)
            for idx in range(no_of_fields):
                if idx in can_contain_noske_sep:
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


def main():
    """Main."""
    args = get_args()

    FILE = args.file

    CAN_CONTAIN_NOSKE_SEP = list(map(int, args.can_contain_noske_sep.split(',')))
    # XXX feltesszük, hogy ezek mindig ugyanannyi plusz NOSKE_SEP-et tartalmaznak...

    NO_OF_FIELDS = args.number_of_fields

    # XXX SHOULD BE: (1) equal length; (2) without header
    word_file = f'{FILE}_word.txt' # just the 'word' attrib (for easier alignment)
    full_file = f'{FILE}_full.txt' # the same with all attribs needed

    with open(word_file, "r") as wfile, open(full_file, "r") as ffile:
        for wline, fline in zip(wfile, ffile):

            # fix
            wline = wline.replace('<coll>', ' <coll> ')
            wline = wline.replace('</coll>', ' </coll> ')
            fline = fline.replace('<coll>', ' <coll> ')
            fline = fline.replace('</coll>', ' </coll> ')

            wtoks = iter(wline.rstrip('\n').split())
            ftoks = iter(fline.rstrip('\n').split())

            # 1st token: header
            header = next(wtoks)
            next(ftoks) # XXX ua kell lennie, ellenőrzés nincs
            print(f'header=[{header}]')

            # 2ns token: '|'
            next(wtoks), next(ftoks)

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
                    # print összegyűjtött
                    print(split2fields('++'.join(ftok_joined), NO_OF_FIELDS, CAN_CONTAIN_NOSKE_SEP))
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
            # print összegyűjtött
            print(split2fields('++'.join(ftok_joined), NO_OF_FIELDS, CAN_CONTAIN_NOSKE_SEP))


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
