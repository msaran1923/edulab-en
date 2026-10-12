
`lesson` / `steps` / `board`。


```jsonc
"lesson": {
  "language": "zh-CN",                 // ：zh-CN / en
  "answer": "$\\left[-3,\\ \\dfrac{7}{4}\\right]$",  //  LaTeX（）
}
```

expand / current / theoRange`。 `lesson.language="en"`  `lesson.ui`。


```jsonc
"steps": [
  ...
]
```


```jsonc
"board": {
  "conics": [ { "name":"C", "kind":"ellipse", "a":2, "b":1.732, "center":[0,0],
                "color":"curve", "label":"C: x²/4+y²/3=1" } ],
  "points": { "M": {"xy":[-1,0], "color":"vecA", "label":"M(-1,0)"}, "F":[1,0] },
  "param": { "name":"e", "label":" $e$", "min":1.05,"max":3,"step":0.01,
             "value":1.5, "unit":"", "standard":1.5, "ticks":["1","2","3"] },
  "rangeBar": { "of":"dot", "min":-3, "max":1.75, "label":"$[-3,\\ \\frac74]$" },  // /
  "constant": { "of":"kprod", "label":"$-\\dfrac34$" },                            // 
  "trace":    { "of":"Q", "color":"locus" },                                       // （）
}
```
> `rangeBar` / `constant` / `answerBand` 。

| kind |  |  |
|---|---|---|
| `ellipse` | `a`(x ), `b`(y ), `center` | |
| `parabola` | `p`, `center`(), `axis`("x"/"y") | `(y-cy)²=2p(x-cx)`  `(x-cx)²=2p(y-cy)` |
| `circle` | `r`, `center` | |

：`color`、`label`（）、`dashed`、`hidden`、`legend:false`。




`points` / `readouts` 。：`[{"name":"c","expr":"e"},{"name":"b","expr":"sqrt(e*e-1)"}]`。


| type |  |  |
|---|---|---|
| `line_through_slope` | `name, point, slope` | （、） |
| `line_x_eq_my_c` | `name, m, c` |  `x=my+c` |
| `line_through_points` | `name, a, b`() |  |
| `line_through_point_dir` | `name, point, dir:[dx,dy]` |  |
| `intersect_line_line` | `name, a, b`() |  |
| `midpoint` | `name, a, b` |  |
| `point_reflect` | `name, of, center` |  `2·center − of` |
| `foot_perp` | `name, point, line` |  |
| `reflect` | `name, point, line` |  |
| `vector` | `name, from, to`() |  |
| `segment` | `name, a, b, dashed, color` |  |


`id`  `rangeBar.of` / `constant.of` 。

| type |  |  |
|---|---|---|
| `coord` | `of`() | `(x, y)` |
| `length` | `a,b`()  `of`() |  |
| `distance` | `a,b`() |  |
| `dot` | `a,b`() |  |
| `slope_product` | `a,b`() |  |
| `area_triangle` | `pts:[p,q,r]` |  |
| `distance_point_line` | `point, line` |  |

### 3.6 rangeBar / constant / answerBand / trace

