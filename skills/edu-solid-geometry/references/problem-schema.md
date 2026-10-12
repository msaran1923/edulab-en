


```jsonc
{
  "language": "zh-CN",            // ：zh-CN / en / ...
  "body": "regular_quad_pyramid", // ， conventions.md
  "dims": { "base_edge": 2, "height": 1 },  // 
  "givens": [                     //  / 
    { "name": "E", "kind": "midpoint", "of": ["P", "C"] }
  ],
  "query": {                      // 
    "type": "line_plane_angle",   //  conventions.md 
    "line": ["B", "E"],
    "plane": ["P", "A", "C"]
  }
}
```




```jsonc
{
  "lesson": {
    "language": "zh-CN",
    "title": "…………",
    "answerLabel": "…………",
    "answerValue": "$\\frac{2\\sqrt{22}}{11}$",  // LaTeX， $…$
  },
  "steps": [
    {
      "title": "",
      "cameraPos": { "x": 4, "y": 4.5, "z": 4 } // （three ）
    }
  ],
  "model": {
    "points": { "P": [0, 1.5, 0], "A": [2.12, 0, 0] },  // three （y ）， kernel.to_three
    "spheres": ["P", "A", "B", "C", "D", "E"],           // +
    "edges": [                                            // 
      { "a": "A", "b": "B" },
      { "a": "D", "b": "A", "dashed": true },             // 
      { "a": "B", "b": "D", "color": "aux", "dashed": true, "name": "Line_BD" } //  highlight
    ],
      "Line_BE":  { "type": "line",  "a": "B", "b": "E", "color": "emphasis", "depthTest": false },
      "Plane_PAC":{ "type": "plane", "pts": ["P", "A", "C"] },         // 3  4 
      "Normal_Vector": { "type": "arrow", "origin": "O", "dir": [0,0,1], "length": 1.5, "color": "normal" },
      "Axis":     { "type": "axes",  "size": 3 }
    },
    "target": [0, 0.45, 0],        // OrbitControls （three ）
    "initialCamera": [5, 4, 5]     // 
  }
}
```

- `plane` —  `pts`（3  4 ）。
- `axes` —  `size`。
  - `a`、`b`：（）。
  - `label`： LaTeX（ `$`）， `"2"`、`"2\\sqrt{2}"`、`"\\frac{\\sqrt3}{2}"`。




```jsonc
"model": {
  "scale": 1.4,                       //  kernel.to_three  scale 
  "mathPoints": { "A1": [2,0,2], "C1": [0,2,2], "P": [0.5,1.5,2], "C": [0,2,0], "B1": [0,0,2], "A": [2,0,0] },
  "draggable": {
    "along": ["A1", "C1"],            // （）
    "standardLabel": " A₁P=3PC₁",
      { "label": " B₁-APC ", "type": "volume_tetra", "pts": ["B1","A","P","C"] },
      { "label": "A₁P ", "type": "length", "pts": ["A1","P"] }
    ]
  }
}
```
- readout `type` ：`volume_tetra`(4 )、`length`(2 )、`line_plane_angle_sin`(`line`:2 , `plane`:3 )。

