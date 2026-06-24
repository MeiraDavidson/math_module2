"""Builder for the Chapter 5 companion notebook (exponentials & logarithms).

    cd notebooks && python3 nb_ch5.py

Emits notebooks/ch5_exponentials.ipynb. The notebook is self-contained: its
first cell (nbb.setup_cell()) imports numpy/matplotlib/ipywidgets/IPython and
the Book 2 palette, so the widget cells below assume np, plt, animation, the
ipywidgets factories, HTML/display/Markdown, the colour constants, and axes().

Chapter theme: e is the base whose curve's slope equals its height, and the
mystery constant M(a) = ln a is the slope of a^x as it crosses the y-axis.
"""
import nbbuild as nbb

TITLE = "The Function That Is Its Own Slope"
SUBTITLE = "Why one strange number between 2 and 3 refuses to change"
BLURB = (
    "Three live experiments on the number $e$. You will drag a base $a$ and "
    "watch the curve $y=a^x$ tilt away from the $y$-axis until its crossing "
    "slope $M(a)=\\ln a$ hits exactly $1$ — that base *is* $e$. Then you will "
    "see what \"its own derivative\" looks like, where the steepness of "
    "$y=e^x$ equals its height at every point. Finally you will run a decay "
    "simulator and watch a quantity halve, then halve again, at evenly spaced "
    "half-lives."
)


