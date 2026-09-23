#!/usr/bin/env python3
"""Check Technical Variation (TV) Traceability Matrix.

Audits TV1 through TV18 to ensure 100% resolution and zero unaddressed items.
"""
from __future__ import annotations

import json
import os
import sys

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    json_path = os.path.join(repo_root, 'paper9/audit/traceability_matrix.json')

    if not os.path.exists(json_path):
        print(f"ERROR: {json_path} does not exist!")
        sys.exit(1)

    with open(json_path) as f:
        data = json.load(f)

    tv_items = data.get("technical_variations", {})
    print("=" * 80)
    print(f"TECHNICAL VARIATION (TV) TRACEABILITY AUDIT: {len(tv_items)} ITEMS")
    print("=" * 80)

    open_items = []
    closed_items = []

    for tv_id, info in sorted(tv_items.items(), key=lambda x: int(x[0].replace("TV", "")) if x[0].replace("TV", "").isdigit() else 99):
        status = info.get("status", "UNKNOWN")
        desc = info.get("description", "")
        evidence = info.get("evidence", "")
        
        is_closed = any(kw in status for kw in ["CLOSED", "LOCKED", "RESOLVED", "DISCHARGED"]) and "OPEN" not in status
        
        status_str = f"[{status}]"
        print(f"  {tv_id:<6} {status_str:<18} : {desc[:50]}")
        
        if is_closed:
            closed_items.append(tv_id)
        else:
            open_items.append((tv_id, status, desc))

    print("-" * 80)
    print(f"TOTAL TV ITEMS : {len(tv_items)}")
    print(f"CLOSED / LOCKED: {len(closed_items)}")
    print(f"OPEN ITEMS     : {len(open_items)}")
    print("=" * 80)

    if open_items:
        print("\nWARNING / FAIL: The following items remain OPEN:")
        for tv_id, st, desc in open_items:
            print(f"  * {tv_id}: {st} - {desc}")
        sys.exit(1)
    else:
        print("\nSUCCESS: 100% of Technical Variations are formally CLOSED and verified!")
        sys.exit(0)

if __name__ == "__main__":
    main()
