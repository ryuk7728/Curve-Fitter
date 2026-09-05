# Parametric Curve Parameter Recovery

This repository recovers the unknown parameters $\theta$, $M$, and $X$
of the supplied parametric curve from the unordered points in `xy_data.csv`.

## Final result

| Parameter | Recovered value |
|---|---:|
| $\theta$ | $29.999973^\circ$ |
| $M$ | $0.0299999974$ |
| $X$ | $54.9999982$ |
| Mean L1 loss | $2.5598\times10^{-6}$ |

These numerical values correspond to the clean solution

$$
\boxed{\theta=30^\circ,\qquad M=0.03,\qquad X=55}.
$$

The resulting curve is

$$
\left(
t\cos\left(\frac{\pi}{6}\right)-e^{0.03|t|}\sin(0.3t)\sin\left(\frac{\pi}{6}\right)+55,
\;42+t\sin\left(\frac{\pi}{6}\right)+e^{0.03|t|}\sin(0.3t)\cos\left(\frac{\pi}{6}\right)
\right),\quad 6<t<60.
$$

## Repository structure

```text
.
├── README.md          # Results, repository contents, and run instructions
├── APPROACH.md        # Explanation of the solution approach
├── solve_curve.py     # Parameter-fitting implementation
├── xy_data.csv        # Supplied curve points
├── result.json        # Recovered parameters and L1 loss
├── requirements.txt   # Python dependencies
└── .gitignore         # Files excluded from Git
```

## Run locally

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the solver from the repository directory:

```bash
python solve_curve.py
```

The program prints the fitted values and writes them to `result.json`.
