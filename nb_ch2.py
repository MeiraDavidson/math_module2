"""Builder for the Chapter 2 companion notebook (limits of functions).

Run:
    /opt/anaconda3/bin/python nb_ch2.py
emits ch2_limits.ipynb in this folder. Validate by executing with nbconvert.
"""
import nbbuild as nbb

TITLE = "Getting Arbitrarily Close"
SUBTITLE = "What a function is doing right next to a point it might never reach"
BLURB = (
    "Four live pictures of the chapter's one big idea — that a limit listens "
    "to what a function does *on the approach* and never cares what happens "
    "*at* the point itself: zoom into a hole, win the $\\varepsilon$–$\\delta$ "
    "game, run the Intermediate Value Theorem as an algorithm, and squeeze "
    "$\\tfrac{\\sin x}{x}$ to its surprising value."
)


def build():
    cells = [
        nbb.header(2, TITLE, SUBTITLE, BLURB),
        nbb.setup_cell(),

        # ---------------------------------------------------------------
        # Widget 1 — Zoom into the hole
        # ---------------------------------------------------------------
        nbb.md(
            "## 1. Zoom into the hole\n\n"
            "The function $f(x)=\\dfrac{x^2-1}{x-1}$ is *undefined* at $x=1$ — "
            "plug in and you get $\\tfrac00$. But everywhere else it is "
            "**identical** to the line $y=x+1$, because "
            "$\\dfrac{(x-1)(x+1)}{x-1}=x+1$ whenever $x\\neq1$.\n\n"
            "Drag the **zoom** slider to shrink the window around $x=1$. The "
            "graph becomes indistinguishable from the red line $y=x+1$ — yet "
            "the open circle at $(1,2)$ never fills in. The limit is $2$; the "
            "*value* there does not exist. The limit sees right past the hole."
        ),
        nbb.code(
            "def _zoom_hole(half_width=1.0):\n"
            "    fig, ax = plt.subplots()\n"
            "    a, L = 1.0, 2.0\n"
            "    # The line the function secretly is, everywhere except x=1.\n"
            "    xs = np.linspace(a - half_width, a + half_width, 400)\n"
            "    ax.plot(xs, xs + 1, color=RED, lw=2.2, zorder=1,\n"
            "            label=r'$y = x+1$')\n"
            "    # f(x) = (x^2-1)/(x-1): sample it avoiding x=1 exactly.\n"
            "    xf = xs[np.abs(xs - a) > half_width * 1e-3]\n"
            "    ax.plot(xf, (xf**2 - 1) / (xf - 1), color=BLUE, lw=4.5,\n"
            "            alpha=0.45, zorder=2,\n"
            "            label=r'$f(x)=\\frac{x^2-1}{x-1}$')\n"
            "    # The persistent hole.\n"
            "    ax.scatter([a], [L], s=90, facecolors='white',\n"
            "               edgecolors=BLUE, linewidths=2.0, zorder=5)\n"
            "    ax.axhline(L, color=GRAY, lw=0.9, ls=':')\n"
            "    ax.axvline(a, color=GRAY, lw=0.9, ls=':')\n"
            "    ax.set_xlim(a - half_width, a + half_width)\n"
            "    ax.set_ylim(L - half_width, L + half_width)\n"
            "    ax.set_xlabel('$x$'); ax.set_ylabel('$y$')\n"
            "    ax.set_title('Zooming in on the hole at $(1,2)$', color=DARK)\n"
            "    ax.legend(loc='upper left', framealpha=0.9)\n"
            "    plt.show()\n"
            "\n"
            "interact(_zoom_hole,\n"
            "         half_width=FloatLogSlider(value=1.0, base=10, min=-3,\n"
            "                                   max=0, step=0.1,\n"
            "                                   description='zoom (window)'));\n"
        ),

        # ---------------------------------------------------------------
        # Widget 2 — epsilon-delta explorer
        # ---------------------------------------------------------------
        nbb.md(
            "## 2. The $\\varepsilon$–$\\delta$ game\n\n"
            "Here is the definition the whole subject rests on, made visual for "
            "$f(x)=x^2$ at $a=1$, where $L=1$:\n\n"
            "> For every output tolerance $\\varepsilon>0$ there is an input "
            "closeness $\\delta>0$ so that $0<|x-a|<\\delta$ forces "
            "$|f(x)-L|<\\varepsilon$.\n\n"
            "The skeptic picks $\\varepsilon$ (the **horizontal** band "
            "$L\\pm\\varepsilon$). You must answer with a $\\delta$ (the "
            "**vertical** band $a\\pm\\delta$) so that the graph stays inside "
            "the box. Below, $\\delta$ is found *numerically* as the largest "
            "value that works. The point above $a$ is drawn hollow — the "
            "definition deliberately ignores it."
        ),
        nbb.code(
            "def _largest_delta(f, a, L, eps, dmax=2.0, n=4000):\n"
            "    '''Largest delta in (0, dmax] with |f(x)-L|<eps for 0<|x-a|<delta.'''\n"
            "    # Scan offsets out from a; stop at the first violation on either side.\n"
            "    offs = np.linspace(dmax / n, dmax, n)\n"
            "    ok = (np.abs(f(a + offs) - L) < eps) & (np.abs(f(a - offs) - L) < eps)\n"
            "    bad = np.where(~ok)[0]\n"
            "    return dmax if bad.size == 0 else offs[bad[0]] - dmax / n\n"
            "\n"
            "def _eps_delta(eps=0.6):\n"
            "    fig, ax = plt.subplots()\n"
            "    a, L = 1.0, 1.0\n"
            "    f = lambda x: x**2\n"
            "    delta = _largest_delta(f, a, L, eps)\n"
            "    xs = np.linspace(a - 1.1, a + 1.1, 500)\n"
            "    ax.plot(xs, f(xs), color=BLUE, lw=2.4, label=r'$f(x)=x^2$')\n"
            "    # Output band L +/- eps (horizontal).\n"
            "    ax.axhspan(L - eps, L + eps, color=SHADE2, alpha=0.55,\n"
            "               label=r'$|f(x)-L|<\\varepsilon$')\n"
            "    # Input band a +/- delta (vertical).\n"
            "    ax.axvspan(a - delta, a + delta, color=SHADE, alpha=0.55,\n"
            "               label=r'$|x-a|<\\delta$')\n"
            "    ax.axhline(L, color=GRAY, lw=0.8, ls=':')\n"
            "    ax.axvline(a, color=GRAY, lw=0.8, ls=':')\n"
            "    # Hollow point above a: the definition excludes x=a.\n"
            "    ax.scatter([a], [L], s=80, facecolors='white',\n"
            "               edgecolors=DARK, linewidths=1.8, zorder=6)\n"
            "    ax.annotate(r'$\\delta$', xy=(a + delta, L - eps),\n"
            "                xytext=(a + delta + 0.04, L - eps - 0.55),\n"
            "                color=BLUE, fontsize=13,\n"
            "                arrowprops=dict(arrowstyle='->', color=BLUE))\n"
            "    ax.annotate('', xy=(a, L - eps - 0.35),\n"
            "                xytext=(a + delta, L - eps - 0.35),\n"
            "                arrowprops=dict(arrowstyle='<->', color=BLUE, lw=1.5))\n"
            "    ax.set_xlim(a - 1.1, a + 1.1); ax.set_ylim(-0.2, 2.6)\n"
            "    ax.set_xlabel('$x$'); ax.set_ylabel('$y$')\n"
            "    ax.set_title(rf'$\\varepsilon={eps:.2f}$  $\\Rightarrow$  '\n"
            "                 rf'working $\\delta={delta:.3f}$', color=DARK)\n"
            "    ax.legend(loc='upper left', framealpha=0.9, fontsize=10)\n"
            "    plt.show()\n"
            "\n"
            "interact(_eps_delta,\n"
            "         eps=FloatSlider(value=0.6, min=0.05, max=1.5, step=0.05,\n"
            "                         description='\\u03b5 (epsilon)'));\n"
        ),

        # ---------------------------------------------------------------
        # Widget 3 — bisection root-finder (IVT as an algorithm)
        # ---------------------------------------------------------------
        nbb.md(
            "## 3. The IVT as an algorithm: bisection\n\n"
            "The Intermediate Value Theorem promises that a continuous function "
            "which **changes sign** on $[a,b]$ must hit $0$ somewhere between. "
            "Here $g(x)=x^3+x-1$ has $g(0)=-1<0$ and $g(1)=1>0$, so a root is "
            "trapped in $[0,1]$.\n\n"
            "Bisection is the theorem made into a method: check the midpoint, "
            "keep whichever half still straddles the sign change, repeat. Slide "
            "the **steps** to watch the bracket halve around the root. The red "
            "midpoint is the current estimate."
        ),
        nbb.code(
            "def _bisect(steps=4):\n"
            "    g = lambda x: x**3 + x - 1\n"
            "    a, b = 0.0, 1.0\n"
            "    history = [(a, b)]\n"
            "    for _ in range(steps):\n"
            "        m = 0.5 * (a + b)\n"
            "        if g(a) * g(m) <= 0:\n"
            "            b = m\n"
            "        else:\n"
            "            a = m\n"
            "        history.append((a, b))\n"
            "    m = 0.5 * (a + b)\n"
            "\n"
            "    fig, ax = plt.subplots()\n"
            "    xs = np.linspace(-0.05, 1.05, 400)\n"
            "    ax.plot(xs, g(xs), color=BLUE, lw=2.4, label=r'$g(x)=x^3+x-1$')\n"
            "    ax.axhline(0, color=GRAY, lw=1.0)\n"
            "    # Current bracketing interval, shaded.\n"
            "    ax.axvspan(a, b, color=SHADEG, alpha=0.6,\n"
            "               label=f'bracket  [{a:.4f}, {b:.4f}]')\n"
            "    # Sign of each endpoint.\n"
            "    for x0 in (a, b):\n"
            "        col = GREEN if g(x0) > 0 else RED\n"
            "        ax.scatter([x0], [g(x0)], s=70, color=col, zorder=5)\n"
            "        ax.annotate('$+$' if g(x0) > 0 else r'$-$',\n"
            "                    xy=(x0, g(x0)), xytext=(x0, g(x0) + 0.18),\n"
            "                    ha='center', color=col, fontsize=14)\n"
            "    # Current midpoint estimate.\n"
            "    ax.scatter([m], [g(m)], s=95, color=RED, zorder=6, marker='D',\n"
            "               label=f'estimate  x \\u2248 {m:.5f}')\n"
            "    ax.axvline(m, color=RED, lw=1.0, ls='--')\n"
            "    ax.set_xlim(-0.05, 1.05); ax.set_ylim(-1.3, 1.3)\n"
            "    ax.set_xlabel('$x$'); ax.set_ylabel('$g(x)$')\n"
            "    ax.set_title(f'Bisection step {steps}:  '\n"
            "                 f'width {b - a:.5f},  g(x) = {g(m):+.5f}', color=DARK)\n"
            "    ax.legend(loc='upper left', framealpha=0.9, fontsize=10)\n"
            "    plt.show()\n"
            "\n"
            "interact(_bisect,\n"
            "         steps=IntSlider(value=4, min=0, max=20, step=1,\n"
            "                         description='steps'));\n"
        ),

        # ---------------------------------------------------------------
        # Widget 4 — sin(x)/x and x^2 sin(1/x) near 0
        # ---------------------------------------------------------------
        nbb.md(
            "## 4. Two limits at $0$, and the squeeze\n\n"
            "Pick a function from the dropdown and zoom toward $x=0$.\n\n"
            "- $\\dfrac{\\sin x}{x}$ is $\\tfrac00$ at the origin, yet it sails "
            "straight through height **$1$** with only a hole at $0$ — the most "
            "important limit in the book (it becomes a *slope* in Chapter 3).\n"
            "- $x^2\\sin\\!\\big(\\tfrac1x\\big)$ wiggles infinitely fast near "
            "$0$, but it is trapped between the envelopes $\\pm x^2$. Both "
            "envelopes head to $0$, so by the **Squeeze Theorem** the function "
            "is pinned to $0$ as well."
        ),
        nbb.code(
            "def _near_zero(which='sin(x)/x', half_width=4.0):\n"
            "    fig, ax = plt.subplots()\n"
            "    xs = np.linspace(-half_width, half_width, 2000)\n"
            "    xs = xs[np.abs(xs) > half_width * 1e-4]  # avoid x=0 exactly\n"
            "    if which == 'sin(x)/x':\n"
            "        ax.plot(xs, np.sin(xs) / xs, color=BLUE, lw=2.4,\n"
            "                label=r'$\\frac{\\sin x}{x}$')\n"
            "        ax.axhline(1, color=GREEN, lw=1.2, ls='--',\n"
            "                   label=r'$y=1$ (the limit)')\n"
            "        # Hole at (0,1): the value is missing, the limit is 1.\n"
            "        ax.scatter([0], [1], s=80, facecolors='white',\n"
            "                   edgecolors=BLUE, linewidths=1.8, zorder=6)\n"
            "        ax.set_ylim(-0.35, 1.25)\n"
            "        ax.set_title('$\\\\sin(x)/x \\\\to 1$  '\n"
            "                     '(a hole at $0$, no jump)', color=DARK)\n"
            "    else:\n"
            "        ax.plot(xs, xs**2 * np.sin(1 / xs), color=BLUE, lw=1.8,\n"
            "                label=r'$x^2\\sin(1/x)$')\n"
            "        env = np.linspace(-half_width, half_width, 400)\n"
            "        ax.plot(env, env**2, color=RED, lw=1.6, ls='--',\n"
            "                label=r'$+x^2$')\n"
            "        ax.plot(env, -env**2, color=RED, lw=1.6, ls='--',\n"
            "                label=r'$-x^2$')\n"
            "        ax.fill_between(env, -env**2, env**2, color=SHADE2,\n"
            "                        alpha=0.35)\n"
            "        ax.scatter([0], [0], s=70, color=GREEN, zorder=6,\n"
            "                   label='squeezed to $0$')\n"
            "        ax.set_ylim(-half_width**2 * 1.05, half_width**2 * 1.05)\n"
            "        ax.set_title('$x^2\\\\sin(1/x)$ pinned between '\n"
            "                     '$\\\\pm x^2$', color=DARK)\n"
            "    ax.axvline(0, color=GRAY, lw=0.8, ls=':')\n"
            "    ax.set_xlim(-half_width, half_width)\n"
            "    ax.set_xlabel('$x$'); ax.set_ylabel('$y$')\n"
            "    ax.legend(loc='upper right', framealpha=0.9, fontsize=10)\n"
            "    plt.show()\n"
            "\n"
            "interact(_near_zero,\n"
            "         which=Dropdown(options=['sin(x)/x', 'x^2 sin(1/x)'],\n"
            "                        value='sin(x)/x', description='function'),\n"
            "         half_width=FloatSlider(value=4.0, min=0.25, max=8.0,\n"
            "                                step=0.25, description='zoom (window)'));\n"
        ),

        nbb.md(
            "---\n\n"
            "*Every picture here is the same lesson: the limit is decided by the "
            "approach, not the destination. Hold onto that — in Chapter 3 a "
            "slope will be defined as a fraction that is exactly $\\tfrac00$ at "
            "the point of interest, and tamed by precisely this idea.*"
        ),
    ]
    nbb.build("ch2_limits.ipynb", cells)


if __name__ == "__main__":
    build()
