#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reaction_kernel.py — “”。

（ sympy kernel ）：
  1. ：/， sympy （）。
  2. /：、、/。
  3. ：，“(start)”“(end)”。
  4. ：bonds_before / bonds_after → broken / formed / kept（、）。
  5.  data（、、、、、、）。

（ data）：
  - （species + atom_map）：“”，kernel  +  + 。
  - （ atoms + bonds_before/after + fragments）：。

： sympy（ kernel ）。： RDKit，
 SMILES （rdkit_available ；）。
"""

import math
import sympy as sp

import molecules as M


# ===========================================================================
# ===========================================================================
def rdkit_available():
    try:
        import rdkit  # noqa: F401
        return True
    except Exception:
        return False


# ===========================================================================
# ===========================================================================
def _rot_matrix(rot):
    rx, ry, rz = (rot + [0, 0, 0])[:3] if isinstance(rot, list) else (0, 0, 0)
    cx, sx = math.cos(rx), math.sin(rx)
    cy, sy = math.cos(ry), math.sin(ry)
    cz, sz = math.cos(rz), math.sin(rz)
    # R = Rz Ry Rx
    return [
        [cz * cy, cz * sy * sx - sz * cx, cz * sy * cx + sz * sx],
        [sz * cy, sz * sy * sx + cz * cx, sz * sy * cx - cz * sx],
        [-sy,     cy * sx,                cy * cx],
    ]


def _apply(local, pos, rot):
    R = _rot_matrix(rot)
    x, y, z = local
    wx = R[0][0] * x + R[0][1] * y + R[0][2] * z + pos[0]
    wy = R[1][0] * x + R[1][1] * y + R[1][2] * z + pos[1]
    wz = R[2][0] * x + R[2][1] * y + R[2][2] * z + pos[2]
    return [round(wx, 4), round(wy, 4), round(wz, 4)]


# ===========================================================================
# ===========================================================================
def balanced_coefficients(reactant_species, product_species):
    """
    、 id （，）。
     (r_coef, p_coef)：。
    """
    species = list(reactant_species) + list(product_species)
    elements = sorted({el for s in species for el in M.atom_counts(s)})
    rows = []
    for el in elements:
        row = [M.atom_counts(s).get(el, 0) for s in reactant_species]
        row += [-M.atom_counts(s).get(el, 0) for s in product_species]
        rows.append(row)
    A = sp.Matrix(rows)
    ns = A.nullspace()
    if len(ns) != 1:
        raise ValueError(f"（={len(ns)}）：{reactant_species}->{product_species}")
    vec = ns[0]
    denoms = [sp.nsimplify(v).as_numer_denom()[1] for v in vec]
    lcm = sp.ilcm(*denoms) if denoms else 1
    ints = [int(sp.nsimplify(v) * lcm) for v in vec]
    g = 0
    for v in ints:
        g = math.gcd(g, abs(v))
    ints = [v // g for v in ints] if g else ints
    if any(v < 0 for v in ints):
        ints = [-v for v in ints]
    n = len(reactant_species)
    return ints[:n], ints[n:]


# ===========================================================================
# ===========================================================================
def _expand(side_list, default_y=0.0):
    inst = []
    counter = {}
    for entry in side_list:
        sp_id = entry["species"]
        cnt = entry.get("count", 1)
        for _ in range(cnt):
            counter[sp_id] = counter.get(sp_id, 0) + 1
            inst.append({
                "id": f"{sp_id}#{counter[sp_id]}",
                "species": sp_id,
                "pos": entry.get("pos"),
                "rot": entry.get("rot", [0, 0, 0]),
                "explicit": entry.get("pos") is not None,
            })
    k = len(inst)
    spacing = 3.4
    for i, it in enumerate(inst):
        if not it["explicit"]:
            it["pos"] = [round((i - (k - 1) / 2.0) * spacing, 3),
                         round(default_y + (0.6 if i % 2 else -0.6), 3), 0.0]
    return inst


def _instance_atoms(inst):
    mol = M.get(inst["species"])
    refs = {}
    for a in mol["atoms"]:
        ref = f"{inst['id']}.{a['slot']}"
        refs[ref] = {"el": a["el"], "world": _apply(a["pos"], inst["pos"], inst["rot"])}
    bonds = [(f"{inst['id']}.{b['a']}", f"{inst['id']}.{b['b']}", b["order"]) for b in mol["bonds"]]
    return refs, bonds


# ===========================================================================
# ===========================================================================
def resolve_high_level(spec):
    r_inst = _expand(spec["reactants"])
    p_inst = _expand(spec["products"])

    r_refs, r_bonds = {}, []
    for it in r_inst:
        refs, bonds = _instance_atoms(it)
        r_refs.update(refs)
        r_bonds += bonds
    p_refs, p_bonds = {}, []
    for it in p_inst:
        refs, bonds = _instance_atoms(it)
        p_refs.update(refs)
        p_bonds += bonds

    amap = spec["atom_map"]
    map_r = [pair[0] for pair in amap]
    map_p = [pair[1] for pair in amap]

    if set(map_r) != set(r_refs):
        missing = set(r_refs) - set(map_r)
        extra = set(map_r) - set(r_refs)
        raise ValueError(f"atom_map ： {sorted(missing)}； {sorted(extra)}")
    if set(map_p) != set(p_refs):
        missing = set(p_refs) - set(map_p)
        extra = set(map_p) - set(p_refs)
        raise ValueError(f"atom_map ： {sorted(missing)}； {sorted(extra)}")
    if len(map_r) != len(set(map_r)) or len(map_p) != len(set(map_p)):
        raise ValueError("atom_map （）")

    rid, pid, atoms_out = {}, {}, []
    el_counter = {}
    for rr, pr in amap:
        el = r_refs[rr]["el"]
        if p_refs[pr]["el"] != el:
            raise ValueError(f"：{rr}({el}) ↔ {pr}({p_refs[pr]['el']})")
        el_counter[el] = el_counter.get(el, 0) + 1
        aid = f"{el}{el_counter[el]}"
        rid[rr] = pid[pr] = aid
        atoms_out.append({
            "id": aid, "el": el,
            "color": M.element_color(el), "radius": M.element_radius(el),
            "start": r_refs[rr]["world"], "end": p_refs[pr]["world"],
            "rmol": rr.split(".")[0], "pmol": pr.split(".")[0],
        })

    before = [{"a": rid[a], "b": rid[b], "order": o} for a, b, o in r_bonds]
    after = [{"a": pid[a], "b": pid[b], "order": o} for a, b, o in p_bonds]
    return atoms_out, before, after, r_inst, p_inst


# ===========================================================================
# ===========================================================================
def resolve_low_level(spec):
    """
    spec["atoms"]: [{id,el,start,end,rmol,pmol, frag?, flocal?}]
    spec["bonds_before"/"bonds_after"]: [{a,b,order}]（ id）
     reactants/products （）。
    """
    atoms_out = []
    for a in spec["atoms"]:
        el = a["el"]
        atoms_out.append({
            "id": a["id"], "el": el,
            "color": M.element_color(el), "radius": M.element_radius(el),
            "start": a["start"], "end": a["end"],
            "rmol": a.get("rmol"), "pmol": a.get("pmol"),
            **({"frag": a["frag"]} if a.get("frag") else {}),
            **({"flocal": a["flocal"]} if a.get("flocal") is not None else {}),
        })
    before = [dict(b) for b in spec.get("bonds_before", [])]
    after = [dict(b) for b in spec.get("bonds_after", [])]
    r_inst = _expand(spec.get("reactants", []))
    p_inst = _expand(spec.get("products", []))
    return atoms_out, before, after, r_inst, p_inst


# ===========================================================================
# ===========================================================================
def _bkey(b):
    return (tuple(sorted([b["a"], b["b"]])), b["order"])


def bond_diff(before, after):
    bset = {_bkey(b): b for b in before}
    aset = {_bkey(b): b for b in after}
    broken = [b for k, b in bset.items() if k not in aset]
    formed = [b for k, b in aset.items() if k not in bset]
    kept = [b for k, b in aset.items() if k in bset]
    return broken, formed, kept


def element_counts(atoms):
    counts = {}
    for a in atoms:
        counts[a["el"]] = counts.get(a["el"], 0) + 1
    return counts


def verify_conservation(atoms, before, after):
    counts = element_counts(atoms)
    ids = {a["id"] for a in atoms}
    for b in before + after:
        if b["a"] not in ids or b["b"] not in ids:
            raise ValueError(f"：{b}")
    return counts


def _grouped(inst_list):
    order, cnt = [], {}
    for it in inst_list:
        s = it["species"]
        if s not in cnt:
            order.append(s)
        cnt[s] = cnt.get(s, 0) + 1
    return [(s, cnt[s]) for s in order]


def _term(latex, c):
    return latex if c == 1 else f"{c}\\,{latex}"


def equation_latex(r_groups, p_groups, conditions):
    left = " + ".join(_term(M.get(s)["latex"], c) for s, c in r_groups)
    right = " + ".join(_term(M.get(s)["latex"], c) for s, c in p_groups)
    cond = conditions or {}
    over = cond.get("catalyst", {}).get("formula") if cond.get("catalyst") else cond.get("text")
    under = cond.get("under")
    if cond.get("catalyst") and cond.get("text"):
        over = cond["catalyst"]["formula"]
        under = under or cond["text"]
    arrow_body = r"\rightleftharpoons" if cond.get("reversible") else r"\longrightarrow"
    if over and under:
        arrow = rf"\underset{{\text{{{under}}}}}{{\overset{{\text{{{over}}}}}{{{arrow_body}}}}}"
    elif over:
        if cond.get("reversible"):
            arrow = rf"\overset{{\text{{{over}}}}}{{{arrow_body}}}"
        else:
            arrow = rf"\xrightarrow{{\text{{{over}}}}}"
    else:
        arrow = arrow_body
    return f"{left} \\;{arrow}\\; {right}"


# ===========================================================================
# ===========================================================================
def resolve_engine(spec):
    eng = spec.get("meta", {}).get("engine", "auto")
    if eng in ("morph", "mechanism"):
        return eng
    if spec.get("fragments") or spec.get("meta", {}).get("category") == "organic":
        return "mechanism"
    return "morph"


def _labels(atoms, r_inst, p_inst):
    out = []
    for side, insts, key in (("reactant", r_inst, "rmol"), ("product", p_inst, "pmol")):
        for it in insts:
            ids = [a["id"] for a in atoms if a.get(key) == it["id"]]
            if not ids:
                continue
            mol = M.get(it["species"])
            out.append({
                "id": f"{side}-{it['id']}",
                "text": f"{mol['name']} ({mol['formula']})",
                "color": mol["color"], "phase": side, "atoms": ids,
            })
    return out


UI_ZH = {
    "reactants": "", "products": "", "progress": "",
    "play": "", "pause": "", "reset": "",
    "prev": "", "next": "",
    "hint": "、，。",
    "drag": " ·  · ",
    "legend": "", "conservation": "", "energy": "·",
    "broken": "", "formed": "",
    "labels": "", "labelsHint": " / ",
}
UI_EN = {
    "reactants": "Reactants", "products": "Products", "progress": "Reaction progress",
    "play": "Auto play", "pause": "Pause", "reset": "Reset",
    "prev": "Prev", "next": "Next",
    "hint": "Drag the slider to watch bonds break, atoms recombine and mass conserve, or click a step.",
    "drag": "Drag to rotate · scroll to zoom · right-drag to pan",
    "legend": "Atom legend", "conservation": "Atom conservation", "energy": "Energy · progress",
    "broken": "Bonds broken", "formed": "Bonds formed",
    "labels": "Labels", "labelsHint": "Show / hide molecule labels",
}


# ===========================================================================
# ===========================================================================
def assemble_data(spec):
    meta = dict(spec.get("meta", {}))
    lang = meta.get("language", "zh-CN")
    is_en = str(lang).lower().startswith("en")

    if "atoms" in spec:                       # （）
        atoms, before, after, r_inst, p_inst = resolve_low_level(spec)
    else:                                     # （species + atom_map）
        atoms, before, after, r_inst, p_inst = resolve_high_level(spec)

    verify_conservation(atoms, before, after)
    broken, formed, kept = bond_diff(before, after)

    cat_frags = {f["id"] for f in spec.get("fragments", []) if f.get("catalyst")}
    counted = [a for a in atoms if a.get("frag") not in cat_frags]
    counts = element_counts(counted)

    legend = [{"el": el, "color": M.element_color(el),
               "name": M.ELEMENTS.get(el, {}).get("en" if is_en else "zh", el)}
              for el in counts]

    r_groups, p_groups = _grouped(r_inst), _grouped(p_inst)
    r_species = [s for s, _ in r_groups]
    p_species = [s for s, _ in p_groups]
    try:
        rc, pc = balanced_coefficients(r_species, p_species)
        got = {s: c for s, c in r_groups} | {s: c for s, c in p_groups}
        want = {s: c for s, c in zip(r_species, rc)} | {s: c for s, c in zip(p_species, pc)}
        if got != want:
            raise AssertionError(f" {got}  sympy  {want} ")
    except (ValueError, KeyError):
        pass  # ，（ meta.equation ）

    eq = meta.get("equation") or equation_latex(r_groups, p_groups, spec.get("conditions"))

    engine = resolve_engine(spec)
    data = {
        "meta": {
            "title": meta.get("title", ""),
            "subtitle": meta.get("subtitle", ""),
            "language": lang,
            "category": meta.get("category", "junior"),
            "accent": meta.get("accent", "indigo"),
            "engine": engine,
            "equation": eq,
        },
        "conditions": spec.get("conditions", {}),
        "atoms": atoms,
        "bonds": {"before": before, "after": after,
                  "broken": broken, "formed": formed, "kept": kept},
        "labels": spec.get("labels") or _labels(atoms, r_inst, p_inst),
        "elementCounts": counts,
        "legend": legend,
        "steps": spec.get("steps", []),
        "fragments": spec.get("fragments", []),
        "energy": spec.get("energy"),
        "electrons": spec.get("electrons", []),
        "ui": UI_EN if is_en else UI_ZH,
    }
    return data


# ===========================================================================
# ===========================================================================
def _selfcheck():
    rc, pc = balanced_coefficients(["CH4", "O2"], ["CO2", "H2O"])
    assert (rc, pc) == ([1, 2], [1, 2]), (rc, pc)

    rc, pc = balanced_coefficients(["H2", "O2"], ["H2O"])
    assert (rc, pc) == ([2, 1], [2]), (rc, pc)

    rc, pc = balanced_coefficients(["Na", "Cl2"], ["NaCl"])
    assert (rc, pc) == ([2, 1], [2]), (rc, pc)

    spec = {
        "meta": {"title": "", "category": "junior", "engine": "morph"},
        "conditions": {"text": "", "under": ""},
        "reactants": [{"species": "H2O", "count": 2}],
        "products": [{"species": "H2", "count": 2}, {"species": "O2", "count": 1}],
        "atom_map": [
            ["H2O#1.A", "O2#1.Oa"], ["H2O#2.A", "O2#1.Ob"],
            ["H2O#1.Ha", "H2#1.Ha"], ["H2O#1.Hb", "H2#1.Hb"],
            ["H2O#2.Ha", "H2#2.Ha"], ["H2O#2.Hb", "H2#2.Hb"],
        ],
        "steps": [{"title": "", "html": ""},
                  {"title": "", "html": "O-H "},
                  {"title": "", "html": ""}],
    }
    data = assemble_data(spec)
    assert data["elementCounts"] == {"O": 2, "H": 4}, data["elementCounts"]
    assert len(data["atoms"]) == 6
    assert len(data["bonds"]["broken"]) == 4, data["bonds"]["broken"]
    assert len(data["bonds"]["formed"]) == 3, data["bonds"]["formed"]
    assert data["meta"]["engine"] == "morph"
    print("reaction_kernel self-check OK ✓  rdkit_available =", rdkit_available())
    print("  electrolysis equation:", data["meta"]["equation"])


if __name__ == "__main__":
    _selfcheck()
