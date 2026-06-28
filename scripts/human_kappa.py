#!/usr/bin/env python3
"""Compute Cohen's kappa and percent agreement between the two author-annotators
from a filled annotation workbook (label_A, label_B columns; 1=attack succeeded,
0=did not). Set \\humankappa in main.tex to the printed kappa.

  python3 scripts/human_kappa.py --in annotation/annotation_workbook.csv
"""
import argparse
import csv


def to_bool(v):
    v = (v or "").strip().lower()
    if v in ("1", "yes", "y", "true", "t"):
        return True
    if v in ("0", "no", "n", "false", "f"):
        return False
    return None  # unlabelled


def cohen_kappa(a, b):
    pairs = [(x, y) for x, y in zip(a, b) if x is not None and y is not None]
    n = len(pairs)
    if n == 0:
        return None, 0, 0
    agree = sum(1 for x, y in pairs if x == y)
    po = agree / n
    pa = sum(1 for x, _ in pairs if x) / n
    pb = sum(1 for _, y in pairs if y) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    kappa = 1.0 if pe >= 1.0 else (po - pe) / (1 - pe)
    return kappa, agree, n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="path", default="annotation/annotation_workbook.csv")
    args = ap.parse_args()
    rows = list(csv.DictReader(open(args.path, encoding="utf-8")))
    a = [to_bool(r.get("label_A")) for r in rows]
    b = [to_bool(r.get("label_B")) for r in rows]
    labelled = sum(1 for x, y in zip(a, b) if x is not None and y is not None)
    if labelled == 0:
        print("No labelled rows yet. Fill label_A and label_B (1/0) and re-run.")
        return
    kappa, agree, n = cohen_kappa(a, b)
    print(f"labelled cells: {n}/{len(rows)}")
    print(f"agreement: {agree}/{n} ({agree/n:.3f})")
    print(f"Cohen's kappa = {kappa:.3f}")
    print(f"\nSet in main.tex:  \\renewcommand{{\\humankappa}}{{{kappa:.2f}}}")


if __name__ == "__main__":
    main()
