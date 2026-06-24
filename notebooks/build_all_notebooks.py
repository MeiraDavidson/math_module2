"""Regenerate all 12 companion notebooks from their builder scripts.

    cd notebooks && python3 build_all_notebooks.py

Each nb_chN.py defines build(); this driver runs them all and checks that the
12 .ipynb files exist.
"""
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

FILES = {
    1:  "ch1_sequences.ipynb",
    2:  "ch2_limits.ipynb",
    3:  "ch3_derivative.ipynb",
    4:  "ch4_rules.ipynb",
    5:  "ch5_exponentials.ipynb",
    6:  "ch6_mvt.ipynb",
    7:  "ch7_taylor.ipynb",
    8:  "ch8_convexity.ipynb",
    9:  "ch9_newton_gradient_descent.ipynb",
    10: "ch10_integral.ipynb",
    11: "ch11_fundamental_theorem.ipynb",
    12: "ch12_series.ipynb",
}


def main():
    for c in range(1, 13):
        importlib.import_module(f"nb_ch{c}").build()
    missing = [f for f in FILES.values()
               if not os.path.exists(os.path.join(HERE, f))]
    if missing:
        print("MISSING:", missing)
        sys.exit(1)
    print(f"OK — all {len(FILES)} companion notebooks built into notebooks/")


if __name__ == "__main__":
    main()
