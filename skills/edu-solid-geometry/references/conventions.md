



- `cuboid(lx, ly, lz)` / `cube(edge)` —  $A$ ，$AB$  $x$、$AD$  $y$、$AA_1$  $z$。



| query.type |  | kernel  |
|---|---|---|
| `line_plane_angle` | $\sin\theta = \dfrac{|\vec v\cdot\vec n|}{|\vec v||\vec n|}$ | `line_plane_angle_sin(v, n)` |
| `line_line_angle` | $\cos\theta = \dfrac{|\vec{d_1}\cdot\vec{d_2}|}{|\vec{d_1}||\vec{d_2}|}$ | `line_line_angle_cos(d1, d2)` |
| `point_plane_distance` | $d = \dfrac{|(P-P_0)\cdot\vec n|}{|\vec n|}$ | `point_plane_distance(P, P0, n)` |







