#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""


def _edge(a, b, **kw):
    e = {"a": a, "b": b}
    e.update(kw)
    return e


def quad_pyramid(apex="P", base=("A", "B", "C", "D")):
    a, b, c, d = base
    edges = [
        _edge(a, b), _edge(b, c), _edge(c, d), _edge(d, a),
        _edge(apex, a), _edge(apex, b), _edge(apex, c), _edge(apex, d),
    ]
    return {"spheres": [apex, a, b, c, d], "edges": edges}


def tri_pyramid(apex="P", base=("A", "B", "C")):
    a, b, c = base
    edges = [
        _edge(a, b), _edge(b, c), _edge(c, a),
        _edge(apex, a), _edge(apex, b), _edge(apex, c),
    ]
    return {"spheres": [apex, a, b, c], "edges": edges}


def cuboid(bottom=("A", "B", "C", "D"), top=("A1", "B1", "C1", "D1")):
    a, b, c, d = bottom
    a1, b1, c1, d1 = top
    edges = [
        _edge(a, b), _edge(b, c), _edge(c, d), _edge(d, a),       # 
        _edge(a1, b1), _edge(b1, c1), _edge(c1, d1), _edge(d1, a1),  # 
        _edge(a, a1), _edge(b, b1), _edge(c, c1), _edge(d, d1),   # 
    ]
    return {"spheres": [a, b, c, d, a1, b1, c1, d1], "edges": edges}


def prism(bottom=("A", "B", "C"), top=("A1", "B1", "C1")):
    n = len(bottom)
    edges = []
    for i in range(n):
        edges.append(_edge(bottom[i], bottom[(i + 1) % n]))
        edges.append(_edge(top[i], top[(i + 1) % n]))
        edges.append(_edge(bottom[i], top[i]))
    return {"spheres": list(bottom) + list(top), "edges": edges}
