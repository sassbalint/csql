"""
Processing funcs for csql.
"""

from hit import Hit

# -----

# 1. original ~ NoSkE basic but cut into fields
orig = Hit.orig_fields

# 2. header + csak a KWIC szóalak
def header_kwic(hit):
    return hit.header + [hit.kwic[0][0]]

# 3. KWIC szóalak lemma + 1 bal-kontext lemma + 1 jobb-kontext lemma
# XXX IndexError-t ad, közben meg megcsinálja végig a fájl -- vajon miért?
def one_context(hit):
    return [hit.left[-1][1], hit.kwic[0][1], hit.right[0][1]]

# 4. jobbsó legközelebbi ige
def nearest_verb(hit):
    fields = [hit.kwic[0][0]]
    verb_lemma = 'None'
    verb_index = 'None'
    for i, token in enumerate(hit.right):
        if token[2] == 'VERB':
            verb_lemma = token[1]
            verb_index = i
            break
    fields += [verb_lemma, str(verb_index)]
    return fields

# 5. vmi hossz...
def length(hit):
    kwic = hit.kwic[0][0]
    left = 'None'
    try:
        left = hit.left[-1][0]
    except IndexError:
        pass
    return hit.header + [left, kwic, str(len(kwic))]

# -----

# XXX jó lenne elkerülni, hogy itt újból fel kelljen sorolni!
funcs = {
    'orig': orig,
    'header_kwic': header_kwic,
    'one_context': one_context,
    'nearest_verb': nearest_verb,
    'length': length,
}

