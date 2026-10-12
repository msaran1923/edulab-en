#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
molecules.py — /(VSEPR).

:
  - ( unicode / LaTeX /  / )
  - : slot()、el()、pos()
  - :slot  + (1/2/3, 'ionic' )

( ≈ 1.0–1.4 , ELEMENTS).
/ reaction_kernel “”,.

:; RDKit,reaction_kernel  RDKit  SMILES
().
"""

import math

# ---------------------------------------------------------------------------
# :(, CPK )+  + 
# ---------------------------------------------------------------------------
ELEMENTS = {
    "C":  {"color": "#334155", "radius": 0.50, "zh": "",  "en": "Carbon"},
    "O":  {"color": "#ef4444", "radius": 0.42, "zh": "",  "en": "Oxygen"},
    "H":  {"color": "#f1f5f9", "radius": 0.25, "zh": "",  "en": "Hydrogen"},
    "N":  {"color": "#3b82f6", "radius": 0.46, "zh": "",  "en": "Nitrogen"},
    "Cl": {"color": "#22c55e", "radius": 0.52, "zh": "",  "en": "Chlorine"},
    "Na": {"color": "#a855f7", "radius": 0.58, "zh": "",  "en": "Sodium"},
    "S":  {"color": "#eab308", "radius": 0.52, "zh": "", "en": "Sulfur"},
    "Fe": {"color": "#f97316", "radius": 0.58, "zh": "",  "en": "Iron"},
    "Cu": {"color": "#fb923c", "radius": 0.56, "zh": "",  "en": "Copper"},
    "Mg": {"color": "#d1d5db", "radius": 0.56, "zh": "",  "en": "Magnesium"},
}

# (/;)
DEFAULT_CHARGE = {}


def element_color(el):
    return ELEMENTS.get(el, {"color": "#94a3b8"})["color"]


def element_radius(el):
    return ELEMENTS.get(el, {"radius": 0.45})["radius"]


# ---------------------------------------------------------------------------
# 
# ---------------------------------------------------------------------------
_INV_SQRT3 = 1.0 / math.sqrt(3.0)


def _r(v, n=4):
    return [round(float(x), n) for x in v]


def _atom(slot, el, pos):
    return {"slot": slot, "el": el, "pos": _r(pos)}


def _tetra_dirs():
    """ 4 ()."""
    base = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    return [tuple(c * _INV_SQRT3 for c in d) for d in base]


def _diatomic(slot_a, el_a, slot_b, el_b, d, order):
    half = d / 2.0
    return {
        "atoms": [_atom(slot_a, el_a, (-half, 0, 0)), _atom(slot_b, el_b, (half, 0, 0))],
        "bonds": [{"a": slot_a, "b": slot_b, "order": order}],
    }


def _linear_triatomic(center_el, out_el, d, order):
    """X=Y=X ( CO2)., ±x."""
    return {
        "atoms": [
            _atom("Y", center_el, (0, 0, 0)),
            _atom("Xa", out_el, (-d, 0, 0)),
            _atom("Xb", out_el, (d, 0, 0)),
        ],
        "bonds": [
            {"a": "Y", "b": "Xa", "order": order},
            {"a": "Y", "b": "Xb", "order": order},
        ],
    }


def _bent(center_el, out_el, d, angle_deg, order=1):
    """ AX2E( H2O).,、 +y."""
    half = math.radians(angle_deg) / 2.0
    sx, cy = d * math.sin(half), d * math.cos(half)
    return {
        "atoms": [
            _atom("A", center_el, (0, 0, 0)),
            _atom("Ha", out_el, (sx, cy, 0)),
            _atom("Hb", out_el, (-sx, cy, 0)),
        ],
        "bonds": [
            {"a": "A", "b": "Ha", "order": order},
            {"a": "A", "b": "Hb", "order": order},
        ],
    }


def _tetrahedral(center_el, out_el, d):
    """ AX4( CH4).,4 ."""
    atoms = [_atom("C", center_el, (0, 0, 0))]
    bonds = []
    for i, dr in enumerate(_tetra_dirs(), start=1):
        slot = f"H{i}"
        atoms.append(_atom(slot, out_el, tuple(c * d for c in dr)))
        bonds.append({"a": "C", "b": slot, "order": 1})
    return {"atoms": atoms, "bonds": bonds}


def _pyramidal(center_el, out_el, d, h=0.38):
    """ AX3E( NH3). h,."""
    atoms = [_atom("A", center_el, (0, h, 0))]
    bonds = []
    rad = d * math.cos(math.radians(20))
    for i in range(3):
        ang = math.radians(90 + i * 120)
        atoms.append(_atom(f"H{i + 1}", out_el,
                           (rad * math.cos(ang), h - d * math.sin(math.radians(20)) - 0.3,
                            rad * math.sin(ang))))
        bonds.append({"a": "A", "b": f"H{i + 1}", "order": 1})
    return {"atoms": atoms, "bonds": bonds}


def _mono(el):
    """(/, Na、C()、Fe)."""
    return {"atoms": [_atom("X", el, (0, 0, 0))], "bonds": []}


def _ion_pair(slot_a, el_a, slot_b, el_b, d):
    """( NaCl ):."""
    half = d / 2.0
    return {
        "atoms": [_atom(slot_a, el_a, (-half, 0, 0)), _atom(slot_b, el_b, (half, 0, 0))],
        "bonds": [{"a": slot_a, "b": slot_b, "order": "ionic"}],
    }


def _glucose_openchain():
    """D-(Fischer  3D):6 , Y .
    slots: C1-C6, O1-O6, H1-H5, H6a, H6b, HO2-HO6( 24 )."""
    a, b = [], []
    yc = [3.75, 2.25, 0.75, -0.75, -2.25, -3.75]   # C1..C6  y 
    # C1:  (CHO)
    a += [_atom("C1", "C", (0,    yc[0], 0)),
          _atom("O1", "O", (0,    yc[0] + 1.0, 0)),   # C=O 
          _atom("H1", "H", (-1.1, yc[0], 0))]          #  H
    b += [{"a": "C1", "b": "O1", "order": 2}, {"a": "C1", "b": "H1", "order": 1}]
    # C2 (OH )
    a += [_atom("C2",  "C", (0,    yc[1], 0)), _atom("O2",  "O", (1.4,  yc[1], 0)),
          _atom("HO2", "H", (2.1,  yc[1], 0)), _atom("H2",  "H", (-1.1, yc[1], 0))]
    b += [{"a": "C1", "b": "C2",  "order": 1}, {"a": "C2", "b": "O2",  "order": 1},
          {"a": "O2", "b": "HO2", "order": 1}, {"a": "C2", "b": "H2",  "order": 1}]
    # C3 (OH )
    a += [_atom("C3",  "C", (0,    yc[2], 0)), _atom("O3",  "O", (-1.4, yc[2], 0)),
          _atom("HO3", "H", (-2.1, yc[2], 0)), _atom("H3",  "H", (1.1,  yc[2], 0))]
    b += [{"a": "C2", "b": "C3",  "order": 1}, {"a": "C3", "b": "O3",  "order": 1},
          {"a": "O3", "b": "HO3", "order": 1}, {"a": "C3", "b": "H3",  "order": 1}]
    # C4 (OH )
    a += [_atom("C4",  "C", (0,    yc[3], 0)), _atom("O4",  "O", (1.4,  yc[3], 0)),
          _atom("HO4", "H", (2.1,  yc[3], 0)), _atom("H4",  "H", (-1.1, yc[3], 0))]
    b += [{"a": "C3", "b": "C4",  "order": 1}, {"a": "C4", "b": "O4",  "order": 1},
          {"a": "O4", "b": "HO4", "order": 1}, {"a": "C4", "b": "H4",  "order": 1}]
    # C5 (OH )
    a += [_atom("C5",  "C", (0,    yc[4], 0)), _atom("O5",  "O", (-1.4, yc[4], 0)),
          _atom("HO5", "H", (-2.1, yc[4], 0)), _atom("H5",  "H", (1.1,  yc[4], 0))]
    b += [{"a": "C4", "b": "C5",  "order": 1}, {"a": "C5", "b": "O5",  "order": 1},
          {"a": "O5", "b": "HO5", "order": 1}, {"a": "C5", "b": "H5",  "order": 1}]
    # C6:  (CH₂OH)
    a += [_atom("C6",  "C", (0,    yc[5],        0)),
          _atom("H6a", "H", (-0.8, yc[5] - 0.7,  0.5)),
          _atom("H6b", "H", (-0.8, yc[5] - 0.7, -0.5)),
          _atom("O6",  "O", (1.0,  yc[5] - 0.7,  0)),
          _atom("HO6", "H", (1.7,  yc[5] - 0.7,  0))]
    b += [{"a": "C5", "b": "C6",  "order": 1}, {"a": "C6", "b": "H6a", "order": 1},
          {"a": "C6", "b": "H6b", "order": 1}, {"a": "C6", "b": "O6",  "order": 1},
          {"a": "O6", "b": "HO6", "order": 1}]
    return {"atoms": a, "bonds": b}


# ---------------------------------------------------------------------------
# :id -> ( + )
#  unicode  + LaTeX;name 、name_en .
# ---------------------------------------------------------------------------
def _spec(species_id, geom, formula, latex, zh, en, color):
    return {
        "id": species_id,
        "formula": formula,
        "latex": latex,
        "name": zh,
        "name_en": en,
        "color": color,
        "atoms": geom["atoms"],
        "bonds": geom["bonds"],
    }


_LIBRARY_BUILDERS = {
    # —  /  —
    "H2":  lambda: _spec("H2",  _diatomic("Ha", "H", "Hb", "H", 0.90, 1),
                         "H₂", r"\text{H}_2", "", "hydrogen", "sky"),
    "O2":  lambda: _spec("O2",  _diatomic("Oa", "O", "Ob", "O", 1.10, 2),
                         "O₂", r"\text{O}_2", "", "oxygen", "red"),
    "N2":  lambda: _spec("N2",  _diatomic("Na", "N", "Nb", "N", 1.05, 3),
                         "N₂", r"\text{N}_2", "", "nitrogen", "blue"),
    "Cl2": lambda: _spec("Cl2", _diatomic("Cla", "Cl", "Clb", "Cl", 1.45, 1),
                         "Cl₂", r"\text{Cl}_2", "", "chlorine", "green"),
    "CO":  lambda: _spec("CO",  _diatomic("C", "C", "O", "O", 1.13, 3),
                         "CO", r"\text{CO}", "", "carbon monoxide", "slate"),
    # —  /  —
    "CO2": lambda: _spec("CO2", _linear_triatomic("C", "O", 1.16, 2),
                         "CO₂", r"\text{CO}_2", "", "carbon dioxide", "slate"),
    "H2O": lambda: _spec("H2O", _bent("O", "H", 0.96, 104.5),
                         "H₂O", r"\text{H}_2\text{O}", "", "water", "cyan"),
    "CH4": lambda: _spec("CH4", _tetrahedral("C", "H", 1.10),
                         "CH₄", r"\text{CH}_4", "", "methane", "slate"),
    "NH3": lambda: _spec("NH3", _pyramidal("N", "H", 1.0),
                         "NH₃", r"\text{NH}_3", "", "ammonia", "blue"),
    # —  /  /  —
    "Na":  lambda: _spec("Na", _mono("Na"), "Na", r"\text{Na}", "", "sodium", "violet"),
    "C":   lambda: _spec("C",  _mono("C"),  "C",  r"\text{C}",  "", "carbon", "slate"),
    "Fe":  lambda: _spec("Fe", _mono("Fe"), "Fe", r"\text{Fe}", "", "iron", "orange"),
    "Mg":  lambda: _spec("Mg", _mono("Mg"), "Mg", r"\text{Mg}", "", "magnesium", "slate"),
    "NaCl": lambda: _spec("NaCl", _ion_pair("Na", "Na", "Cl", "Cl", 1.50),
                          "NaCl", r"\text{NaCl}", "", "sodium chloride", "violet"),
    "Glucose": lambda: _spec("Glucose", _glucose_openchain(),
                             "C₆H₁₂O₆", r"\text{C}_6\text{H}_{12}\text{O}_6",
                             "", "glucose", "amber"),
}


def known_species():
    return sorted(_LIBRARY_BUILDERS.keys())


def has_species(species_id):
    return species_id in _LIBRARY_BUILDERS


def get(species_id):
    """ + (,)."""
    if species_id not in _LIBRARY_BUILDERS:
        raise KeyError(f" {species_id};: {', '.join(known_species())}")
    spec = _LIBRARY_BUILDERS[species_id]()
    # /,
    spec["atoms"] = [dict(a, pos=list(a["pos"])) for a in spec["atoms"]]
    spec["bonds"] = [dict(b) for b in spec["bonds"]]
    return spec


def atom_counts(species_id):
    """, / ."""
    counts = {}
    for a in _LIBRARY_BUILDERS[species_id]()["atoms"]:
        counts[a["el"]] = counts.get(a["el"], 0) + 1
    return counts


if __name__ == "__main__":
    # :
    for sid in known_species():
        m = get(sid)
        print(f"{sid:6s} {m['formula']:6s} atoms={len(m['atoms'])} "
              f"bonds={len(m['bonds'])} counts={atom_counts(sid)}")
