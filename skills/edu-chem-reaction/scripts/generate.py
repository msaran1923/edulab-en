#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate.py —  spec  reaction_kernel  template/reaction.html，。

 lib/reaction_kernel.py （）：、、/、。
 build_* “ spec”，assemble_data 。

 sympy。 import sympy （：/opt/homebrew/bin/python3.11）：
    python3 scripts/generate.py <key> [.html]
    python3 scripts/generate.py list
    python3 scripts/generate.py all <>
"""

import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "template" / "reaction.html"
PLACEHOLDER = "__REACTION_DATA__"

sys.path.insert(0, str(SKILL_DIR / "lib"))
import reaction_kernel as K          # noqa: E402


def render_html(data: dict, out_path: Path) -> Path:
    template = TEMPLATE.read_text(encoding="utf-8")
    if PLACEHOLDER not in template:
        raise RuntimeError(f" {PLACEHOLDER}")
    out_path.write_text(template.replace(PLACEHOLDER, json.dumps(data, ensure_ascii=False)),
                        encoding="utf-8")
    return out_path


def _p(html):
    return f"<p>{html}</p>"


# =====================================================================
# =====================================================================
def build_combustion_ch4():
    return {
        "meta": {"title": "", "subtitle": "CH₄ + O₂ ",
                 "language": "en", "category": "junior", "accent": "amber", "engine": "morph"},
        "conditions": {"text": "", "exothermic": True, "flame": True},
        "reactants": [{"species": "CH4", "count": 1, "pos": [-4.0, 0.2, 0]},
                      {"species": "O2", "count": 2}],   #  O2 （O2#1  CO2，O2#2 ）
        "products": [{"species": "CO2", "count": 1, "pos": [-2.7, 1.1, 0]},
                     {"species": "H2O", "count": 2}],
        "atom_map": [
            ["CH4#1.C", "CO2#1.Y"],
            ["O2#1.Oa", "CO2#1.Xa"], ["O2#1.Ob", "CO2#1.Xb"],
            ["O2#2.Oa", "H2O#1.A"], ["O2#2.Ob", "H2O#2.A"],
            ["CH4#1.H1", "H2O#1.Ha"], ["CH4#1.H2", "H2O#1.Hb"],
            ["CH4#1.H3", "H2O#2.Ha"], ["CH4#1.H4", "H2O#2.Hb"],
        ],
        "energy": {"activation": 0.5, "deltaH": -0.75, "reactantLabel": "CH₄+O₂", "productLabel": "CO₂+H₂O"},
        "steps": [
            {"title": "",
             "html": "<span class='text-slate-200 font-semibold'> (CH₄)</span>  "
                     "<span class='text-red-400 font-semibold'> (O₂)</span> 。"
                     " C–H  O=O ，，<span class='text-amber-400 font-semibold'></span>。"},
            {"title": "",
             "html": "，<span class='border-b border-dashed border-amber-500'>C–H  O=O </span>，"
                     "。<span class='text-amber-400 font-semibold'></span>，"
                     "，。"},
            {"title": "",
             "html": " <span class='text-slate-200 font-semibold'> (CO₂)</span>  "
                     "<span class='text-blue-300 font-semibold'> (H₂O)</span>。"
                     "（1C、4H、4O），。"},
        ],
    }


# =====================================================================
# =====================================================================
def build_combustion_h2():
    return {
        "meta": {"title": "", "subtitle": "2H₂ + O₂ ",
                 "language": "en", "category": "junior", "accent": "sky", "engine": "morph"},
        "conditions": {"text": "", "exothermic": True, "flame": True},
        "reactants": [{"species": "H2", "count": 2}, {"species": "O2", "count": 1}],
        "products": [{"species": "H2O", "count": 2}],
        "atom_map": [
            ["O2#1.Oa", "H2O#1.A"], ["O2#1.Ob", "H2O#2.A"],
            ["H2#1.Ha", "H2O#1.Ha"], ["H2#1.Hb", "H2O#1.Hb"],
            ["H2#2.Ha", "H2O#2.Ha"], ["H2#2.Hb", "H2O#2.Hb"],
        ],
        "energy": {"activation": 0.45, "deltaH": -0.7, "reactantLabel": "H₂+O₂", "productLabel": "H₂O"},
        "steps": [
            {"title": "",
             "html": " <span class='text-sky-300 font-semibold'> (H₂)</span>  "
                     "<span class='text-red-400 font-semibold'> (O₂)</span> 。"},
            {"title": "",
             "html": " <span class='border-b border-dashed border-sky-400'>H–H  O=O </span>，"
                     "，（）。"},
            {"title": "",
             "html": "， <span class='text-blue-300 font-semibold'> (H₂O)</span>。"
                     "：4H、2O。"},
        ],
    }


# =====================================================================
# =====================================================================
def build_electrolysis_water():
    return {
        "meta": {"title": "", "subtitle": "",
                 "language": "en", "category": "junior", "accent": "cyan", "engine": "morph"},
        "conditions": {"text": "", "under": ""},
        "reactants": [{"species": "H2O", "count": 2}],
        "products": [{"species": "H2", "count": 2}, {"species": "O2", "count": 1}],
        "atom_map": [
            ["H2O#1.A", "O2#1.Oa"], ["H2O#2.A", "O2#1.Ob"],
            ["H2O#1.Ha", "H2#1.Ha"], ["H2O#1.Hb", "H2#1.Hb"],
            ["H2O#2.Ha", "H2#2.Ha"], ["H2O#2.Hb", "H2#2.Hb"],
        ],
        "energy": {"activation": 0.35, "deltaH": 0.55, "reactantLabel": "H₂O", "productLabel": "H₂+O₂"},
        "steps": [
            {"title": "",
             "html": " <span class='text-cyan-300 font-semibold'> (H₂O)</span> ，"
                     "O–H ，<span class='text-cyan-400 font-semibold'></span>。"},
            {"title": "",
             "html": "，<span class='border-b border-dashed border-cyan-400'>O–H </span>，"
                     "、。<span class='text-cyan-400 font-semibold'></span>。"},
            {"title": "",
             "html": " <span class='text-sky-300 font-semibold'> (H₂)</span>（），"
                     " <span class='text-red-400 font-semibold'> (O₂)</span>（）， 2:1。：4H、2O。"},
        ],
    }


# =====================================================================
# =====================================================================
def build_redox_na_cl2():
    return {
        "meta": {"title": "", "subtitle": "2Na + Cl₂ —— ",
                 "language": "en", "category": "inorganic", "accent": "violet", "engine": "morph"},
        "conditions": {"text": "", "exothermic": True, "transitionGlow": True},
        "reactants": [{"species": "Na", "count": 2}, {"species": "Cl2", "count": 1}],
        "products": [{"species": "NaCl", "count": 2}],
        "atom_map": [
            ["Na#1.X", "NaCl#1.Na"], ["Na#2.X", "NaCl#2.Na"],
            ["Cl2#1.Cla", "NaCl#1.Cl"], ["Cl2#1.Clb", "NaCl#2.Cl"],
        ],
        "electrons": [
            {"from": "Na1", "to": "Cl1", "count": 1, "label": "e⁻"},
            {"from": "Na2", "to": "Cl2", "count": 1, "label": "e⁻"},
        ],
        "energy": {"activation": 0.4, "deltaH": -0.8, "reactantLabel": "Na+Cl₂", "productLabel": "NaCl"},
        "steps": [
            {"title": "",
             "html": "<span class='text-violet-300 font-semibold'> (Na)</span>  1 ，"
                     "<span class='text-green-400 font-semibold'> (Cl₂)</span>  7 ， 8 。"},
            {"title": "",
             "html": " <span class='border-b border-dashed border-green-400'>Cl–Cl </span>，"
                     " 1  <span class='text-cyan-300 font-semibold'> (e⁻)</span> ："
                     "<span class='text-amber-400 font-semibold'></span> Na⁺，<span class='text-sky-400 font-semibold'></span> Cl⁻。"},
            {"title": "",
             "html": "Na⁺  Cl⁻ （） <span class='text-violet-300 font-semibold'> (NaCl)</span>。"
                     "：Na 0→+1、Cl 0→−1，，：2Na、2Cl。"},
        ],
    }


# =====================================================================
# =====================================================================
_EST_FRAGS = {
    "acetyl":    {"K0": {"pos": [-4.5, 0.5, 0], "rot": [0, 0, 0]},
                  "K1": {"pos": [-0.7, 0.1, 0], "rot": [0, 0, 0]},
                  "K2": {"pos": [-2.5, 1.2, 0], "rot": [0, 0, -0.1]}},
    "leavingOH": {"K0": {"pos": [-3.5, -0.1, 0.2], "rot": [0, 0, 0]},
                  "K1": {"pos": [0.5, -0.5, -0.3], "rot": [0, 0, -0.2]},
                  "K2": {"pos": [3.2, -1.5, -0.5], "rot": [0.2, 0.3, 0.5]}},
    "ethoxy":    {"K0": {"pos": [4.5, -0.5, 0], "rot": [0, 0, 0]},
                  "K1": {"pos": [0.6, 0.2, 0.15], "rot": [0, 0, 0]},
                  "K2": {"pos": [-1.38, 1.05, 0], "rot": [0, 0, 0]}},
    "leavingH":  {"K0": {"pos": [3.9, -1.1, 0], "rot": [0, 0, 0]},
                  "K1": {"pos": [1.1, -1.3, -0.3], "rot": [0, 0, 0]},
                  "K2": {"pos": [3.9, -2.0, -0.5], "rot": [0, 0, 0]}},
    "catalyst":  {"catalyst": True,
                  "K0": {"pos": [-4.5, 2.5, 0.5], "rot": [0, 0, 0]},
                  "K1": {"pos": [-0.5, -1.0, -0.3], "rot": [0, 0, 0]},
                  "K2": {"pos": [5.0, 1.0, 1.0], "rot": [0, 0, 0]}},
}
_EST_ATOMS = [
    ("C1", "C", "acetyl", [0, 0.2, 0]), ("O1", "O", "acetyl", [0, 1.25, 0]),
    ("C2", "C", "acetyl", [-1.2, -0.5, 0]), ("H1", "H", "acetyl", [-1.2, -1.2, 0.8]),
    ("H2", "H", "acetyl", [-1.2, -1.2, -0.8]), ("H3", "H", "acetyl", [-2.0, -0.1, 0]),
    ("O2", "O", "leavingOH", [0, 0, 0]), ("H4", "H", "leavingOH", [0.7, -0.5, 0.1]),
    ("O3", "O", "ethoxy", [0, 0, 0]), ("C3", "C", "ethoxy", [1.1, 0.4, 0]),
    ("H5", "H", "ethoxy", [1.1, 1.0, 0.8]), ("H6", "H", "ethoxy", [1.1, 1.0, -0.8]),
    ("C4", "C", "ethoxy", [2.3, -0.3, 0]), ("H7", "H", "ethoxy", [2.3, -0.9, 0.8]),
    ("H8", "H", "ethoxy", [2.3, -0.9, -0.8]), ("H9", "H", "ethoxy", [3.0, 0.3, 0]),
    ("H10", "H", "leavingH", [0, 0, 0]),
    ("Hp", "H", "catalyst", [0, 0, 0]),
]
_EST_BEFORE = [
    ("C1", "O1", 2), ("C1", "C2", 1), ("C2", "H1", 1), ("C2", "H2", 1), ("C2", "H3", 1),
    ("C1", "O2", 1), ("O2", "H4", 1),
    ("O3", "C3", 1), ("C3", "H5", 1), ("C3", "H6", 1), ("C3", "C4", 1),
    ("C4", "H7", 1), ("C4", "H8", 1), ("C4", "H9", 1), ("O3", "H10", 1),
]
_EST_AFTER = [
    ("C1", "O1", 2), ("C1", "C2", 1), ("C2", "H1", 1), ("C2", "H2", 1), ("C2", "H3", 1),
    ("C1", "O3", 1), ("O3", "C3", 1), ("C3", "H5", 1), ("C3", "H6", 1), ("C3", "C4", 1),
    ("C4", "H7", 1), ("C4", "H8", 1), ("C4", "H9", 1),
    ("O2", "H4", 1), ("O2", "H10", 1),
]
_EST_RMOL = {"acetyl": "#1", "leavingOH": "#1", "ethoxy": "#1", "leavingH": "#1", "catalyst": "H+"}
_EST_PMOL = {"acetyl": "#1", "ethoxy": "#1", "leavingOH": "#1", "leavingH": "#1", "catalyst": "H+"}


def build_esterification():
    atoms = []
    for aid, el, frag, flocal in _EST_ATOMS:
        f = _EST_FRAGS[frag]
        atoms.append({
            "id": aid, "el": el, "frag": frag, "flocal": flocal,
            "start": K._apply(flocal, f["K0"]["pos"], f["K0"]["rot"]),
            "end": K._apply(flocal, f["K2"]["pos"], f["K2"]["rot"]),
            "rmol": _EST_RMOL[frag], "pmol": _EST_PMOL[frag],
        })
    fragments = [dict(v, id=k) for k, v in _EST_FRAGS.items()]
    acetyl_eth = ["C1", "O1", "C2", "H1", "H2", "H3", "O3", "C3", "H5", "H6", "C4", "H7", "H8", "H9"]
    labels = [
        {"id": "r-acid", "text": " (CH₃COOH)", "color": "red", "phase": "reactant",
         "atoms": ["C1", "O1", "C2", "H1", "H2", "H3", "O2", "H4"]},
        {"id": "r-ethanol", "text": " (C₂H₅OH)", "color": "blue", "phase": "reactant",
         "atoms": ["O3", "C3", "H5", "H6", "C4", "H7", "H8", "H9", "H10"]},
        {"id": "p-ester", "text": " (CH₃COOC₂H₅)", "color": "emerald", "phase": "product",
         "atoms": acetyl_eth},
        {"id": "p-water", "text": " (H₂O)", "color": "cyan", "phase": "product",
         "atoms": ["O2", "H4", "H10"]},
    ]
    return {
        "meta": {"title": "", "subtitle": " +  ",
                 "language": "en", "category": "organic", "accent": "indigo", "engine": "mechanism",
                 "equation": r"\text{CH}_3\text{COOH} + \text{C}_2\text{H}_5\text{OH} "
                             r"\underset{\Delta}{\overset{\text{}}{\rightleftharpoons}} "
                             r"\text{CH}_3\text{COOC}_2\text{H}_5 + \text{H}_2\text{O}"},
        "conditions": {"text": "、", "reversible": True, "transitionGlow": True,
                       "catalyst": {"label": " (H⁺)", "formula": "H^+"}},
        "reactants": [{"species": ""}, {"species": ""}],
        "products": [{"species": ""}, {"species": ""}],
        "atoms": atoms,
        "bonds_before": [{"a": a, "b": b, "order": o} for a, b, o in _EST_BEFORE],
        "bonds_after": [{"a": a, "b": b, "order": o} for a, b, o in _EST_AFTER],
        "fragments": fragments,
        "labels": labels,
        "energy": {"activation": 0.62, "deltaH": -0.12, "reactantLabel": "+", "productLabel": "+"},
        "steps": [
            {"title": "",
             "html": "<span class='text-red-400 font-semibold'> (CH₃COOH)</span>  "
                     "<span class='text-blue-400 font-semibold'> (C₂H₅OH)</span> 。"
                     " <span class='text-cyan-400 font-semibold'> (H⁺)</span> ，。"},
            {"title": "",
             "html": "，："
                     "<span class='border-b border-dashed border-amber-500'> C–OH 、 O–H </span>，"
                     "<span class='border-b border-dashed border-emerald-500'> C–O  H₂O </span>。。"},
            {"title": "",
             "html": " <span class='text-cyan-400 font-semibold'> (H₂O)</span>，"
                     " <span class='text-emerald-400 font-semibold'> (CH₃COOC₂H₅)</span>。"
                     "<span class='text-indigo-300 font-semibold'> H⁺</span> ，“”。"},
        ],
    }


# =====================================================================
# =====================================================================
def build_glucose_combustion():
    return {
        "meta": {
            "title": "",
            "subtitle": "C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O（）",
            "language": "en",
            "category": "inorganic",
            "accent": "amber",
            "engine": "morph",
        },
        "conditions": {"text": "", "exothermic": True, "flame": True},
        "reactants": [
            {"species": "Glucose", "count": 1},
            {"species": "O2", "count": 6},
        ],
        "products": [
            {"species": "CO2", "count": 6},
            {"species": "H2O", "count": 6},
        ],
        "atom_map": [
            ["Glucose#1.C1", "CO2#1.Y"], ["Glucose#1.C2", "CO2#2.Y"],
            ["Glucose#1.C3", "CO2#3.Y"], ["Glucose#1.C4", "CO2#4.Y"],
            ["Glucose#1.C5", "CO2#5.Y"], ["Glucose#1.C6", "CO2#6.Y"],
            ["Glucose#1.O1", "H2O#1.A"], ["Glucose#1.O2", "H2O#2.A"],
            ["Glucose#1.O3", "H2O#3.A"], ["Glucose#1.O4", "H2O#4.A"],
            ["Glucose#1.O5", "H2O#5.A"], ["Glucose#1.O6", "H2O#6.A"],
            ["Glucose#1.H1",  "H2O#1.Ha"], ["Glucose#1.HO2", "H2O#1.Hb"],
            ["Glucose#1.H2",  "H2O#2.Ha"], ["Glucose#1.HO3", "H2O#2.Hb"],
            ["Glucose#1.H3",  "H2O#3.Ha"], ["Glucose#1.HO4", "H2O#3.Hb"],
            ["Glucose#1.H4",  "H2O#4.Ha"], ["Glucose#1.HO5", "H2O#4.Hb"],
            ["Glucose#1.H5",  "H2O#5.Ha"], ["Glucose#1.HO6", "H2O#5.Hb"],
            ["Glucose#1.H6a", "H2O#6.Ha"], ["Glucose#1.H6b", "H2O#6.Hb"],
            ["O2#1.Oa", "CO2#1.Xa"], ["O2#1.Ob", "CO2#1.Xb"],
            ["O2#2.Oa", "CO2#2.Xa"], ["O2#2.Ob", "CO2#2.Xb"],
            ["O2#3.Oa", "CO2#3.Xa"], ["O2#3.Ob", "CO2#3.Xb"],
            ["O2#4.Oa", "CO2#4.Xa"], ["O2#4.Ob", "CO2#4.Xb"],
            ["O2#5.Oa", "CO2#5.Xa"], ["O2#5.Ob", "CO2#5.Xb"],
            ["O2#6.Oa", "CO2#6.Xa"], ["O2#6.Ob", "CO2#6.Xb"],
        ],
        "energy": {
            "activation": 0.25,
            "deltaH": -0.95,
            "reactantLabel": "C₆H₁₂O₆+O₂",
            "productLabel": "CO₂+H₂O",
        },
        "steps": [
            {
                "title": "： 6 ",
                "html": (
                    "<span class='text-amber-300 font-semibold'> (C₆H₁₂O₆)</span>  6 ，"
                    " 1 （C₁=O）、5 （C–OH） 5  C–C ， 24 。"
                    "<span class='text-red-400 font-semibold'>6  O₂</span>  12 。"
                    "<span class='text-amber-400'></span>， △G ≈ −2803 kJ/mol。"
                ),
            },
            {
                "title": "·",
                "html": (
                    "（→→），"
                    "C–C  C–H <span class='border-b border-dashed border-red-400'></span>，"
                    "O=O ；。 <span class='text-red-400 font-semibold'>17+ </span>，"
                    " <span class='text-green-400 font-semibold'>18 </span>（12  C=O  12  O–H）。"
                ),
            },
            {
                "title": " 6CO₂ + 6H₂O · ",
                "html": (
                    "6  2  O₂ ，"
                    "<span class='text-slate-200 font-semibold'> 6  CO₂</span>（， C=O）；"
                    "12  6 ，"
                    "<span class='text-cyan-300 font-semibold'> 6  H₂O</span>（）。"
                    "： 6C · 12H · 18O，。"
                ),
            },
        ],
    }


REGISTRY = {
    "combustion_ch4": build_combustion_ch4,
    "combustion_h2": build_combustion_h2,
    "electrolysis_water": build_electrolysis_water,
    "redox_na_cl2": build_redox_na_cl2,
    "esterification": build_esterification,
    "glucose_combustion": build_glucose_combustion,
}


def main(argv):
    if not argv or argv[0] == "list":
        print(":")
        for k in REGISTRY:
            print("  -", k)
        return
    if argv[0] == "random":
        import random
        seed = int(argv[1]) if len(argv) > 1 else 0
        out = Path(argv[2]) if len(argv) > 2 else (SKILL_DIR / "output" / "random.html")
        key = random.Random(seed).choice(list(REGISTRY))
        render_html(K.assemble_data(REGISTRY[key]()), out)
        print(f"written: {out}  (seed={seed} -> {key})")
        return
    if argv[0] == "all":
        out_dir = Path(argv[1]) if len(argv) > 1 else (SKILL_DIR / "output")
        out_dir.mkdir(parents=True, exist_ok=True)
        for k in REGISTRY:
            render_html(K.assemble_data(REGISTRY[k]()), out_dir / f"{k}.html")
            print("written:", out_dir / f"{k}.html")
        return
    key = argv[0]
    if key not in REGISTRY:
        print(f" {key}；: {', '.join(REGISTRY)}")
        sys.exit(1)
    out = Path(argv[1]) if len(argv) > 1 else (SKILL_DIR / "output" / f"{key}.html")
    render_html(K.assemble_data(REGISTRY[key]()), out)
    print("written:", out)


if __name__ == "__main__":
    main(sys.argv[1:])
