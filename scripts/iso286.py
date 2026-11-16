"""ISO 286-1:2010 verified subset: Tables 1–5, Figures 12–13, Annex B.

All signed differences use hole minus shaft; interferences are negative.
Unsupported values fail closed. This module does not infer application suitability.
"""
import json
import re
from decimal import Decimal, InvalidOperation
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[1] / 'references/iso-286-1-2010.json'

def load():
    return json.loads(DATA_PATH.read_text(encoding='utf-8'))

def number(value):
    if isinstance(value, bool):
        raise ValueError('Boolean is not a dimension')
    try:
        n = Decimal(str(value).strip().replace(',', '.'))
    except InvalidOperation as exc:
        raise ValueError('Invalid dimension') from exc
    if not n.is_finite():
        raise ValueError('Dimension must be finite')
    return n

def index(ends, size):
    return next(i for i, hi in enumerate(ends) if size <= hi)

def deviations(code, size, hole, data=None):
    d = data or load()
    size = number(size)
    if not 0 < size <= 500:
        raise ValueError('Verified subset: 0 < nominal size ≤ 500 mm')
    m = re.fullmatch(r'([A-Za-z]+)([0-9]+)', code)
    if not m or (m[1].isupper() != hole):
        raise ValueError('Use uppercase hole and lowercase shaft classes')
    letter, grade = m[1].lower(), int(m[2])
    if m[1] not in d['scope']['letters'] or str(grade) not in d['it_um']:
        raise ValueError('Class outside the verified implementation subset')
    i = index(d['size_upper_mm'], size)
    it = Decimal(d['it_um'][str(grade)][i])
    if letter == 'js':
        return -it/2, it/2
    if letter == 'h':
        return (Decimal(0), it) if hole else (-it, Decimal(0))
    if letter in ['e','f','g']:
        es = Decimal(d['fundamental_um'][letter][i])
        return (-es, -es+it) if hole else (es-it, es)
    base = Decimal(d['rs_um'][letter][index(d['rs_upper_mm'],size)] if letter in ['r','s'] else d['fundamental_um'][letter][i])
    if not hole:
        if letter == 'k' and grade not in [5,6,7]:
            base = Decimal(0)
        return base, base+it
    # Table 3 delta equals ITn - IT(n-1); no delta in the first size interval.
    corrected = (letter in ['k','m','n'] and grade <= 8) or (letter in ['p','r','s'] and grade <= 7)
    delta = Decimal(0)
    if corrected and size > 3:
        if grade == 5:
            raise ValueError('Hole delta for IT5 is outside the verified subset')
        delta = it - Decimal(d['it_um'][str(grade-1)][i])
    if letter == 'k' and grade > 8:
        es = Decimal(0)
    elif letter == 'n' and grade > 8 and size > 3:
        es = Decimal(0)
    else:
        es = -base + delta
    if letter == 'm' and grade == 6 and 250 < size <= 315:
        es = Decimal(-9)  # Table 2 footnote b.
    return es-it, es

def calculate(designation, size, data=None):
    d = data or load()
    parts = designation.replace(' ','').split('/')
    if len(parts) != 2:
        raise ValueError('Expected hole/shaft, e.g. H7/g6')
    nominal = number(size)
    loh, hih = deviations(parts[0], nominal, True, d)
    los, his = deviations(parts[1], nominal, False, d)
    minimum, maximum = loh-his, hih-los
    kind = 'clearance' if minimum >= 0 else ('interference' if maximum <= 0 else 'transition')
    return {'standard':d['standard'],'designation':'/'.join(parts),'nominal_mm':float(nominal),
            'type':kind,'hole_deviations_um':[float(loh),float(hih)],'shaft_deviations_um':[float(los),float(his)],
            'hole_limits_mm':[float(nominal+loh/1000),float(nominal+hih/1000)],
            'shaft_limits_mm':[float(nominal+los/1000),float(nominal+his/1000)],
            'signed_difference_um':[float(minimum),float(maximum)],
            'signed_difference_mm':[float(minimum/1000),float(maximum/1000)],
            'formula':['C_min = hole_min - shaft_max','C_max = hole_max - shaft_min'],
            'source':'ISO 286-1:2010 Tables 1–5; Annex B.2',
            'scope':'Size intervals only; form, coating, temperature and assembly forces not evaluated.'}

def recommend(basis, kind, size, minimum=None, maximum=None, data=None):
    d = data or load()
    if basis not in d['candidates'] or kind not in ['clearance','transition','interference']:
        raise ValueError('Invalid basis or fit type')
    # Validate even when no candidates remain.
    deviations('H7',size,True,d)
    low = number(minimum)*1000 if minimum is not None else None
    high = number(maximum)*1000 if maximum is not None else None
    if low is not None and high is not None and low > high:
        raise ValueError('Minimum must not exceed maximum')
    out = []
    for candidate in d['candidates'][basis]:
        r = calculate(candidate['code'],size,d)
        c0,c1 = map(number,r['signed_difference_um'])
        if r['type'] == kind and (low is None or c0 >= low) and (high is None or c1 <= high):
            out.append({**r,'first_choice':candidate['first_choice']})
    return {'standard':d['standard'],'basis':basis,'type':kind,
            'requirement_mm':[float(low/1000) if low is not None else None,float(high/1000) if high is not None else None],
            'status':'CANDIDATES' if out else 'NO_MATCH_IN_VERIFIED_SUBSET',
            'candidates':out,'source':'5.3.4 Figures 12–13; functional filtering per 5.3.5 and Annex B.4',
            'note':'First choice means framed combination, not DIN series. No application suitability is inferred.'}
