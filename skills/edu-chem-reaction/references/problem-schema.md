

---

```jsonc
"meta": {
  "title": "",              // 
  "accent": "amber",                 // ：amber/indigo/emerald/sky/violet/cyan/red/green/orange...
  "engine": "morph",                 // auto | morph | mechanism（auto：organic  fragments → mechanism）
}
```

```jsonc
"conditions": {
  "reversible": true,        //  ⇌
  "exothermic": true,        // （）
  "transitionGlow": true,    // （）
}
```

```jsonc
"reactants": [ {"species":"CH4","count":1,"pos":[-4,0.2,0]}, {"species":"O2","count":2} ],
"products":  [ {"species":"CO2","count":1,"pos":[-2.7,1.1,0]}, {"species":"H2O","count":2} ],
"atom_map": [
  ["O2#1.Oa",  "CO2#1.Xa"], ...
]
```

|  | slot |
|---|---|
|  `H2 O2 N2 Cl2` | `Ha,Hb` / `Oa,Ob` / `Na,Nb` / `Cla,Clb` |
| `CO` | `C,O` |
|  `CO2` | `Y`(C), `Xa,Xb`(O) |
|  `H2O` | `A`(O), `Ha,Hb` |
|  `CH4` | `C, H1,H2,H3,H4` |
|  `NH3` | `A`(N), `H1,H2,H3` |
|  `Na C Fe Mg` | `X` |
|  `NaCl` | `Na, Cl` |


```jsonc
"atoms": [
  {"id":"C1","el":"C","frag":"acetyl","flocal":[0,0.2,0],
   "start":[...world...],"end":[...world...],"rmol":"#1","pmol":"#1"}, ...
],
"bonds_before": [ {"a":"C1","b":"O1","order":2}, {"a":"C1","b":"O2","order":1}, ... ],
"bonds_after":  [ {"a":"C1","b":"O3","order":1}, {"a":"O2","b":"H10","order":1}, ... ],
"fragments": [
  {"id":"acetyl",   "K0":{"pos":[-4.5,0.5,0],"rot":[0,0,0]}, "K1":{...}, "K2":{...}},
  {"id":"catalyst", "catalyst":true, "K0":{...},"K1":{...},"K2":{...}}
],
"labels": [ {"id":"r-acid","text":" (CH₃COOH)","color":"red","phase":"reactant","atoms":["C1","O1",...]}, ... ]
```

```jsonc
"steps": [
  {"title":"","html":"……"},
  {"title":"","html":"……"}
]
```

```jsonc
               "reactantLabel":"CH₄+O₂", "productLabel":"CO₂+H₂O" }  // deltaH<0 、>0 
```

`{ meta, conditions, atoms[{id,el,color,radius,start,end,frag?,flocal?,rmol,pmol}],
   bonds{before,after,broken,formed,kept}, labels[], elementCounts{}, legend[],
   steps[], fragments[], energy, electrons[], ui{} }`
