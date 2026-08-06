# CaribeApp — Jersey Distribution for the Juegos Caribe

![Juegos Caribe](images/Caribe.png)

A **Mixed-Integer Linear Programming** model, wrapped in a web app, that decides how a limited stock of team jerseys should be split across the faculties competing in the *Juegos Deportivos Caribe* — the inter-faculty games of the University of Havana.

Built for a real client (the games' organising committee) as the Mathematical Models course project, Facultad de Matemática y Computación, University of Havana, 2024.

**▶ Live app: <https://caribe.streamlit.app/>**

> 🇪🇸 Original Spanish version, including the full mathematical formulation and the project log: [`README.es.md`](./README.es.md)

---

## The problem

The committee has *N* jerseys spread across a handful of colours and has to hand them out to ~18 faculties. Everyone wants more than there is, and the rules that govern "fair" are partly hard and partly negotiable:

**Hard constraints**
1. Every jersey is handed out — total assigned equals total available.
2. Each faculty gets exactly **one** colour (they compete as a bloc).
3. No colour is over-allocated beyond its stock.
4. No faculty is left with zero.

**Soft constraints, in priority order** — the solver satisfies as many as it can, respecting the ordering:
1. A faculty never receives more jerseys than it has registered athletes.
2. A faculty never receives fewer jerseys than one ranked below it.
3. A faculty with fewer than 10 athletes receives exactly one per athlete.
4. If faculty *A* has more athletes than *B*, *A* gets at least as many jerseys.
5. If a faculty's preferred colour has enough stock left, give it that colour.

**Objective** — minimise total deviation from proportional fairness:

$$\min \sum_{i \in \text{faculties}} \left| \frac{x_i}{\text{athletes}_i} - \overline{p} \right|, \qquad \overline{p} = \frac{T}{\sum_k \text{athletes}_k}$$

where $x_i$ is the number of jerseys assigned to faculty $i$ and $T$ the total stock. The absolute value is linearised with an auxiliary variable and two one-sided constraints, keeping the model linear.

Fixed allocations for referees, professors, and the Association of Former Caribe Athletes (AAAC) are subtracted up front, and faculties under 10 athletes are settled directly, so the MILP only handles the contested part of the stock.

---

## Why MILP and not a heuristic

Genetic algorithms, simulated annealing, hill climbing, and tabu search were all considered. MILP won on three counts specific to *this* problem:

- **Optimality is checkable.** The soft constraints encode a real committee's fairness policy; "close enough" is a political problem, not just a numerical one. MILP either proves optimality or reports the gap.
- **Priorities are first-class.** Ranking the soft constraints maps directly onto weighted-sum / lexicographic objectives. In GA or SA the same thing becomes penalty-term tuning, and the resulting ordering is implicit and fragile.
- **No local optima to escape.** Local-search methods stall; branch-and-bound doesn't.

The instance size makes the tradeoff cheap — the problem is small enough that exactness costs seconds, not hours.

### Solver performance

`PuLP` (CBC backend) with a 30-second cap; it returns the best incumbent if the cap is hit.

| Faculties | Colours | Jerseys | Time (s) |
| --- | --- | --- | --- |
| 2 | 2 | 100 | 0.07 |
| 4 | 2 | 250 | 0.33 |
| 7 | 3 | 350 | 1.62 |
| 11 | 3 | 600 | 7.83 |
| 16 | 4 | 1350 | 30.33 |

18 faculties is the realistic ceiling for the Juegos Caribe, so the cap is only reached at the top of the expected range — where the incumbent is already good.

---

## Using the app

<table>
  <tr>
    <td align="center"><img src="images/01main_screen_dark.png" width="300"><br><sub>Main screen</sub></td>
    <td align="center"><img src="images/02introducing_data.png" width="300"><br><sub>Colour stock</sub></td>
  </tr>
  <tr>
    <td align="center"><img src="images/03introducing_data2.png" width="300"><br><sub>Faculty data</sub></td>
    <td align="center"><img src="images/04execution.png" width="300"><br><sub>Results</sub></td>
  </tr>
</table>

1. Enter the fixed reserves for referees, professors, and the AAAC.
2. Set the number of colours, then each colour's name and available stock.
3. Set the number of faculties, then for each one: name, athlete count, ranking position, and preferred colour. **Always fill in the athlete count** — if the exact figure isn't known, an estimate from previous years produces a far better solution than leaving it blank.
4. Press **Ejecutar**.

The input set can be downloaded as `.json` and reloaded later. Results can be exported to PDF from `Settings → Print`, and pushed to Telegram via [@el_indio_de_los_caribe_bot](https://t.me/el_indio_de_los_caribe_bot) by entering a username. Light and dark themes are both available under `Settings`.

Two full demo runs are included as PDFs: [horizontal](<./Caribe Demo. Vista Horizontal.pdf>), [vertical](<./Caribe Demo. Vista Vertical.pdf>).

---

## Running locally

```bash
pip install -r requirements.txt
streamlit run src/main.py
```

**Stack:** Python · [PuLP](https://pypi.org/project/PuLP/) (CBC solver) · Streamlit · Telegram Bot API.

```
src/
├─ main.py          # Streamlit UI, input model, validation
├─ PuLP_Solver.py   # MILP formulation and solve
├─ time_testing.py  # benchmark harness behind the table above
└─ pages/Readme.py  # in-app documentation
```

---

## A note on how it was built

The project went through three technology stacks before landing. Flutter was dropped for Python packaging incompatibilities; Flet got as far as a working build before Android permission issues around subprocess execution made the solver unusable on device; Streamlit was the third and final choice, which also meant reconceiving the app as a web tool rather than a mobile one. The client was consulted at each pivot. The full log is in [`README.es.md`](./README.es.md#bitácora-del-proyecto).

---

## Authors

- **Daniel Machado Pérez** — [@DanielMPMatCom](https://github.com/DanielMPMatCom)
- **Osvaldo R. Moreno Prieto** — [@Val020213](https://github.com/Val020213)
- **Daniel Toledo Martínez** — [@Phann020126](https://github.com/Phann020126)

## References

1. COIN-OR Foundation. *PuLP: A Python linear programming API*. <https://coin-or.github.io/pulp/>
2. Python Package Index. *PuLP*. <https://pypi.org/project/PuLP/>
