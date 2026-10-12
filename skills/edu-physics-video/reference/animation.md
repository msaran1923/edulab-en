


`index.html` ：`build/timeline.js`（ render.mjs  timeline.json ）→ `engine.js` → `phys.js` → `anim.js` → `boot()`。



```
y=0    ┌──────────────────────────────────────────────────────────────┐
       │ 01  Tag (x 64~700, y 40~105)                             │
y=130  │ ┌────  ────────────┐  ┌────  board() ─────────┐ │
       │ │ x 60 ~ 900             │  │ x 930 ~ 1870, y 130 ~ 880    │ │
       │ │ y 130 ~ 860            │  │ bl()  0~10 ， 62       │ │
       │ │                        │  │  i  y = 192 + 62*i       │ │
       │ └────────────────────────┘  └──────────────────────────────┘ │
y=914  │            ┌──────── （）────────┐                  │
y=1044 │            └───────────────────────────────┘                  │
y=1080 └──────────────────────────────────────────────────────────────┘
```


```js
SC.solve = (lt, S) => {
  const { P, at } = S;
  board(1);
  bl(0, ' Compute:', 0, lt, { c: C.gray, size: 32 }); // 
  bl(3, 'CD = 2.5', at(1, 0.2), lt, { c: C.red, size: 50 });
  stamp(1560, 760, '：CD = 2.5', P(at(1, 0.7), 0.5), C.red, 50);
};
```
- `lt`：。
- `S.cue(k)`、`S.dur(k)`、`S.n`（）。




****
|  |  |
|---|---|
| `line(x1,y1,x2,y2,o)` |  |
| `circ(cx,cy,r,o)` |  |
| `ellPts(cx,cy,rx,ry,a0,a1,n)` | /， draw / fillPts |
| `quadPts(x0,y0,cx,cy,x1,y1)` |  |
| `fnPts(f, x0, x1, toScreen)` |  y=f(x) （ `axes().S`） |
| `mid(p,q)`、`mix2(p,q,t)`、`lerp`、`clamp` |  |

****
|  |  |
|---|---|
| `dot(x,y,col,r)` |  |
| `rightM(V, A, B, col, size, p)` |  |
| `angM(V, A, B, col, r, p)` |  |
| `tickM(p, q, n, col, pp)` | （n ） |
| `paraM(p, q, col, pp)` | （ >） |

****
|  |  |
|---|---|
| `lb(zh, en, x, y, o)` | + |
| `board(p)` |  |
| `stamp(x, y, str, p, col, size, rot)` | （） |
| `bubble(x, y, str, p, o)` |  |

|  |  |
|---|---|

****
|  |  |
|---|---|
| `scaleAt(x, y, k, fn)` |  (x,y)  |

****：`problemCard(p)`、`hiBox(box, col, t, lt)`（）。

****：
```js
const ax = axes({ ox: 300, oy: 600, sx: 70, sy: 70, xr: [-3, 5], yr: [-2, 5], step: 1 });
draw(fnPts(x => (x - 1) ** 2 - 1, -1.2, 3.2, ax.S), { c: C.blue, w: 5, p: P(at(0), 1.5) });
ptLabel('P', ax.S([1, -1]), 30, 20, 1, C.red);                     // ax.S([x,y])  → 
```
：`ox + xr[0]*sx ≥ 60`，`ox + xr[1]*sx ≤ 880`，`oy - yr[1]*sy ≥ 150`，`oy - yr[0]*sy ≤ 850`。

```js
CAM.cx = 470; CAM.cy = 520; CAM.s = 160; CAM.target = [0, 0, 1];   //  anim.js 
const G = { A: [-2, 0, 0], B: [2, 0, 0], P: [0, 0, 2], ... };
L3(G.A, G.B);                      // 3D 
draw(arc3(G.O, G.A, G.P, 0.4), { c: C.red, w: 3 });   // 3D 
const q = pr(G.P);                 // 3D  →  [x,y]， ptLabel / fillPts
```

```js
const at_s = s => s <= 60 ? mix2(A, B, s / 60) : mix2(B, C_, (s - 60) / 80);   //  s → 
const tau = lerp(-10, 7.5, eio(P(at(1), 3)));                                     // ""
const pj = at_s(4 * (tau + 10));  token('', ...pj, C.red);
```



****：`vadd(a,b)`、`vsub`、`vmul(a,k)`、`vlen`、`vdot`、`vunit`、`vperp(a)`（ 90°）、`polar(len, ang)`、`deg(37)`。

**（）**
|  |  |
|---|---|
| `mwidth(s, size, font)` | mtx  |

****
|  |  |
|---|---|
| `vecA(from, len, ang, o)` |  +  |

****
|  |  |
|---|---|
| `arcMark(x, y, r, a0, a1, label, p, col, lr)` |  +  |
| `notToScale(p)` | "（）" |

****
|  |  |
|---|---|
| `trail(pos, t0, t1, o)` | ：`pos(t) → [x, y]`；`o.dots: 0.1`  |
| `clockTag(x, y, t)`、`readout(x, y, name, val, unit)` | 、 |
| `graph(o)` | v-t / x-t ：`{ox, oy, w, h, xr, yr, xl, yl, xt, yt}` → `{S, draw(p), curve(f, x0, x1, o), area(f, x0, x1, col, a), cursor(x, f, col)}` |

****
|  |  |
|---|---|
| `spot(x, y, a, col)` |  |
| `glassBlock(cx, cy, w, h, ang, p)` |  |

```js
const A1 = 10, T1 = 1, XMAX = 5, A2 = 2, T2 = Math.sqrt(5);
const sPos = t => t <= T1 ? V0 * t - 0.5 * A1 * t * t : XMAX - 0.5 * A2 * (t - T1) ** 2;
const vel  = t => t <= T1 ? V0 - A1 * t : -A2 * (t - T1);
const G = incline([200, 780], TH, 640, 1, { p: 0 });
const blockAt = t => block(G.at(S0 + PXM * sPos(t)), BW, BH, ANG, { p: 0 });
```


`anim.js` ：
```js
const PROBLEM = {
  src: 'problem.png', srcW: 1500, srcH: 240,          // 
    AC: [[773, 44, 915, 116]],
    mid: [[1123, 44, 1422, 116], [34, 124, 184, 196]],
  },
};
```
intro ：
```js
hiBox(PROBLEM.boxes.AC, C.blue, at(1, 0.2), lt);      //  1  20% 
chip('AC = 3', 800, C.blue, P(at(1, 0.8), 0.5));      // 
```
：
- ****：



- [ ] ** JS **（render.mjs  `FAILED` / `PAGE ERROR`）



