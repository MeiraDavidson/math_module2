"""Builder for the Chapter 7 companion notebook (Taylor series).

Run:
    /opt/anaconda3/bin/python nb_ch7.py
emits ch7_taylor.ipynb in this folder. Validate by executing with nbconvert.

All Taylor coefficients are computed from the *known* closed-form series
(e^x, sin, cos, 1/(1-x), ln(1+x)) — no sympy required.
"""
import nbbuild as nbb

TITLE = "Building a Function From Its Derivatives"
SUBTITLE = ("a curve is a line, then a parabola, then a polynomial — and you "
            "choose how close")
BLURB = (
    "Four live pictures of the chapter's one machine: replace a smooth curve, "
    "near a point, with a **polynomial** that matches it to whatever order you "
    "like. Push the degree up and watch the Taylor polynomial hug the curve "
    "over a wider window; shade the *remainder* to see exactly where the "
    "approximation can be trusted; watch the geometric series track inside "
    "$|x|<1$ and explode past the walls; and finally watch $e^{ix}$ trace the "
    "unit circle, its shadows drawing $\\cos x$ and $\\sin x$ — Euler's formula, "
    "in motion."
)

# ----------------------------------------------------------------------------
# A small library of Taylor-coefficient generators, shared by widgets 1 & 2.
# Each entry: (numpy function, c_k generator, plot window, pretty name, note).
# c_k is the coefficient of x^k in the Maclaurin series about 0.
# These come straight from the chapter's boxed series — no sympy.
# ----------------------------------------------------------------------------
COEFF_LIB = r"""
from math import factorial

# Maclaurin coefficient c_k (coefficient of x^k) for each flagship function.
def _coef_exp(k):   return 1.0 / factorial(k)                 # e^x
def _coef_sin(k):   return 0.0 if k % 2 == 0 else (-1.0)**((k - 1)//2) / factorial(k)
def _coef_cos(k):   return 0.0 if k % 2 == 1 else (-1.0)**(k//2) / factorial(k)
def _coef_geo(k):   return 1.0                                # 1/(1-x)
def _coef_log(k):   return 0.0 if k == 0 else (-1.0)**(k - 1) / k   # ln(1+x)

# name -> (f(x), coefficient generator, (xlo, xhi), (ylo, yhi))
FUNCS = {
    'e^x':       (lambda x: np.exp(x),        _coef_exp, (-4.0, 4.0), (-2.0, 12.0)),
    'sin x':     (lambda x: np.sin(x),        _coef_sin, (-2*np.pi, 2*np.pi), (-2.5, 2.5)),
    'cos x':     (lambda x: np.cos(x),        _coef_cos, (-2*np.pi, 2*np.pi), (-2.5, 2.5)),
    '1/(1-x)':   (lambda x: 1.0/(1.0 - x),    _coef_geo, (-0.95, 0.95), (-3.0, 12.0)),
    'ln(1+x)':   (lambda x: np.log1p(x),      _coef_log, (-0.9, 0.9), (-3.0, 2.0)),
}

def taylor_coeffs(name, n):
    '''The list [c_0, c_1, ..., c_n] for the named function, about 0.'''
    cgen = FUNCS[name][1]
    return [cgen(k) for k in range(n + 1)]

def taylor_eval(name, n, x):
    '''Evaluate the degree-n Taylor polynomial T_n at the array x (Horner).'''
    cs = taylor_coeffs(name, n)
    out = np.zeros_like(np.asarray(x, dtype=float))
    for c in reversed(cs):           # Horner: ((c_n)x + c_{n-1})x + ...
        out = out * x + c
    return out

def taylor_latex(name, n, maxterms=6):
    '''A short LaTeX string for T_n (first few nonzero terms, then dots).'''
    cs = taylor_coeffs(name, n)
    terms = []
    for k, c in enumerate(cs):
        if abs(c) < 1e-12:
            continue
        # render the coefficient as a clean fraction where we can
        from fractions import Fraction
        frac = Fraction(c).limit_denominator(10**6)
        mag = abs(frac)
        sign = '-' if c < 0 else '+'
        if k == 0:
            body = f'{mag}'
        else:
            xpow = 'x' if k == 1 else f'x^{{{k}}}'
            body = xpow if mag == 1 else (
                f'\\tfrac{{{mag.numerator}}}{{{mag.denominator}}}{xpow}'
                if mag.denominator != 1 else f'{mag.numerator}{xpow}')
        terms.append((sign, body))
        if len(terms) >= maxterms:
            break
    if not terms:
        return '0'
    head = terms[0][1] if terms[0][0] == '+' else '-' + terms[0][1]
    rest = ''.join(f' {s} {b}' for s, b in terms[1:])
    tail = ' + \\cdots' if any(abs(c) > 1e-12 for c in taylor_coeffs(name, n + 4)[n+1:]) else ''
    return head + rest + tail
"""


