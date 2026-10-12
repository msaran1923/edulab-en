#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate.py — Inject structured data into template/board.html and produce a single-page analytic geometry interactive page.

Data is driven by exact sympy computation in lib/analytic_kernel.py (single source of truth): answer, coordinates, step values,
interactive engine initial values and "theoretical range / fixed value" stay consistent. Each build_* has built-in self-check assertions.

Dependency: sympy. Run with any interpreter that can import sympy:
    python3 scripts/generate.py <problem-key> [output.html]
    python3 scripts/generate.py list
    python3 scripts/generate.py all <output-dir>     # generate all registered problem types
"""

import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "template" / "board.html"
PLACEHOLDER = "__LESSON_DATA__"

sys.path.insert(0, str(SKILL_DIR / "lib"))
import sympy as sp                       # noqa: E402
import conics                            # noqa: E402
import analytic_kernel as K              # noqa: E402


def render_html(data: dict, out_path: Path) -> Path:
    template = TEMPLATE.read_text(encoding="utf-8")
    if PLACEHOLDER not in template:
        raise RuntimeError(f"placeholder {PLACEHOLDER} not found in template")
    out_path.write_text(template.replace(PLACEHOLDER, json.dumps(data, ensure_ascii=False)),
                        encoding="utf-8")
    return out_path


# ---------------- Utilities ----------------
def f(e):
    return float(sp.N(e))


def pt(xy, color="point", label=None, emphasis=False):
    return {"xy": [f(xy[0]), f(xy[1])], "color": color, "label": label, "emphasis": emphasis}


def itv(rg):
    return "$" + rg["latex"] + "$"


def conic_board(c, color="curve", label=None):
    b = dict(c["board"]); b["name"] = "C"; b["color"] = color
    if label:
        b["label"] = label
    return b


# =====================================================================
# 1) Ellipse · dot product · range (flagship)
# =====================================================================
def build_ellipse_dot_range() -> dict:
    E = conics.ellipse(2, sp.sqrt(3))
    M, F = (-1, 0), (1, 0)
    expr, cs = K.dot_product_expr(E, F, M)
    rg = K.range_over_m(expr)
    # Self-check: horizontal line (x-axis) attains -3, vertical line attains 7/4
    assert (rg["lo_f"], rg["hi_f"]) == (-3.0, 1.75) and rg["lo_closed"] and rg["hi_closed"]

    board = {
        "view": {"xRange": [-3.6, 3.6], "yRange": [-2.6, 2.6]},
        "conics": [conic_board(E, label="C: x²/4 + y²/3 = 1")],
        "points": {"M": pt(M, "vecA", "M(-1,0)"), "F": pt(F, "point", "F(1,0)"),
                   "P": pt((1, 1.5), "given", "P")},
        "param": {"name": "θ", "label": "Inclination angle $\\theta$", "min": 0, "max": 180,
                  "step": 0.5, "value": 45, "unit": "°", "standard": 45,
                  "ticks": ["0° (x-axis)", "90°", "180°"]},
        "derived": [
            {"type": "line_through_angle", "name": "l", "point": "F", "angle": "@param", "color": "line"},
            {"type": "intersect_line_conic", "name": ["A", "B"], "line": "l", "conic": "C", "colors": ["ptA", "ptB"]},
            {"type": "vector", "name": "vMA", "from": "M", "to": "A", "color": "vecA"},
            {"type": "vector", "name": "vMB", "from": "M", "to": "B", "color": "vecB"},
        ],
        "readouts": [
            {"id": "F", "label": "Right focus F coordinates", "type": "coord", "of": "F"},
            {"id": "k", "label": "Line slope k", "type": "slope", "of": "l"},
            {"id": "A", "label": "Intersection A", "type": "coord", "of": "A", "color": "ptA"},
            {"id": "B", "label": "Intersection B", "type": "coord", "of": "B", "color": "ptB"},
            {"id": "dot", "label": "Dot product $\\vec{MA}\\cdot\\vec{MB}$", "type": "dot", "a": "vMA", "b": "vMB", "highlight": True},
        ],
        "rangeBar": {"of": "dot", "min": rg["lo_f"], "max": rg["hi_f"], "label": itv(rg)},
        "legend": [{"color": "line", "text": "Moving line l"}, {"color": "vecA", "text": "Vector MA (red)"},
                   {"color": "vecB", "text": "Vector MB (blue)"}],
    }
    lesson = {
        "language": "en", "title": "Ellipse and dynamic vector product range",
        "problem": ("<p class='font-medium text-slate-800'>[Problem]</p>"
                    "<p> $C:\\dfrac{x^2}{a^2}+\\dfrac{y^2}{b^2}=1\\,(a>b>0)$  $e=\\dfrac12$，"
                    " $P\\left(1,\\dfrac32\\right)$。$M(-1,0)$， $F$  $l$  $C$  $A,B$。</p>"
                    "<ol class='list-decimal pl-5 space-y-1'><li> $C$ ；</li>"
                    "<li>Find the range of $\\vec{MA}\\cdot\\vec{MB}$.</li></ol>"),
        "answerLabel": "", "answer": itv(rg),
    }
    steps = [
        {"title": " C ",
         "content": ("<p>$e=\\dfrac{c}{a}=\\dfrac12,\\ c^2=a^2-b^2\\Rightarrow a^2=\\dfrac43b^2$；"
                     " $P\\left(1,\\dfrac32\\right)$  $b^2=3,\\ a^2=4$。</p>"
                     "<div class='text-center py-3 bg-indigo-50 border border-indigo-100 rounded-xl text-indigo-900 font-bold'>"
                     f"$$ {E['eq_latex']} $$</div>")},
        {"title": " + ",
         "content": ("<p>$F(1,0)$。 $l:\\,x=my+1$（，），：</p>"
                     f"<p class='text-center'>$$ {K.tex(cs['A'])}\\,y^2 + {K.tex(cs['B'])}\\,y {K.tex(cs['C'])} = 0 $$</p>"
                     f"<p>：$y_1+y_2={K.tex(cs['ysum'])},\\ y_1y_2={K.tex(cs['yprod'])}$。</p>")},
        {"title": "",
         "content": (f"<p>$\\vec{{MA}}\\cdot\\vec{{MB}}=(m^2+1)y_1y_2+2m(y_1+y_2)+4={K.tex(sp.apart(expr, K.m))}$。</p>"
                     "<p> $3m^2+4\\ge4$  $\\dfrac{19}{3m^2+4}\\in\\left(0,\\dfrac{19}{4}\\right]$，"
                     " $\\dfrac74$；$l$  $x$  $A(2,0),B(-2,0)$  $-3$。</p>"
                     "<div class='text-center py-3 bg-emerald-50 border border-emerald-100 rounded-xl text-emerald-900 font-bold'>"
                     f"$$ \\vec{{MA}}\\cdot\\vec{{MB}}\\in {rg['latex']} $$</div>")},
    ]
    return {"lesson": lesson, "steps": steps, "board": board}


# =====================================================================
# =====================================================================
def build_ellipse_chord_range() -> dict:
    E = conics.ellipse(2, sp.sqrt(3))
    F = (1, 0)
    cl2, cs = K.chord_len_sq_expr(E, F)
    rg2 = K.range_over_m(cl2)               # |AB|^2 ∈ [9,16]
    lo, hi = sp.sqrt(rg2["lo"]), sp.sqrt(rg2["hi"])
    chord_latex = K.interval_latex(lo, hi, rg2["lo_closed"], rg2["hi_closed"])
    assert (f(lo), f(hi)) == (3.0, 4.0)

    board = {
        "view": {"xRange": [-3.6, 3.6], "yRange": [-2.6, 2.6]},
        "conics": [conic_board(E, label="C: x²/4 + y²/3 = 1")],
        "points": {"F1": pt((-1, 0), "point", "F₁(-1,0)"), "F": pt(F, "given", "F(1,0)")},
        "param": {"name": "θ", "label": " AB  $\\theta$", "min": 0, "max": 180,
                  "step": 0.5, "value": 90, "unit": "°", "standard": 90,
                  "ticks": ["0° ()", "90° ()", "180°"]},
        "derived": [
            {"type": "line_through_angle", "name": "l", "point": "F", "angle": "@param", "color": "line"},
            {"type": "intersect_line_conic", "name": ["A", "B"], "line": "l", "conic": "C", "colors": ["ptA", "ptB"]},
            {"type": "segment", "name": "AB", "a": "A", "b": "B", "color": "line2"},
        ],
        "readouts": [
            {"id": "k", "label": "Line slope k", "type": "slope", "of": "l"},
            {"id": "A", "label": "Intersection A", "type": "coord", "of": "A", "color": "ptA"},
            {"id": "B", "label": "Intersection B", "type": "coord", "of": "B", "color": "ptB"},
            {"id": "len", "label": " $|AB|$", "type": "length", "a": "A", "b": "B", "highlight": True},
        ],
        "rangeBar": {"of": "len", "min": f(lo), "max": f(hi), "label": "$" + chord_latex + "$"},
        "legend": [{"color": "line", "text": " l"}],
    }
    lesson = {
        "language": "zh-CN", "title": "",
        "problem": ("<p class='font-medium text-slate-800'>[Problem]</p>"
                    "<p> $C:\\dfrac{x^2}{4}+\\dfrac{y^2}{3}=1$， $F(1,0)$  $l$  $C$  $A,B$。"
                    " $|AB|$ 。</p>"),
        "answerLabel": "", "answer": "$|AB|\\in" + chord_latex + "$",
    }
    steps = [
        {"title": " + ",
         "content": ("<p> $l:\\,x=my+1$， "
                     f"$ {K.tex(cs['A'])}y^2+{K.tex(cs['B'])}y{K.tex(cs['C'])}=0 $，</p>"
                     f"<p>$y_1+y_2={K.tex(cs['ysum'])},\\ y_1y_2={K.tex(cs['yprod'])}$。</p>")},
        {"title": "",
         "content": ("<p>$|AB|^2=(1+m^2)\\left[(y_1+y_2)^2-4y_1y_2\\right]="
                     f"{K.tex(sp.simplify(cl2))}$。</p>"
                     "<p> $u=m^2\\ge0$：$|AB|^2=\\dfrac{144(u+1)}{(3u+4)^2}$， $u$ ，"
                     "$u=0$（·） $9$，$u\\to\\infty$（·） $16$。</p>"
                     "<div class='text-center py-3 bg-emerald-50 border border-emerald-100 rounded-xl text-emerald-900 font-bold'>"
                     f"$$ |AB|\\in {chord_latex} $$</div>")},
    ]
    return {"lesson": lesson, "steps": steps, "board": board}


# =====================================================================
# =====================================================================
def build_ellipse_area_max() -> dict:
    E = conics.ellipse(2, sp.sqrt(3))
    F = (1, 0)
    area, cs = K.triangle_area_expr(E, F, (0, 0))
    rg = K.range_over_m(sp.simplify(area), horizontal_valid=False)   # (0, 3/2]
    assert rg["hi_f"] == 1.5 and rg["hi_closed"] and not rg["lo_closed"]

    board = {
        "view": {"xRange": [-3.6, 3.6], "yRange": [-2.6, 2.6]},
        "conics": [conic_board(E, label="C: x²/4 + y²/3 = 1")],
        "points": {"O": pt((0, 0), "point", "O"), "F": pt(F, "given", "F(1,0)")},
        "param": {"name": "θ", "label": " AB  $\\theta$", "min": 0, "max": 180,
                  "step": 0.5, "value": 90, "unit": "°", "standard": 90,
                  "ticks": ["0°", "90°", "180°"]},
        "derived": [
            {"type": "line_through_angle", "name": "l", "point": "F", "angle": "@param", "color": "line"},
            {"type": "intersect_line_conic", "name": ["A", "B"], "line": "l", "conic": "C", "colors": ["ptA", "ptB"]},
            {"type": "polygon", "name": "tri", "pts": ["O", "A", "B"], "color": "area", "stroke": "line2"},
        ],
        "readouts": [
            {"id": "A", "label": "Intersection A", "type": "coord", "of": "A", "color": "ptA"},
            {"id": "B", "label": "Intersection B", "type": "coord", "of": "B", "color": "ptB"},
            {"id": "len", "label": " $|AB|$", "type": "length", "a": "A", "b": "B"},
            {"id": "area", "label": "$S_{\\triangle OAB}$", "type": "area_triangle", "pts": ["O", "A", "B"], "highlight": True},
        ],
        "rangeBar": {"of": "area", "min": 0.0, "max": rg["hi_f"], "label": itv(rg)},
        "legend": [{"color": "line", "text": " l"}, {"color": "area", "text": "△OAB"}],
    }
    lesson = {
        "language": "zh-CN", "title": "",
        "problem": ("<p class='font-medium text-slate-800'>[Problem]</p>"
                    "<p> $C:\\dfrac{x^2}{4}+\\dfrac{y^2}{3}=1$，$O$ ， $F(1,0)$  $l$  $C$  $A,B$。"
                    " $\\triangle OAB$ 。</p>"),
        "answerLabel": "△OAB ", "answer": "$\\dfrac{3}{2}$",
    }
    steps = [
        {"title": "",
         "content": ("<p> $l:\\,x=my+1$。$S=\\dfrac12|AB|\\cdot d(O,l)=\\dfrac12\\,\\dfrac{|c|}{\\sqrt{1+m^2}}\\,|AB|$。</p>"
                     f"<p> $y_1+y_2={K.tex(cs['ysum'])},\\ y_1y_2={K.tex(cs['yprod'])}$， "
                     f"$S={K.tex(sp.simplify(area))}$。</p>")},
        {"title": "",
         "content": ("<p> $u=m^2\\ge0$：$S=\\dfrac{6\\sqrt{u+1}}{3u+4}$，$S^2=\\dfrac{36(u+1)}{(3u+4)^2}$  $u\\ge0$ "
                     "， $u=0$（）。</p>"
                     "<div class='text-center py-3 bg-emerald-50 border border-emerald-100 rounded-xl text-emerald-900 font-bold'>"
                     "$$ S_{\\max}=\\dfrac{3}{2} $$</div>"
                     "<p class='text-slate-500 text-sm'>（$l$  $x$  $O,A,B$ ， 0， "
                     f"$S\\in {rg['latex']}$。）</p>")},
    ]
    return {"lesson": lesson, "steps": steps, "board": board}


# =====================================================================
# =====================================================================
def build_ellipse_slopeprod_const() -> dict:
    E = conics.ellipse(2, sp.sqrt(3))
    P = (2, 0)
    val = K.slope_product_central(E, P)        # -3/4
    assert sp.simplify(val + sp.Rational(3, 4)) == 0

    board = {
        "view": {"xRange": [-3.2, 3.2], "yRange": [-2.4, 2.4]},
        "conics": [conic_board(E, label="C: x²/4 + y²/3 = 1")],
        "points": {"P": pt(P, "fixed", "P(2,0)", emphasis=True)},
        "param": {"name": "t", "label": " A  $t$", "min": 12, "max": 168,
                  "step": 1, "value": 60, "unit": "°", "standard": 60,
                  "ticks": ["12°", "90°", "168°"]},
        "derived": [
            {"type": "point_on_conic", "name": "A", "conic": "C", "t": "@param", "color": "ptA", "emphasis": True},
            {"type": "point_reflect", "name": "B", "of": "A", "center": [0, 0], "color": "ptB", "emphasis": True},
            {"type": "line_through_points", "name": "PA", "a": "P", "b": "A", "color": "vecA"},
            {"type": "line_through_points", "name": "PB", "a": "P", "b": "B", "color": "vecB"},
            {"type": "segment", "name": "AB", "a": "A", "b": "B", "color": "aux", "dashed": True},
        ],
        "readouts": [
            {"id": "A", "label": " A", "type": "coord", "of": "A", "color": "ptA"},
            {"id": "B", "label": " B", "type": "coord", "of": "B", "color": "ptB"},
            {"id": "kPA", "label": " $k_{PA}$", "type": "slope", "of": "PA"},
            {"id": "kprod", "label": " $k_{PA}\\cdot k_{PB}$", "type": "slope_product", "a": "PA", "b": "PB", "highlight": True},
        ],
        "constant": {"of": "kprod", "label": "$-\\dfrac{3}{4}$"},
        "legend": [{"color": "vecA", "text": " PA"}, {"color": "vecB", "text": " PB"},
                   {"color": "aux", "text": "AB  O"}],
    }
    lesson = {
        "language": "zh-CN", "title": "",
        "problem": ("<p class='font-medium text-slate-800'>[Problem]</p>"
                    "<p> $C:\\dfrac{x^2}{4}+\\dfrac{y^2}{3}=1$，$P(2,0)$ 。$A,B$  $C$ "
                    "（$B=-A$）。 $k_{PA}\\cdot k_{PB}$ 。</p>"),
        "answerLabel": "", "answer": "$k_{PA}\\cdot k_{PB}=-\\dfrac{3}{4}$",
    }
    steps = [
        {"title": "",
         "content": ("<p> $A(x_0,y_0)$， $B(-x_0,-y_0)$， $\\dfrac{x_0^2}{4}+\\dfrac{y_0^2}{3}=1$，"
                     " $y_0^2=3\\left(1-\\dfrac{x_0^2}{4}\\right)=\\dfrac{3(4-x_0^2)}{4}$。</p>")},
        {"title": "",
         "content": ("<p>$k_{PA}\\cdot k_{PB}=\\dfrac{y_0-0}{x_0-2}\\cdot\\dfrac{-y_0-0}{-x_0-2}"
                     "=\\dfrac{-y_0^2}{(x_0-2)(-x_0-2)}=\\dfrac{-y_0^2}{4-x_0^2}$。</p>"
                     "<p> $y_0^2=\\dfrac{3(4-x_0^2)}{4}$：</p>"
                     "<div class='text-center py-3 bg-emerald-50 border border-emerald-100 rounded-xl text-emerald-900 font-bold'>"
                     "$$ k_{PA}\\cdot k_{PB}=\\dfrac{-\\frac{3}{4}(4-x_0^2)}{4-x_0^2}=-\\dfrac{3}{4} $$</div>"
                     "<p class='text-slate-500 text-sm'> $A$ ，。。</p>")},
    ]
    return {"lesson": lesson, "steps": steps, "board": board}


# =====================================================================
# =====================================================================
def build_parabola_dot_const() -> dict:
    PB = conics.parabola(2)                 # y^2 = 4x, focus (1,0)
    F = (1, 0)
    expr, cs = K.dot_product_expr(PB, F, (0, 0))
    const, val = K.is_constant_in_m(expr)
    assert const and sp.simplify(val + 3) == 0

    board = {
        "view": {"xRange": [-2.0, 7.0], "yRange": [-4.0, 4.0]},
        "conics": [conic_board(PB, label="C: y² = 4x")],
        "points": {"O": pt((0, 0), "point", "O"), "F": pt(F, "fixed", "F(1,0)", emphasis=True)},
        "param": {"name": "θ", "label": " $\\theta$", "min": 18, "max": 162,
                  "step": 0.5, "value": 60, "unit": "°", "standard": 60,
                  "ticks": ["18°", "90°", "162°"]},
        "derived": [
            {"type": "line_through_angle", "name": "l", "point": "F", "angle": "@param", "color": "line"},
            {"type": "intersect_line_conic", "name": ["A", "B"], "line": "l", "conic": "C", "colors": ["ptA", "ptB"]},
            {"type": "vector", "name": "vOA", "from": "O", "to": "A", "color": "vecA"},
            {"type": "vector", "name": "vOB", "from": "O", "to": "B", "color": "vecB"},
        ],
        "readouts": [
            {"id": "A", "label": "Intersection A", "type": "coord", "of": "A", "color": "ptA"},
            {"id": "B", "label": "Intersection B", "type": "coord", "of": "B", "color": "ptB"},
            {"id": "k", "label": "Line slope k", "type": "slope", "of": "l"},
            {"id": "dot", "label": "$\\vec{OA}\\cdot\\vec{OB}$", "type": "dot", "a": "vOA", "b": "vOB", "highlight": True},
        ],
        "constant": {"of": "dot", "label": "$-3$"},
        "legend": [{"color": "line", "text": " l"}, {"color": "vecA", "text": " OA"},
                   {"color": "vecB", "text": " OB"}],
    }
    lesson = {
        "language": "zh-CN", "title": "",
        "problem": ("<p class='font-medium text-slate-800'>[Problem]</p>"
                    "<p> $C:y^2=4x$，$O$ ， $F(1,0)$  $l$  $C$  $A,B$。"
                    " $\\vec{OA}\\cdot\\vec{OB}$ 。</p>"),
        "answerLabel": "", "answer": "$\\vec{OA}\\cdot\\vec{OB}=-3$",
    }
    steps = [
        {"title": " + ",
         "content": ("<p> $l:\\,x=my+1$， $y^2=4x$  "
                     f"$ y^2-4my-4=0 $， $y_1+y_2={K.tex(cs['ysum'])},\\ y_1y_2={K.tex(cs['yprod'])}$。</p>"
                     "<p> $x_i=\\dfrac{y_i^2}{4}$， $x_1x_2=\\dfrac{(y_1y_2)^2}{16}=1$。</p>")},
        {"title": "",
         "content": ("<p>$\\vec{OA}\\cdot\\vec{OB}=x_1x_2+y_1y_2=1+(-4)$。</p>"
                     "<div class='text-center py-3 bg-emerald-50 border border-emerald-100 rounded-xl text-emerald-900 font-bold'>"
                     "$$ \\vec{OA}\\cdot\\vec{OB}=-3 $$</div>"
                     "<p class='text-slate-500 text-sm'>，。</p>")},
    ]
    return {"lesson": lesson, "steps": steps, "board": board}


# =====================================================================
# =====================================================================
def build_hyperbola_ecc_range() -> dict:
    k = 3                                   # |PF₁| = k|PF₂|
    rg = K.ecc_range_focal_ratio(k)         # e ∈ (1, 2]
    assert rg["hi_f"] == 2.0 and rg["hi_closed"] and not rg["lo_closed"]

    board = {
        "view": {"xRange": [-4.2, 4.2], "yRange": [-3.0, 3.0]},
        "conics": [{"name": "C", "kind": "hyperbola", "a": 1, "b": "sqrt(e*e-1)",
                    "center": [0, 0], "orient": "x", "asymptotes": True,
                    "color": "curve", "label": "C: x² − y²/(e²−1) = 1  (a=1)"}],
        "points": {
            "F1": {"xy": ["-e", "0"], "color": "point", "label": "F₁"},
            "F2": {"xy": ["e", "0"], "color": "given", "label": "F₂"},
            "P":  {"xy": ["2/e", "sqrt((e*e-1)*(4/(e*e)-1))"], "color": "ptA", "label": "P", "emphasis": True},
        },
        "param": {"name": "e", "label": " $e$", "min": 1.05, "max": 3, "step": 0.01,
                  "value": 1.5, "unit": "", "standard": 1.5, "ticks": ["1", "2", "3"]},
        "derived": [
            {"type": "segment", "name": "PF1", "a": "F1", "b": "P", "color": "vecA"},
            {"type": "segment", "name": "PF2", "a": "F2", "b": "P", "color": "vecB"},
        ],
        "readouts": [
            {"id": "c", "label": " $c=ae$", "type": "expr", "expr": "e", "digits": 2},
            {"id": "pf2", "label": "$|PF_2|$", "type": "distance", "a": "F2", "b": "P"},
            {"id": "pf1", "label": "$|PF_1|$", "type": "distance", "a": "F1", "b": "P"},
            {"id": "cond", "label": " $P$ ", "type": "status",
             "expr": "e", "op": "<=", "rhs": 2, "okText": " ✓", "badText": " ✗", "highlight": True},
        ],
        "answerBand": {"min": 1, "max": 3, "lo": float(rg["lo"]), "hi": rg["hi_f"],
                       "label": "$e\\in" + rg["latex"] + "$"},
        "legend": [{"color": "curve", "text": " C（ e ）"},
                   {"color": "vecA", "text": "|PF₁| = 3|PF₂|"}, {"color": "vecB", "text": "|PF₂|"}],
    }
    lesson = {
        "language": "zh-CN", "title": "",
        "problem": ("<p class='font-medium text-slate-800'>[Problem]</p>"
                    "<p> $C:\\dfrac{x^2}{a^2}-\\dfrac{y^2}{b^2}=1\\,(a,b>0)$， $F_1,F_2$。"
                    " $C$ <strong></strong> $P$  $|PF_1|=3|PF_2|$， $e$ 。</p>"
                    "<p class='text-slate-500 text-sm'>（ $e$，； $e>2$  $P$ 。）</p>"),
        "answerLabel": "", "answer": "$e\\in" + rg["latex"] + "$",
    }
    steps = [
        {"title": "",
         "content": ("<p> $P$， $|PF_1|-|PF_2|=2a$， $|PF_2|\\ge c-a$（）。</p>")},
        {"title": "",
         "content": ("<p> $|PF_1|=3|PF_2|$  $|PF_1|-|PF_2|=2a$  $2|PF_2|=2a$， $|PF_2|=a$。</p>"
                     "<p> $|PF_2|\\ge c-a$：$a\\ge c-a\\Rightarrow c\\le 2a\\Rightarrow e=\\dfrac{c}{a}\\le 2$。 $e>1$。</p>"
                     "<div class='text-center py-3 bg-emerald-50 border border-emerald-100 rounded-xl text-emerald-900 font-bold'>"
                     "$$ e\\in" + rg["latex"] + " $$</div>"
                     "<p class='text-slate-500 text-sm'> $e=2$ ，$P$ ，"
                     "“”，——。</p>")},
    ]
    return {"lesson": lesson, "steps": steps, "board": board}


REGISTRY = {
    "ellipse_dot_range": build_ellipse_dot_range,
    "ellipse_chord_range": build_ellipse_chord_range,
    "ellipse_area_max": build_ellipse_area_max,
    "ellipse_slopeprod_const": build_ellipse_slopeprod_const,
    "parabola_dot_const": build_parabola_dot_const,
    "hyperbola_ecc_range": build_hyperbola_ecc_range,
}


def main(argv):
    if not argv or argv[0] == "list":
        print(":")
        for k in REGISTRY:
            print("  -", k)
        return
    if argv[0] == "all":
        out_dir = Path(argv[1]) if len(argv) > 1 else (SKILL_DIR / "output")
        out_dir.mkdir(parents=True, exist_ok=True)
        for k, fn in REGISTRY.items():
            render_html(fn(), out_dir / f"{k}.html")
            print("written:", out_dir / f"{k}.html")
        return
    key = argv[0]
    if key not in REGISTRY:
        print(f" {key}；: {', '.join(REGISTRY)}")
        sys.exit(1)
    out = Path(argv[1]) if len(argv) > 1 else (SKILL_DIR / "output" / f"{key}.html")
    render_html(REGISTRY[key](), out)
    print("written:", out)


if __name__ == "__main__":
    main(sys.argv[1:])
