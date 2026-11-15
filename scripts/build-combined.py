#!/usr/bin/env python3
"""Combine blocklists into one deduplicated list for AdGuard Home.

Tiers (AdBlock format, same format in, same format out). All tiers share
the same TIF medium + AdGuard DNS + DynDNS sources; only the HaGeZi
"Multi" base list changes:
  - mini:    HaGeZi Multi PRO        -> adblock/mini.txt
  - pro:     HaGeZi Multi PRO++      -> adblock/pro.txt
  - pro-max: HaGeZi Multi ULTIMATE   -> adblock/pro-max.txt
Note: HaGeZi Fake is intentionally NOT included - 99.94% of its rules
are already in Multi PRO (verified 2026-11-01: only 5 Fake-only rules),
so it adds nothing material.
Rules are deduplicated by exact line and sorted, so diffs stay stable
between runs. Header comments (starting with '!') are regenerated
on every run and are not carried over from the sources.

Usage:
  python3 build-combined.py [--tier mini|pro|pro-max] [--all]
  Default tier is mini. --all builds all three tiers.
"""
import argparse
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HAGEZI_BASE = "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/"

COMMON_SOURCES = [
    ("Threat Intelligence Feeds (medium)", HAGEZI_BASE + "tif.medium.txt"),
    ("AdGuard DNS filter", "https://adguardteam.github.io/AdGuardSDNSFilter/Filters/filter.txt"),
    ("DynDNS", HAGEZI_BASE + "dyndns.txt"),
]

# Tier config: HaGeZi base list (name, filename), output file, title label.
TIERS = {
    "mini": {
        "hagezi_name": "Multi PRO",
        "hagezi_file": "pro.txt",
        "output": "adblock/mini.txt",
        "label": "PRO",
    },
    "pro": {
        "hagezi_name": "Multi PRO++",
        "hagezi_file": "pro.plus.txt",
        "output": "adblock/pro.txt",
        "label": "PRO++",
    },
    "pro-max": {
        "hagezi_name": "Multi ULTIMATE",
        "hagezi_file": "ultimate.txt",
        "output": "adblock/pro-max.txt",
        "label": "ULTIMATE",
    },
}

ROOT = Path(__file__).resolve().parent


def sources_for(tier: str):
    cfg = TIERS[tier]
    return [
        (cfg["hagezi_name"], HAGEZI_BASE + cfg["hagezi_file"]),
        *COMMON_SOURCES,
    ]


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "dns-blocklists-combined/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        if resp.status != 200:
            raise RuntimeError(f"{url} returned HTTP {resp.status}")
        return resp.read().decode("utf-8", errors="replace")


def build(tier: str) -> int:
    cfg = TIERS[tier]
    sources = sources_for(tier)
    output = ROOT / cfg["output"]

    rules = set()
    per_source = []
    for name, url in sources:
        text = fetch(url)
        count_before = len(rules)
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            if line == "[Adblock Plus]":
                continue
            if line.startswith("!"):
                continue
            if line.startswith("#"):
                # SDNS embeds some '#' comment lines from its own sources;
                # they are not domain rules and are useless for DNS blocking.
                continue
            rules.add(line)
        per_source.append(f"{name}: {len(rules) - count_before} new rules")

    now = datetime.now(timezone.utc)
    label = cfg["label"]
    hagezi_name = cfg["hagezi_name"]
    header = [
        "[Adblock Plus]",
        "",
        f"! Title: Combined Blocklist ({label} + TIF medium + AdGuard DNS + DynDNS)",
        f"! Description: Deduplicated combination of HaGeZi {hagezi_name}, Threat Intelligence Feeds (medium), AdGuard DNS filter and HaGeZi DynDNS, in AdBlock format for AdGuard Home.",
        "! Homepage: https://github.com/backkampung/dns-blocklists",
        "! License: GPL-3.0 - derived from HaGeZi dns-blocklists (https://github.com/hagezi/dns-blocklists) and AdGuardSDNSFilter (https://github.com/AdguardTeam/AdGuardSDNSFilter). Not affiliated with HaGeZi or AdGuard.",
        "! Sources:",
    ]
    for name, url in sources:
        header.append(f"!   - {name}: {url}")
    header += [
        "! Expires: 6 hours",
        f"! Last modified: {now.strftime('%d %b %Y %H:%M UTC')}",
        f"! Version: {now.strftime('%Y.%m%d.%H%M')}",
        "! Syntax: AdBlock",
        f"! Number of entries: {len(rules)}",
        "",
    ]

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(header + sorted(rules)) + "\n", encoding="utf-8")
    print(f"[{tier}] Wrote {output} with {len(rules)} unique rules")
    for line in per_source:
        print(f"  {line}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Build combined blocklist tier(s).")
    parser.add_argument("--tier", choices=sorted(TIERS), default="mini",
                        help="Tier to build (default: mini).")
    parser.add_argument("--all", action="store_true",
                        help="Build all three tiers.")
    args = parser.parse_args()
    tiers = sorted(TIERS) if args.all else [args.tier]
    for tier in tiers:
        build(tier)
    return 0


if __name__ == "__main__":
    sys.exit(main())