def build():
    cells = [
        nbb.header(7, TITLE, SUBTITLE, BLURB),
        nbb.setup_cell(),

        # Shared coefficient library (one quiet code cell, no output).
        nbb.code(COEFF_LIB),

        # ---------------------------------------------------------------
        # Widget 1 — The Taylor slider
        # ---------------------------------------------------------------
        nbb.md(
            "## 1. The Taylor slider\n\n"
            "The whole machine in one control. The **Taylor polynomial** of "
            "degree $n$ for $f$ about $0$ is\n\n"
            "$$T_n(x) = \\sum_{k=0}^{n}\\frac{f^{(k)}(0)}{k!}\\,x^k,$$\n\n"
            "and for our five flagships the coefficients $\\frac{f^{(k)}(0)}{k!}$ "
            "have a clean closed form — $\\frac{1}{k!}$ for $e^x$, the "
            "alternating odd/even terms for $\\sin$ and $\\cos$, all $1$'s for "
            "$\\frac{1}{1-x}$, and $\\frac{(-1)^{k-1}}{k}$ for $\\ln(1+x)$ — so "
            "we never need to differentiate anything numerically.\n\n"
            "Pick a function (blue) and push the degree $n$ up. The polynomial "
            "$T_n$ (red) starts as the tangent line, becomes a parabola, then "
            "bend after bend it **clings to the curve over a wider and wider "
            "window** — *(Figure 7.3)*."
        ),
        nbb.code(
            "def _taylor_slider(func='e^x', n=1):\n"
            "    f, _, (xlo, xhi), (ylo, yhi) = FUNCS[func]\n"
            "    xs = np.linspace(xlo, xhi, 800)\n"
            "    fig, ax = plt.subplots()\n"
            "    ax.plot(xs, f(xs), color=BLUE, lw=2.6, label=f'$f(x) = {func}$',\n"
            "            zorder=3)\n"
            "    ax.plot(xs, taylor_eval(func, n, xs), color=RED, lw=2.4, ls='--',\n"
            "            label=f'$T_{{{n}}}(x)$', zorder=4)\n"
            "    ax.scatter([0], [f(0.0)], s=55, color=DARK, zorder=6)\n"
            "    ax.axhline(0, color=GRAY, lw=0.8, ls=':')\n"
            "    ax.set_xlim(xlo, xhi); ax.set_ylim(ylo, yhi)\n"
            "    ax.set_xlabel('$x$'); ax.set_ylabel('$y$')\n"
            "    ax.set_title(f'$T_{{{n}}}(x) = {taylor_latex(func, n)}$',\n"
            "                 color=DARK, fontsize=12)\n"
            "    ax.legend(loc='upper left', framealpha=0.9, fontsize=11)\n"
            "    plt.show()\n"
            "\n"
            "interact(_taylor_slider,\n"
            "         func=Dropdown(options=list(FUNCS), value='e^x',\n"
            "                       description='f(x)'),\n"
            "         n=IntSlider(value=1, min=0, max=18, step=1,\n"
            "                     description='degree n'));\n"
        ),

        # ---------------------------------------------------------------
        # Widget 2 — The remainder, shaded
        # ---------------------------------------------------------------
        nbb.md(
            "## 2. How wrong is it? The remainder, shaded\n\n"
            "An approximation you can't bound is a guess. Write "
            "$f(x) = T_n(x) + R_n(x)$, where the **remainder** "
            "$R_n(x) = f(x) - T_n(x)$ is everything the polynomial missed. "
            "Below, the salmon region is the *actual* error $|f(x) - T_n(x)|$ as "
            "$x$ moves away from the center.\n\n"
            "Watch its shape: the error is essentially $0$ in a window around "
            "$0$ — flat against the axis, the zone you can trust — and then "
            "**peels upward** as you leave that window. Raise $n$ and the trusty "
            "window widens; for $e^x$, $\\sin$, $\\cos$ it widens without bound, "
            "while for $\\frac{1}{1-x}$ and $\\ln(1+x)$ the error stays stubborn "
            "past the wall at $x=1$ no matter how high you climb. The lower panel "
            "shows the same error on a log scale, where the trustworthy valley is "
            "unmistakable."
        ),
        nbb.code(
            "def _remainder(func='e^x', n=3):\n"
            "    f, _, (xlo, xhi), _ = FUNCS[func]\n"
            "    xs = np.linspace(xlo, xhi, 800)\n"
            "    err = np.abs(f(xs) - taylor_eval(func, n, xs))\n"
            "\n"
            "    fig, (ax, axlog) = plt.subplots(2, 1, figsize=(7.2, 6.0),\n"
            "                                    sharex=True,\n"
            "                                    gridspec_kw={'height_ratios': [2, 1]})\n"
            "    # Top: f vs T_n with the error shaded between them.\n"
            "    ax.plot(xs, f(xs), color=BLUE, lw=2.4, label=f'$f(x) = {func}$',\n"
            "            zorder=3)\n"
            "    ax.plot(xs, taylor_eval(func, n, xs), color=RED, lw=2.2, ls='--',\n"
            "            label=f'$T_{{{n}}}(x)$', zorder=4)\n"
            "    ax.fill_between(xs, f(xs), taylor_eval(func, n, xs), color=SHADE2,\n"
            "                    alpha=0.85, label='$|f - T_n|$', zorder=2)\n"
            "    ax.axvline(0, color=GRAY, lw=0.8, ls=':')\n"
            "    f0 = f(0.0)\n"
            "    ax.set_ylim(f0 - 6, f0 + 6)\n"
            "    ax.set_ylabel('$y$')\n"
            "    ax.set_title(f'Degree {n}: where $T_n$ is trustworthy, and where '\n"
            "                 f'it peels away', color=DARK, fontsize=12)\n"
            "    ax.legend(loc='upper left', framealpha=0.9, fontsize=10)\n"
            "    # Bottom: the error magnitude itself, shaded to the axis.\n"
            "    axlog.fill_between(xs, 1e-16, err + 1e-16, color=SHADE2, alpha=0.9,\n"
            "                       zorder=2)\n"
            "    axlog.plot(xs, err + 1e-16, color=RED, lw=1.6, zorder=3)\n"
            "    axlog.set_yscale('log')\n"
            "    axlog.set_ylim(1e-14, 1e3)\n"
            "    axlog.set_xlabel('$x$'); axlog.set_ylabel('$|R_n(x)|$')\n"
            "    axlog.set_title('the same error, log scale (low valley = trustworthy)',\n"
            "                    color=DARK, fontsize=10)\n"
            "    plt.tight_layout()\n"
            "    plt.show()\n"
            "\n"
            "interact(_remainder,\n"
            "         func=Dropdown(options=list(FUNCS), value='e^x',\n"
            "                       description='f(x)'),\n"
            "         n=IntSlider(value=3, min=0, max=16, step=1,\n"
            "                     description='degree n'));\n"
        ),

        # ---------------------------------------------------------------
        # Widget 3 — Divergence: the geometric series and its walls
        # ---------------------------------------------------------------
        nbb.md(
            "## 3. The walls at $x = \\pm 1$: a series that diverges\n\n"
            "A Taylor series is a *local* promise — true only where it "
            "converges. The cleanest warning is the geometric series\n\n"
            "$$\\frac{1}{1-x} = 1 + x + x^2 + x^3 + \\cdots,$$\n\n"
            "which holds **only for $|x| < 1$**. Inside that band the partial "
            "sums $1 + x + \\cdots + x^N$ (red, increasing $N$) crowd in on the "
            "true curve $\\frac{1}{1-x}$ (blue). But step past the dashed walls "
            "at $x = \\pm 1$ and they don't just lag — they **fly off**, "
            "alternating ever more wildly. Plug in $x = 2$ and the left side is "
            "$-1$ while the right side is $1 + 2 + 4 + \\cdots = +\\infty$. Push "
            "$N$ up and see the convergence tighten inside the band and the "
            "explosion worsen outside it."
        ),
        nbb.code(
            "def _diverge(N=4):\n"
            "    fig, ax = plt.subplots()\n"
            "    # The true function, drawn on each side of its pole at x=1.\n"
            "    xl = np.linspace(-2.4, 0.985, 400)\n"
            "    xr = np.linspace(1.015, 2.4, 400)\n"
            "    ax.plot(xl, 1.0/(1.0 - xl), color=BLUE, lw=2.8,\n"
            "            label=r'$\\frac{1}{1-x}$', zorder=5)\n"
            "    ax.plot(xr, 1.0/(1.0 - xr), color=BLUE, lw=2.8, zorder=5)\n"
            "    # Partial sums 1 + x + ... + x^N over the whole window.\n"
            "    xs = np.linspace(-2.4, 2.4, 700)\n"
            "    psum = np.zeros_like(xs)\n"
            "    for k in range(N + 1):\n"
            "        psum = psum + xs**k\n"
            "    ax.plot(xs, psum, color=RED, lw=2.2, ls='--',\n"
            "            label=f'$1 + x + \\\\cdots + x^{{{N}}}$', zorder=4)\n"
            "    # The walls of the interval of convergence.\n"
            "    ax.axvspan(-1, 1, color=SHADEG, alpha=0.35, zorder=0,\n"
            "               label='$|x|<1$ (converges)')\n"
            "    ax.axvline(-1, color=DARK, lw=1.2, ls=':')\n"
            "    ax.axvline(1, color=DARK, lw=1.2, ls=':')\n"
            "    ax.axhline(0, color=GRAY, lw=0.8, ls=':')\n"
            "    ax.set_xlim(-2.4, 2.4); ax.set_ylim(-8, 12)\n"
            "    ax.set_xlabel('$x$'); ax.set_ylabel('$y$')\n"
            "    ax.set_title(f'Geometric partial sum, N = {N}: hugs inside, '\n"
            "                 f'explodes outside', color=DARK, fontsize=12)\n"
            "    ax.legend(loc='upper center', framealpha=0.9, fontsize=10)\n"
            "    plt.show()\n"
            "\n"
            "interact(_diverge,\n"
            "         N=IntSlider(value=4, min=0, max=30, step=1,\n"
            "                     description='terms N'));\n"
        ),

        # ---------------------------------------------------------------
        # Widget 4 — Euler's formula in motion
        # ---------------------------------------------------------------
        nbb.md(
            "## 4. Euler's formula, in motion\n\n"
            "Feed an *imaginary* input into the exponential series and the terms "
            "sort themselves into the cosine and sine series:\n\n"
            "$$e^{ix} = \\cos x + i\\sin x.$$\n\n"
            "So as $x$ runs from $0$ to $2\\pi$, the point $e^{ix}$ travels once "
            "around the **unit circle**. Its two shadows are the trigonometric "
            "functions: the horizontal coordinate (the real part) draws "
            "$\\cos x$, and the vertical coordinate (the imaginary part) draws "
            "$\\sin x$. Run the animation below — the green dot rides the circle "
            "on the left while its projections trace the two waves on the right. "
            "At $x = \\pi$ the dot sits at $-1$, which is Euler's identity "
            "$e^{i\\pi} = -1$ — *(Figure 7.7)*."
        ),
        nbb.code(
            "_FRAMES = 60\n"
            "_xmax = 2*np.pi\n"
            "_theta = np.linspace(0, 2*np.pi, 240)\n"
            "\n"
            "fig, (axc, axw) = plt.subplots(1, 2, figsize=(9.6, 4.4),\n"
            "                               gridspec_kw={'width_ratios': [1, 1.5]})\n"
            "\n"
            "def _frame(i):\n"
            "    x = _xmax * i / (_FRAMES - 1)\n"
            "    c, s = np.cos(x), np.sin(x)\n"
            "\n"
            "    # ---- Left: the unit circle and the moving point e^{ix}. ----\n"
            "    axc.clear()\n"
            "    axc.plot(np.cos(_theta), np.sin(_theta), color=GRAY, lw=1.6,\n"
            "             zorder=1)\n"
            "    axc.plot([0, c], [0, s], color=PURPLE, lw=2.0, zorder=2)\n"
            "    # dropped lines to each axis -> the two shadows\n"
            "    axc.plot([c, c], [0, s], color=BLUE, lw=1.4, ls=':', zorder=2)\n"
            "    axc.plot([0, c], [s, s], color=RED, lw=1.4, ls=':', zorder=2)\n"
            "    axc.scatter([c], [s], s=90, color=GREEN, zorder=5)\n"
            "    axc.scatter([c], [0], s=45, color=BLUE, zorder=4)   # cos shadow\n"
            "    axc.scatter([0], [s], s=45, color=RED, zorder=4)    # sin shadow\n"
            "    axc.axhline(0, color=LIGHT, lw=0.8); axc.axvline(0, color=LIGHT, lw=0.8)\n"
            "    axc.set_xlim(-1.4, 1.4); axc.set_ylim(-1.4, 1.4)\n"
            "    axc.set_aspect('equal')\n"
            "    axc.set_title(f'$e^{{ix}}$,  $x = {x:.2f}$', color=DARK, fontsize=12)\n"
            "    axc.grid(False)\n"
            "\n"
            "    # ---- Right: the two shadows tracing cos x and sin x. ----\n"
            "    axw.clear()\n"
            "    xx = np.linspace(0, _xmax, 240)\n"
            "    axw.plot(xx, np.cos(xx), color=LIGHT, lw=1.2, zorder=1)\n"
            "    axw.plot(xx, np.sin(xx), color=LIGHT, lw=1.2, zorder=1)\n"
            "    upto = np.linspace(0, x, max(2, int(240 * (i + 1) / _FRAMES)))\n"
            "    axw.plot(upto, np.cos(upto), color=BLUE, lw=2.4,\n"
            "             label=r'$\\cos x = \\mathrm{Re}\\,e^{ix}$', zorder=3)\n"
            "    axw.plot(upto, np.sin(upto), color=RED, lw=2.4,\n"
            "             label=r'$\\sin x = \\mathrm{Im}\\,e^{ix}$', zorder=3)\n"
            "    axw.scatter([x], [c], s=70, color=BLUE, zorder=5)\n"
            "    axw.scatter([x], [s], s=70, color=RED, zorder=5)\n"
            "    axw.axhline(0, color=GRAY, lw=0.8, ls=':')\n"
            "    axw.set_xlim(0, _xmax); axw.set_ylim(-1.4, 1.4)\n"
            "    axw.set_xlabel('$x$')\n"
            "    axw.set_title('the shadows draw the two waves', color=DARK,\n"
            "                  fontsize=12)\n"
            "    axw.legend(loc='upper right', framealpha=0.9, fontsize=10)\n"
            "    return ()\n"
            "\n"
            "ani = animation.FuncAnimation(fig, _frame, frames=_FRAMES, interval=80)\n"
            "plt.close(fig)\n"
            "HTML(ani.to_jshtml())\n"
        ),

        nbb.md(
            "---\n\n"
            "*Four readings of one idea. The slider builds the polynomial; the "
            "shaded panel keeps it honest about its error; the walls at "
            "$x = \\pm 1$ show that the promise is local; and Euler's circle "
            "shows the same series, fed an imaginary input, weaving the "
            "exponential and the two trig functions into a single object. Carry "
            "the leading-term idea into Chapter 8, where reading the first "
            "surviving Taylor term at a critical point *is* the second-derivative "
            "test.*"
        ),
    ]
    nbb.build("ch7_taylor.ipynb", cells)


if __name__ == "__main__":
    build()
