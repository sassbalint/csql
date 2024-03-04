"""
Processing funcs for csql.
"""

import sys

from hit import Hit

# -----

FORM = 0
LEMMA = 1
POS = 2
FEAT = 3

ID = 4
DEPLABEL = 5

HEADLEMMA = 6
HEADPOS = 7
HEADFEAT = 8
HEADID = 9

# 1. original ~ NoSkE basic but cut into fields
orig = Hit.orig_fields

# 2. header + csak a KWIC szóalak
def header_kwic(hit):
    return hit.header + [hit.kwic[0][FORM]]

# 3. KWIC szóalak lemma + 1 bal-kontext lemma + 1 jobb-kontext lemma
# XXX IndexError-t ad, közben meg megcsinálja végig a fájl -- vajon miért?
def one_context(hit):
    return [hit.left[-1][LEMMA], hit.kwic[0][LEMMA], hit.right[0][LEMMA]]

# 4. jobbsó legközelebbi ige
def nearest_verb(hit):
    fields = [hit.kwic[0][FORM]]
    verb_lemma = 'None'
    verb_index = 'None'
    for i, token in enumerate(hit.right):
        if token[POS] == 'VERB':
            verb_lemma = token[LEMMA]
            verb_index = i
            break
    fields += [verb_lemma, str(verb_index)]
    return fields

# 5. vmi hossz...
def length(hit):
    kwic = hit.kwic[0][FORM]
    left = 'None'
    try:
        left = hit.left[-1][FORM]
    except IndexError:
        pass
    return hit.header + [left, kwic, str(len(kwic))]

# 6. for researching "Brüsszel" in ParlaMint 4.0
def brusszel(hit):
    return (
        hit.header
        + [' '.join(t[FORM] for t in hit.left)]
        + [hit.left[-2][FORM]]
        + [hit.left[-1][FORM]]
        + [hit.kwic[0][FORM]]
        + [hit.right[0][FORM]]
        + [hit.right[1][FORM]]
        + [' '.join(t[FORM] for t in hit.right)]
    )

# 7. fej <- dep
def dep(hit):
    return (
        hit.header
        + [' '.join(t[FORM] for t in hit.left)]
        + [hit.kwic[0][FORM]]
        + [hit.kwic[0][HEADLEMMA]]
        + [hit.kwic[0][HEADPOS]]
        + [hit.kwic[0][DEPLABEL]]
        + [' '.join(t[FORM] for t in hit.right)]
    )


# 8. fej <- dep -- head szóalak kikeresgélve a head dolgai közül
def dep2(hit):
    kwic = hit.kwic[0] # egyszavas kwic-t feltételezve
    headid = kwic[HEADID]
    headform = '?'
    for tok in hit.left + hit.right:
        try: # XXX csql.py ERROR-os sorok miatt...
            if tok[ID] == headid:
                headform = tok[FORM]
                break
        except IndexError:
            pass
    return (
        hit.header
        + [' '.join(t[FORM] for t in hit.left)]
        + [hit.kwic[0][FORM]]
        + [hit.kwic[0][HEADLEMMA]]
        + [hit.kwic[0][HEADPOS]]
        + [hit.kwic[0][DEPLABEL]]
        + [headform]
        + [' '.join(t[FORM] for t in hit.right)]
    )


# -----

# XXX jó lenne elkerülni, hogy itt újból fel kelljen sorolni!
funcs = {
    'orig': orig,
    'header_kwic': header_kwic,
    'one_context': one_context,
    'nearest_verb': nearest_verb,
    'length': length,
    'brusszel': brusszel,
    'dep': dep,
    'dep2': dep2,
}

