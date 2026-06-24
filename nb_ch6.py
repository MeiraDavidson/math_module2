"""Builder for the Chapter 6 companion notebook (the Mean Value Theorem).

Run:
    /opt/anaconda3/bin/python nb_ch6.py
emits ch6_mvt.ipynb in this folder. Validate by executing with nbconvert.
"""
import nbbuild as nbb

TITLE = "The Mean Value Theorem"
SUBTITLE = "somewhere, your speedometer read exactly your average speed"
BLURB = (
    "Two live pictures of the chapter's one theorem and its payoff: tilt an "
    "interval until a tangent line goes *parallel* to the secant — the average "
    "rate of change, achieved as an instantaneous one at an interior point — "
    "and then watch the **sign** of the derivative dictate exactly where a "
    "curve rises and where it falls (Consequence 2, the engine of Chapter 8)."
)


def build():
    cells = [
        nbb.header(6, TITLE, SUBTITLE, BLURB),
        nbb.setup_cell(),

        # ---------------------------------------------------------------
        # Widget 1 — Find the parallel tangent (the MVT)
        # ---------------------------------------------------------------
        nbb.md(
            "## 1. Find the parallel tangent\n\n"
            "The **Mean Value Theorem** says that for a smooth $f$ on $[a,b]$, "
            "*some* interior point $c$ has\n\n"
            "$$f'(c) = \\frac{f(b) - f(a)}{b - a}.$$\n\n"
            "The right side is the slope of the **secant** line through the two "
            "endpoints of the graph — your trip's average rate of change. The "
            "theorem promises a tangent line, touching the curve at an interior "
            "$c$, that is exactly **parallel** to it: at the instant $c$, your "
            "speedometer reads your trip average.\n\n"
            "Pick a curve and drag the endpoints $a$ and $b$. The gray line is "
            "the secant; the red line is the tangent at a $c$ found *numerically* "
            "(by scanning $(a,b)$ for the point where $f'$ matches the secant "
            "slope). Notice the two slopes are equal, and $c$ sits strictly "
            "inside — *(Figure 6.2)*."
        ),
        nbb.code(
            "_CURVES1 = {\n"
            "    'f(x) = x^3 - x':        (lambda x: x**3 - x,\n"
            "                              lambda x: 3*x**2 - 1),\n"
            "    'f(x) = sin(x)':         (lambda x: np.sin(x),\n"
            "                              lambda x: np.cos(x)),\n"
            "    'f(x) = x^2':            (lambda x: x**2,\n"
            "                              lambda x: 2*x),\n"
            "    'f(x) = e^{x/2}':        (lambda x: np.exp(x/2),\n"
            "                              lambda x: 0.5*np.exp(x/2)),\n"
            "}\n"
            "\n"
            "def _find_c(fp, a, b, n=4000):\n"
            "    '''Scan (a,b) for an interior c where f'(c) equals the secant slope.'''\n"
            "    cs = np.linspace(a, b, n)[1:-1]        # strictly interior\n"
            "    target = (_f(b) - _f(a)) / (b - a)\n"
            "    k = int(np.argmin(np.abs(fp(cs) - target)))\n"
            "    return cs[k], target\n"
            "\n"
            "def _f(x):\n"
            "    return _CURRENT_F(x)\n"
            "\n"
            "def _mvt(curve='f(x) = x^3 - x', a=-1.0, b=1.5):\n"
            "    global _CURRENT_F\n"
            "    f, fp = _CURVES1[curve]\n"
            "    _CURRENT_F = f\n"
            "    if b - a < 0.3:            # keep the interval non-degenerate\n"
            "        b = a + 0.3\n"
            "    c, slope = _find_c(fp, a, b)\n"
            "\n"
            "    fig, ax = plt.subplots()\n"
            "    pad = 0.25 * (b - a)\n"
            "    xs = np.linspace(a - pad, b + pad, 500)\n"
            "    ax.plot(xs, f(xs), color=BLUE, lw=2.4, label='$f(x)$', zorder=2)\n"
            "    # Secant through the endpoints (the average slope).\n"
            "    ax.plot([a, b], [f(a), f(b)], color=GRAY, lw=2.2, marker='o',\n"
            "            markersize=6, label=f'secant  (slope {slope:+.3f})',\n"
            "            zorder=3)\n"
            "    # Tangent at c, parallel to the secant.\n"
            "    xt = np.linspace(a - pad, b + pad, 2)\n"
            "    ax.plot(xt, f(c) + slope * (xt - c), color=RED, lw=2.2, ls='--',\n"
            "            label=f\"tangent at c  (f'(c) {fp(c):+.3f})\", zorder=4)\n"
            "    ax.scatter([c], [f(c)], s=80, color=RED, zorder=6)\n"
            "    # Mark c on the x-axis.\n"
            "    ax.axvline(c, color=RED, lw=1.0, ls=':')\n"
            "    ax.annotate('$c$', xy=(c, f(c)), xytext=(c, f(c)),\n"
            "                color=RED, fontsize=13, ha='center')\n"
            "    ax.set_xlabel('$x$'); ax.set_ylabel('$y$')\n"
            "    ax.set_title(f'MVT on [{a:.2f}, {b:.2f}]:  c \\u2248 {c:.3f}, '\n"
            "                 f'slopes match', color=DARK)\n"
            "    ax.legend(loc='best', framealpha=0.9, fontsize=10)\n"
            "    plt.show()\n"
            "\n"
            "interact(_mvt,\n"
            "         curve=Dropdown(options=list(_CURVES1), description='curve'),\n"
            "         a=FloatSlider(value=-1.0, min=-3.0, max=1.5, step=0.1,\n"
            "                       description='a'),\n"
            "         b=FloatSlider(value=1.5, min=-0.5, max=3.0, step=0.1,\n"
            "                       description='b'));\n"
        ),

        # ---------------------------------------------------------------
        # Widget 2 — Slope sign -> shape (Consequence 2)
        # ---------------------------------------------------------------
        nbb.md(
            "## 2. Slope sign $\\to$ shape\n\n"
            "**Consequence 2 of the MVT.** Where $f'>0$, the function is "
            "*rising*; where $f'<0$, it is *falling*. The turning points — "
            "where $f$ swaps one for the other — are exactly the places "
            "$f'=0$.\n\n"
            "Pick a curve. It is painted **green** on the rising stretches and "
            "**red** on the falling ones, with the turning points $f'=0$ marked. "
            "This is the whole method of Chapter 8 in a single glance: to find a "
            "function's peaks and valleys, watch where its derivative changes "
            "sign."
        ),
        nbb.code(
            "_CURVES2 = {\n"
            "    'f(x) = x^3 - 3x':       (lambda x: x**3 - 3*x,\n"
            "                              lambda x: 3*x**2 - 3),\n"
            "    'f(x) = x^4 - 2x^2':     (lambda x: x**4 - 2*x**2,\n"
            "                              lambda x: 4*x**3 - 4*x),\n"
            "    'f(x) = sin(x)':         (lambda x: np.sin(x),\n"
            "                              lambda x: np.cos(x)),\n"
            "    'f(x) = x^2':            (lambda x: x**2,\n"
            "                              lambda x: 2*x),\n"
            "}\n"
            "_RANGES2 = {\n"
            "    'f(x) = x^3 - 3x':   (-2.4, 2.4),\n"
            "    'f(x) = x^4 - 2x^2': (-1.8, 1.8),\n"
            "    'f(x) = sin(x)':     (-2*np.pi, 2*np.pi),\n"
            "    'f(x) = x^2':        (-2.5, 2.5),\n"
            "}\n"
            "\n"
            "def _shape(curve='f(x) = x^3 - 3x'):\n"
            "    f, fp = _CURVES2[curve]\n"
            "    lo, hi = _RANGES2[curve]\n"
            "    xs = np.linspace(lo, hi, 1200)\n"
            "    ys, dy = f(xs), fp(xs)\n"
            "\n"
            "    fig, ax = plt.subplots()\n"
            "    # Color each tiny segment by the sign of f' there.\n"
            "    rising = dy > 0\n"
            "    seg = np.diff(rising.astype(int)) != 0   # sign-change boundaries\n"
            "    cuts = [0] + list(np.where(seg)[0] + 1) + [len(xs)]\n"
            "    lab_up = lab_dn = True\n"
            "    for i in range(len(cuts) - 1):\n"
            "        s, e = cuts[i], cuts[i + 1]\n"
            "        if e - s < 2:\n"
            "            continue\n"
            "        up = rising[s]\n"
            "        col = GREEN if up else RED\n"
            "        lab = None\n"
            "        if up and lab_up:\n"
            "            lab, lab_up = \"rising  (f' > 0)\", False\n"
            "        elif (not up) and lab_dn:\n"
            "            lab, lab_dn = \"falling  (f' < 0)\", False\n"
            "        ax.plot(xs[s:e+1], ys[s:e+1], color=col, lw=3.0, label=lab,\n"
            "                zorder=2)\n"
            "    # Turning points: where f' = 0 (a sign change of f').\n"
            "    tp = np.where(seg)[0]\n"
            "    if tp.size:\n"
            "        xc = 0.5 * (xs[tp] + xs[tp + 1])\n"
            "        ax.scatter(xc, f(xc), s=90, facecolors='white',\n"
            "                   edgecolors=DARK, linewidths=2.0, zorder=6,\n"
            "                   label=\"turning point  (f' = 0)\")\n"
            "    ax.axhline(0, color=GRAY, lw=0.8, ls=':')\n"
            "    ax.set_xlim(lo, hi)\n"
            "    ax.set_xlabel('$x$'); ax.set_ylabel('$y$')\n"
            "    ax.set_title('Green where it rises, red where it falls', color=DARK)\n"
            "    ax.legend(loc='best', framealpha=0.9, fontsize=10)\n"
            "    plt.show()\n"
            "\n"
            "interact(_shape,\n"
            "         curve=Dropdown(options=list(_CURVES2), description='curve'));\n"
        ),

        nbb.md(
            "---\n\n"
            "*Both pictures are the same theorem read two ways. The first is the "
            "MVT itself — average slope, achieved exactly at an interior point. "
            "The second is its most-used consequence — the sign of $f'$ is the "
            "leash on $f$. Carry the second into Chapter 8, where finding maxima "
            "and minima is nothing but tracking where that color changes.*"
        ),
    ]
    nbb.build("ch6_mvt.ipynb", cells)


if __name__ == "__main__":
    build()
