# Companion Notebooks — Book 2

Twelve interactive Jupyter notebooks, one per chapter. They are the book's
**Layer-2 playground**: sliders, animations, and drills that let you *do* the
ideas the chapters describe — shrink an $h$ and watch a secant become a
tangent, dial up a Taylor degree and watch the polynomial wrap a curve, turn a
learning rate past the cliff and watch gradient descent explode.

No installation required — click **Open in Colab** on any chapter to run it free
in your browser.

| # | Notebook | Plays with | Open |
|--:|---|---|---|
| 1 | `ch1_sequences.ipynb` | ε–N tolerance game, the $1^\infty$ race, the $\sqrt{2+a_n}$ cobweb | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MeiraDavidson/math_module2/blob/main/notebooks/ch1_sequences.ipynb) |
| 2 | `ch2_limits.ipynb` | zoom into a hole, ε–δ explorer, bisection root-finder, $\sin(x)/x$ | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MeiraDavidson/math_module2/blob/main/notebooks/ch2_limits.ipynb) |
| 3 | `ch3_derivative.ipynb` | secant→tangent, derivative-as-a-function, corner/cusp zoom | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MeiraDavidson/math_module2/blob/main/notebooks/ch3_derivative.ipynb) |
| 4 | `ch4_rules.ipynb` | rule detector, product-rule area animation, chain-rule builder | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MeiraDavidson/math_module2/blob/main/notebooks/ch4_rules.ipynb) |
| 5 | `ch5_exponentials.ipynb` | base-$a$ slope $M(a)=\ln a$, half-life decay simulator | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MeiraDavidson/math_module2/blob/main/notebooks/ch5_exponentials.ipynb) |
| 6 | `ch6_mvt.ipynb` | find the parallel tangent, slope-sign → shape | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MeiraDavidson/math_module2/blob/main/notebooks/ch6_mvt.ipynb) |
| 7 | `ch7_taylor.ipynb` | Taylor slider, remainder envelope, divergence, Euler's $e^{ix}$ | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MeiraDavidson/math_module2/blob/main/notebooks/ch7_taylor.ipynb) |
| 8 | `ch8_convexity.ipynb` | classify critical points, convexity checker, convex-vs-not descent | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MeiraDavidson/math_module2/blob/main/notebooks/ch8_convexity.ipynb) |
| 9 | `ch9_newton_gradient_descent.ipynb` | **the centerpiece** — GD playground, Newton, two-valley, momentum | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MeiraDavidson/math_module2/blob/main/notebooks/ch9_newton_gradient_descent.ipynb) |
| 10 | `ch10_integral.ipynb` | Riemann sums, antiderivative drill, substitution, area accumulator | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MeiraDavidson/math_module2/blob/main/notebooks/ch10_integral.ipynb) |
| 11 | `ch11_fundamental_theorem.ipynb` | moving-edge FTC, evaluator, by-parts, log-as-area | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MeiraDavidson/math_module2/blob/main/notebooks/ch11_fundamental_theorem.ipynb) |
| 12 | `ch12_series.ipynb` | partial sums, integral test, radius of convergence, bouncing ball | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MeiraDavidson/math_module2/blob/main/notebooks/ch12_series.ipynb) |

## Running them locally

```bash
pip install jupyterlab ipywidgets matplotlib numpy
cd notebooks
jupyter lab            # or: jupyter notebook
```

Open a notebook and **run every cell from the top** (Run ▸ Run All, or
Shift+Enter down the page). Each widget appears under its explanation — drag
the sliders and the picture responds live. Requires `ipywidgets` (works in
JupyterLab and classic Notebook).

## Regenerating

The notebooks are generated from small builder scripts (`nb_ch1.py` …
`nb_ch12.py`) that share `nbbuild.py`, mirroring the `figures/` setup. To
rebuild all twelve:

```bash
cd notebooks
python3 build_all_notebooks.py
```

This emits clean (unexecuted) notebooks. They have all been verified to execute
end-to-end without errors via `jupyter nbconvert --execute`.
