




| |  |  |
|---|---|---|



|  |  |
|---|---|
|  `C.pink` |  f |
|  `C.purple` | 、（E、B） |
|  `C.red` | 、、 |


|---|---|---|
|  |  +  | `stamp`、`bbox` |




```js
const run = at(2, 0.05), win = S.dur(2) * 0.75;
const tp = simT(lt, run, win, T1);                       // 
const B = blockAt(tp);                                   //  sPos(tp)
vec(front, vmul(G.up, vel(tp) * VS), { c: C.red, label: `v = ${vel(tp).toFixed(1)}` });
trail(t => midAt(t), 0, tp, { c: C.red });
VT.curve(vel, 0, tp); VT.cursor(tp, vel);
clockTag(560, 830, tp);
txt(` ×${(T1 / win).toFixed(2)}`, 150, 830, { size: 30, c: C.gray, al: 'left' });
```



