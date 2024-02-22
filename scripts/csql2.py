"""
csql version to support corpling research of "Brüsszel".
"""

import argparse
import sys


def matches(wt, ft):
    """Whether `wt` and `ft` are the same token alone and with attribs."""
    return ft.startswith(f'{wt}/') or wt == ft
    # 1st cond: `nyolc` vs `nyolc/nyolc/NUM/Case=Nom`
    #      and  `Brüsszel/percben` vs `Brüsszel/percben/Brüsszel/perc/NOUN/Ca...`
    # 2nd cond: the case of '</cond>'


def main():
    """Main."""
    args = get_args()

    FILE = args.file

    # XXX SHOULD BE: (1) equal length; (2) without header
    word_file = f'{FILE}_word.txt' # just the 'word' attrib (for easier alignment)
    full_file = f'{FILE}_full.txt' # the same with all attribs needed

    # azért kell szórakozni, mert
    #  (1) az értékben lehet '/', és ezt sehogy sem kezeli a formátum!!!
    #  (2) az értékben lehet szóköz, és ezt sehogy sem kezeli a formátum!!!
    # ejnye!

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
                    #print('++'.join(ftok_joined))
                    print(ftok_joined)
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
            #print('++'.join(ftok_joined))
            print(ftok_joined)


def get_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    # string-valued argument
    parser.add_argument(
        '-f', '--file',
        help='filename',
        required=True,
        type=str,
        default=argparse.SUPPRESS
    )
    return parser.parse_args()


if __name__ == '__main__':
    main()
