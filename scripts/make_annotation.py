#!/usr/bin/env python3
"""Build a blind annotation workbook from the benchmark results so two authors can
independently label each cell as attack-success or not. The rubric's own verdict is
deliberately omitted so annotators are not anchored. Two label columns (label_A,
label_B) are left blank; each annotator fills exactly one, independently.

  python3 scripts/make_annotation.py --results ../rag-sec/results_full/results.jsonl \\
      --out annotation/annotation_workbook.csv
"""
import argparse
import csv
import json
import os


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", required=True)
    ap.add_argument("--out", default="annotation/annotation_workbook.csv")
    args = ap.parse_args()

    rows = [json.loads(l) for l in open(args.results, encoding="utf-8") if l.strip()]
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    cols = ["cell_id", "model", "scenario", "mode", "owasp", "attack_payload",
            "retrieved_ids", "model_output", "tool_results", "label_A", "label_B"]
    with open(args.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for i, r in enumerate(rows):
            w.writerow({
                "cell_id": i,
                "model": r.get("model_label", ""),
                "scenario": r.get("scenario", ""),
                "mode": r.get("mode", ""),
                "owasp": " ".join(r.get("scenario_owasp", [])),
                "attack_payload": "",  # filled below from scenarios if available
                "retrieved_ids": " ".join(r.get("retrieved_ids", [])),
                "model_output": (r.get("model_output", "") or "")[:4000],
                "tool_results": " | ".join(r.get("tool_results", [])),
                "label_A": "", "label_B": "",
            })
    print(f"wrote {args.out} with {len(rows)} cells; annotators fill label_A / label_B "
          f"as 1 (attack succeeded) or 0 (did not), independently.")


if __name__ == "__main__":
    main()
