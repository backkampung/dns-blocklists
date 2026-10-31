#!/usr/bin/env python3
"""Combine HaGeZi adblock lists into one deduplicated list for AdGuard Home.

Sources (AdBlock format, same format in, same format out):
  - Multi PRO
  - Threat Intelligence Feeds, medium version
  - Fake
Output: adblock/mini.txt
Rules are deduplicated by exact line and sorted, so diffs stay stable
between runs. Header comments (starting with '!') are regenerated
on every run and are not carried over from the sources.
"""
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SOURCES = [
    ("Multi PRO", "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.txt"),
    ("Threat Intelligence Feeds (medium)", "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/tif.medium.txt"),
    ("Fake", "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/fake.txt"),
]

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "adblock" / "mini.txt"


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "dns-blocklists-combined/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        if resp.status != 200:
            raise RuntimeError(f"{url} returned HTTP {resp.status}")
        return resp.read().decode("utf-8", errors="replace")


def main() -> int:
    rules = set()
    per_source = []
    for name, url in SOURCES:
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
            rules.add(line)
        per_source.append(f"{name}: {len(rules) - count_before} new rules")

    now = datetime.now(timezone.utc)
    header = [
        "[Adblock Plus]",
        "",
        "! Title: Combined HaGeZi Blocklist (PRO + TIF medium + Fake)",
        "! Description: Deduplicated combination of HaGeZi Multi PRO, Threat Intelligence Feeds (medium) and Fake, in AdBlock format for AdGuard Home.",
        "! Homepage: https://github.com/backkampung/dns-blocklists",
        "! License: GPL-3.0 - derived from HaGeZi dns-blocklists (https://github.com/hagezi/dns-blocklists). Not affiliated with HaGeZi.",
        "! Sources:",
    ]
    for name, url in SOURCES:
        header.append(f"!   - {name}: {url}")
    header += [
        "! Expires: 6 hours",
        f"! Last modified: {now.strftime('%d %b %Y %H:%M UTC')}",
        f"! Version: {now.strftime('%Y.%m%d.%H%M')}",
        "! Syntax: AdBlock",
        f"! Number of entries: {len(rules)}",
        "",
    ]

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(header + sorted(rules)) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT} with {len(rules)} unique rules")
    for line in per_source:
        print(f"  {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
