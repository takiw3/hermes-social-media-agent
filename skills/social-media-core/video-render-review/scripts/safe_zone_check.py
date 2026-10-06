#!/usr/bin/env python3
"""Check that a text box sits inside owner-confirmed safe margins.

    python3 safe_zone_check.py --canvas 1080x1920 \\
        --margins top=220,right=90,bottom=420,left=90 --box x=90,y=1180,w=900,h=150

Margins are the owner's confirmed values from local/brand-and-visual-identity.md.
This profile holds no verified official safe-zone figures for any platform.
Standard library only. Reads no file and makes no network call. Exit 0 inside,
5 outside, 2 on bad input.
"""
import argparse
import json
import sys


def pairs(text, keys):
    out = {}
    for part in text.split(","):
        k, _, v = part.partition("=")
        out[k.strip()] = float(v)
    missing = [k for k in keys if k not in out]
    if missing:
        raise ValueError(f"missing {missing}")
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--canvas", required=True)
    p.add_argument("--margins", required=True)
    p.add_argument("--box", required=True)
    a = p.parse_args()
    try:
        w, h = (float(v) for v in a.canvas.lower().split("x"))
        m = pairs(a.margins, ["top", "right", "bottom", "left"])
        b = pairs(a.box, ["x", "y", "w", "h"])
    except Exception as exc:
        print(json.dumps({"status": "bad input", "error": str(exc)}))
        return 2
    safe = {"left": m["left"], "top": m["top"], "right": w - m["right"], "bottom": h - m["bottom"]}
    over = {
        "left": max(0.0, safe["left"] - b["x"]),
        "top": max(0.0, safe["top"] - b["y"]),
        "right": max(0.0, b["x"] + b["w"] - safe["right"]),
        "bottom": max(0.0, b["y"] + b["h"] - safe["bottom"]),
    }
    inside = not any(over.values())
    print(json.dumps({
        "check": "safe_zone", "result": "pass" if inside else "fail",
        "safe_area": safe, "box": b, "overflow_px": over,
        "margins_source": "owner-confirmed",
    }, indent=2))
    return 0 if inside else 5


if __name__ == "__main__":
    sys.exit(main())