def build():
    cells = [
        nbb.header(5, TITLE, SUBTITLE, BLURB),
        nbb.setup_cell(),

        # ---- Widget 1: base-a slider, M(a) = ln a -------------------------
        nbb.md(
            "## 1. Hunting for the base that leaves the axis at slope 1\n\n"
            "Take any exponential $y=a^x$ and differentiate it from scratch. "
            "The $a^x$ factors straight out of the difference quotient and "
            "*never changes as $h$ shrinks*, leaving one lonely number behind:\n\n"
            "$$\\frac{d}{dx}\\,a^{x} = M(a)\\,a^{x},\\qquad "
            "M(a)=\\lim_{h\\to 0}\\frac{a^{h}-1}{h}.$$\n\n"
            "Every exponential is *already* proportional to its own slope — "
            "off only by that constant $M(a)$. And $M(a)$ has a picture: plug "
            "in $x=0$ and, since $a^0=1$, the slope of $y=a^x$ right where it "
            "**crosses the $y$-axis** is exactly $M(a)$.\n\n"
            "So our whole quest reduces to one question: *for which base does "
            "the curve leave the axis at slope exactly $1$?* Drag $a$ below. "
            "The blue curve is $y=a^x$; the red line is its tangent at the "
            "crossing point $(0,1)$, and its slope is the live number "
            "$M(a)=\\ln a$. Push $a$ until that slope reads $1$ — you will be "
            "sitting on $a=e\\approx 2.718$, the base whose curve refuses to "
            "leave the axis at any slope but one."
        ),
        nbb.code(
            "E = np.e  # 2.71828..., the base we are hunting for\n"
            "\n"
            "def _base_slope(a=2.0, show_family=True):\n"
            "    # M(a) = ln a is the slope of a^x at x=0 (the y-axis crossing).\n"
            "    M = np.log(a)\n"
            "    x = np.linspace(-2.2, 2.2, 400)\n"
            "\n"
            "    fig, ax = plt.subplots()\n"
            "    axes(ax)\n"
            "\n"
            "    # Faint family of other bases, for context.\n"
            "    if show_family:\n"
            "        for b in (1.5, 2.0, E, 3.0, 4.0):\n"
            "            ax.plot(x, b ** x, color=GRAY, lw=1.1, alpha=0.30, zorder=1)\n"
            "\n"
            "    # The chosen curve y = a^x.\n"
            "    ax.plot(x, a ** x, color=BLUE, lw=2.6, zorder=3,\n"
            "            label=f'$y = a^x$,  $a={a:.3f}$')\n"
            "\n"
            "    # Tangent at the y-axis crossing (0, 1): slope = M(a) = ln a.\n"
            "    xt = np.linspace(-1.4, 1.4, 2)\n"
            "    ax.plot(xt, 1.0 + M * xt, color=RED, lw=2.2, ls='--', zorder=4,\n"
            "            label=f'tangent at $(0,1)$, slope $= \\\\ln a = {M:.3f}$')\n"
            "    ax.scatter([0], [1], s=46, color=RED, zorder=5)\n"
            "\n"
            "    # Live verdict on whether we have found e.\n"
            "    if abs(M - 1.0) < 0.01:\n"
            "        verdict = (f'$M(a) = {M:.3f} \\\\approx 1$  \\u2014  '\n"
            "                   f'this is $e \\\\approx {E:.3f}$!')\n"
            "        vcolor = GREEN\n"
            "    elif M < 1.0:\n"
            "        verdict = f'$M(a) = {M:.3f} < 1$  \\u2014  too gentle, push $a$ up'\n"
            "        vcolor = DARK\n"
            "    else:\n"
            "        verdict = f'$M(a) = {M:.3f} > 1$  \\u2014  too steep, ease $a$ down'\n"
            "        vcolor = DARK\n"
            "    ax.set_title(verdict, color=vcolor, fontsize=13)\n"
            "\n"
            "    ax.axhline(0, color=DARK, lw=0.8)\n"
            "    ax.axvline(0, color=DARK, lw=0.8)\n"
            "    ax.set_xlim(-2.2, 2.2)\n"
            "    ax.set_ylim(-0.5, 8)\n"
            "    ax.set_xlabel('$x$'); ax.set_ylabel('$y$')\n"
            "    ax.legend(loc='upper left', framealpha=0.92)\n"
            "    plt.show()\n"
            "\n"
            "interact(_base_slope,\n"
            "         a=FloatSlider(value=2.0, min=1.2, max=4.0, step=0.01,\n"
            "                       description='base $a$', readout_format='.2f',\n"
            "                       continuous_update=False),\n"
            "         show_family=Checkbox(value=True, description='show other bases'));"
        ),

        # ---- Widget 2: slope equals height for e^x ------------------------
        nbb.md(
            "## 2. \"Its own derivative\" — slope equals height\n\n"
            "Setting $M(e)=1$ collapses the boxed rule to the headline of the "
            "whole chapter:\n\n"
            "$$\\frac{d}{dx}\\,e^{x} = e^{x}.$$\n\n"
            "That equation is a *geometric promise*: at any point $x_0$ the "
            "tangent to $y=e^x$ has slope $e^{x_0}$, which is the very height "
            "of the curve there. Where the curve sits at height $5$, it climbs "
            "at slope $5$. Slide $x_0$ along the curve and watch the green "
            "height and the red slope stay locked to the same number — the "
            "shaded triangle has rise equal to its run scaled by exactly that "
            "value."
        ),
        nbb.code(
            "def _slope_equals_height(x0=0.6):\n"
            "    x = np.linspace(-2.5, 2.0, 400)\n"
            "    y = np.exp(x)\n"
            "    h = np.exp(x0)          # height = slope, the whole point\n"
            "\n"
            "    fig, ax = plt.subplots()\n"
            "    axes(ax, '$y=e^x$:  slope at $x_0$ equals the height $e^{x_0}$')\n"
            "    ax.plot(x, y, color=BLUE, lw=2.6, zorder=3, label='$y = e^x$')\n"
            "\n"
            "    # Tangent line through (x0, h) with slope h.\n"
            "    xt = np.linspace(x0 - 1.3, x0 + 1.3, 2)\n"
            "    ax.plot(xt, h + h * (xt - x0), color=RED, lw=2.2, ls='--',\n"
            "            zorder=4, label=f'tangent, slope $= {h:.3f}$')\n"
            "\n"
            "    # Drop line showing the height, and a rise/run slope triangle.\n"
            "    ax.vlines(x0, 0, h, color=GREEN, lw=2.0, zorder=2)\n"
            "    ax.plot([x0, x0 + 1], [h, h], color=GRAY, lw=1.4, zorder=2)\n"
            "    ax.plot([x0 + 1, x0 + 1], [h, h + h], color=GRAY, lw=1.4, zorder=2)\n"
            "    ax.fill([x0, x0 + 1, x0 + 1], [h, h, h + h],\n"
            "            color=SHADE2, alpha=0.55, zorder=1)\n"
            "    ax.annotate(f'run $=1$', xy=(x0 + 0.5, h), xytext=(x0 + 0.5, h - 0.9),\n"
            "                ha='center', color=GRAY, fontsize=11)\n"
            "    ax.annotate(f'rise $= {h:.2f}$', xy=(x0 + 1, h + h / 2),\n"
            "                xytext=(x0 + 1.1, h + h / 2), va='center',\n"
            "                color=DARK, fontsize=11)\n"
            "\n"
            "    ax.scatter([x0], [h], s=46, color=RED, zorder=5)\n"
            "    ax.annotate(f'height $= e^{{{x0:.2f}}} = {h:.3f}$',\n"
            "                xy=(x0, h), xytext=(x0 - 2.3, h + 0.6),\n"
            "                color=GREEN, fontsize=12,\n"
            "                arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.4))\n"
            "\n"
            "    ax.axhline(0, color=DARK, lw=0.8)\n"
            "    ax.axvline(0, color=DARK, lw=0.8)\n"
            "    ax.set_xlim(-2.5, 2.0)\n"
            "    ax.set_ylim(-0.6, 8)\n"
            "    ax.set_xlabel('$x$'); ax.set_ylabel('$y$')\n"
            "    ax.legend(loc='upper left', framealpha=0.92)\n"
            "    plt.show()\n"
            "\n"
            "interact(_slope_equals_height,\n"
            "         x0=FloatSlider(value=0.6, min=-2.0, max=1.9, step=0.01,\n"
            "                        description='point $x_0$', readout_format='.2f',\n"
            "                        continuous_update=False));"
        ),

        # ---- Widget 3: decay simulator with half-lives --------------------
        nbb.md(
            "## 3. Decay and half-life\n\n"
            "Flip the sign of the rate constant and the same function *decays*. "
            "Written in terms of its **half-life** $T$ — the time for the "
            "amount to fall to half of whatever it was — the model is\n\n"
            "$$N(t) = N_{0}\\left(\\tfrac12\\right)^{t/T} = N_0\\,e^{-\\lambda t},"
            "\\qquad \\lambda = \\frac{\\ln 2}{T}.$$\n\n"
            "The defining feature of exponential decay is that this halving is "
            "*memoryless*: it takes one half-life $T$ to go from $N_0$ to "
            "$N_0/2$, another $T$ to reach $N_0/4$, another to reach $N_0/8$ — "
            "no matter where you start counting. Drag the half-life $T$ (and "
            "the starting amount $N_0$). The dashed guides mark $t=T,2T,3T,4T$; "
            "at each one the quantity is exactly halved from the step before, "
            "and the labels read off the value."
        ),
        nbb.code(
            "def _decay(T=2.0, N0=400.0, n_halves=4):\n"
            "    t = np.linspace(0, n_halves * T * 1.05, 400)\n"
            "    N = N0 * 0.5 ** (t / T)\n"
            "\n"
            "    fig, ax = plt.subplots()\n"
            "    lam = np.log(2) / T\n"
            "    axes(ax, f'$N(t)=N_0(1/2)^{{t/T}}$,  half-life $T={T:.2f}$,  '\n"
            "             f'$\\\\lambda=\\\\ln 2/T={lam:.3f}$')\n"
            "    ax.fill_between(t, 0, N, color=SHADE, alpha=0.35, zorder=0)\n"
            "    ax.plot(t, N, color=BLUE, lw=2.6, zorder=3, label='$N(t)$')\n"
            "\n"
            "    # Mark successive half-lives t = T, 2T, 3T, ... with guides.\n"
            "    for k in range(0, n_halves + 1):\n"
            "        tk = k * T\n"
            "        Nk = N0 * 0.5 ** k     # = N0 / 2^k\n"
            "        # vertical guide up to the curve, horizontal guide to the axis\n"
            "        ax.vlines(tk, 0, Nk, color=RED, lw=1.3, ls='--', zorder=2)\n"
            "        ax.hlines(Nk, 0, tk, color=GREEN, lw=1.3, ls=':', zorder=2)\n"
            "        ax.scatter([tk], [Nk], s=40, color=RED, zorder=4)\n"
            "        label = f'{Nk:.4g}' if k else f'$N_0={Nk:.4g}$'\n"
            "        ax.annotate(label, xy=(tk, Nk), xytext=(tk + 0.12 * T, Nk + 0.04 * N0),\n"
            "                    color=DARK, fontsize=11)\n"
            "        if k:\n"
            "            ax.annotate(f'${k}T$', xy=(tk, 0), xytext=(tk, -0.07 * N0),\n"
            "                        ha='center', color=RED, fontsize=11)\n"
            "\n"
            "    ax.set_xlim(0, n_halves * T * 1.05)\n"
            "    ax.set_ylim(-0.1 * N0, 1.12 * N0)\n"
            "    ax.set_xlabel('time $t$'); ax.set_ylabel('amount $N$')\n"
            "    ax.legend(loc='upper right', framealpha=0.92)\n"
            "    plt.show()\n"
            "\n"
            "interact(_decay,\n"
            "         T=FloatSlider(value=2.0, min=0.5, max=5.0, step=0.1,\n"
            "                       description='half-life $T$', readout_format='.1f',\n"
            "                       continuous_update=False),\n"
            "         N0=FloatSlider(value=400.0, min=50.0, max=1000.0, step=50.0,\n"
            "                        description='start $N_0$', readout_format='.0f',\n"
            "                        continuous_update=False),\n"
            "         n_halves=IntSlider(value=4, min=2, max=6, step=1,\n"
            "                            description='# half-lives'));"
        ),

        nbb.md(
            "---\n\n"
            "*Three pictures, one idea.* The first widget shows that picking "
            "the base is the same as picking a crossing slope $M(a)=\\ln a$, "
            "and $e$ is the unique base that picks slope $1$. The second shows "
            "the payoff — at $a=e$ the curve's height *is* its slope "
            "everywhere. The third turns the same exponential, run with a "
            "negative rate, into the half-life arithmetic you can now derive "
            "rather than memorize: $t_{1/2} = \\ln 2/\\lambda$."
        ),
    ]
    nbb.build("ch5_exponentials.ipynb", cells)


if __name__ == "__main__":
    build()
