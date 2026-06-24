"""Shared builder helpers for the Book 2 companion notebooks.

Each chapter has a builder `nb_chN.py` that imports this module, assembles a
list of cells, and calls `build(...)`. The emitted `.ipynb` is fully
self-contained — the reader never needs this module. Run everything with:

    cd notebooks && python3 build_all_notebooks.py

Conventions
-----------
* First cell of every notebook is SETUP (imports + the Book 2 palette so the
  widgets match the printed figures + a clean matplotlib style).
* Use `%matplotlib inline` + ipywidgets `interact` for sliders (re-renders on
  change — works in classic Notebook, JupyterLab, and `nbconvert --execute`).
* Animations: matplotlib FuncAnimation -> HTML(ani.to_jshtml()); keep frames
  modest (<= 60) so files stay small and execute fast.
"""
import os
import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

HERE = os.path.dirname(os.path.abspath(__file__))

# The standard first code cell, shared by all 12 notebooks.
SETUP = r"""%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from ipywidgets import (interact, interactive, fixed, Dropdown, Checkbox,
                        Button, Output, VBox, HBox,
                        FloatSlider, IntSlider, FloatLogSlider)
from IPython.display import HTML, display, Markdown

# Book 2 palette — matches the printed figures in figures/png/
BLUE="#1f4e79"; RED="#c0392b"; GREEN="#2e8b57"; ORANGE="#e08e0b"
PURPLE="#6c3483"; TEAL="#1b9e9e"; GRAY="#7f8c8d"; DARK="#2c3e50"
SHADE="#9fc5e8"; SHADE2="#f4b6ad"; SHADEG="#a9dfbf"; LIGHT="#d6dbdf"

plt.rcParams.update({
    "figure.figsize": (7.2, 4.5), "figure.dpi": 96,
    "font.family": "serif", "mathtext.fontset": "cm", "font.size": 12,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": LIGHT, "grid.linewidth": 0.7,
    "lines.linewidth": 2.2, "lines.solid_capstyle": "round",
})

def axes(ax=None, title=None):
    '''A clean axes with a light grid; returns the axes.'''
    if ax is None:
        _, ax = plt.subplots()
    if title:
        ax.set_title(title, color=DARK)
    return ax
"""


def md(source):
    return new_markdown_cell(source)


def code(source):
    return new_code_cell(source)


def setup_cell():
    return new_code_cell(SETUP)


def header(chapter_no, title, subtitle, blurb):
    """Standard title markdown cell for a chapter notebook."""
    return new_markdown_cell(
        f"# Chapter {chapter_no} — Companion Notebook\n"
        f"## {title}\n"
        f"*{subtitle}*\n\n"
        f"{blurb}\n\n"
        f"> **How to use this notebook.** Run every cell from the top "
        f"(Shift+Enter). Each widget below is live — drag the sliders and "
        f"watch the picture respond. Requires `ipywidgets` and `matplotlib`."
    )


def build(filename, cells):
    """Write a notebook (list of cells) to notebooks/<filename>."""
    nb = new_notebook()
    nb.cells = list(cells)
    nb.metadata = {
        "kernelspec": {"display_name": "Python 3", "language": "python",
                       "name": "python3"},
        "language_info": {"name": "python", "pygments_lexer": "ipython3"},
    }
    path = os.path.join(HERE, filename)
    nbf.write(nb, path)
    print("wrote", os.path.relpath(path, HERE))
    return path
