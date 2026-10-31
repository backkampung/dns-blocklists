# dns-blocklists

Combined, deduplicated HaGeZi blocklist for AdGuard Home.

## Use it in AdGuard Home

Filters -> DNS blocklists -> Add blocklist, with this URL:

```
https://raw.githubusercontent.com/backkampung/dns-blocklists/main/adblock/mini.txt
```

Then remove the three separate HaGeZi lists it replaces, so you only keep this one.

## What is inside

`adblock/mini.txt` is built from these three HaGeZi lists, in AdBlock format, deduplicated by exact rule:

- Multi PRO: https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.txt
- Threat Intelligence Feeds, medium version: https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/tif.medium.txt
- Fake: https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/fake.txt

## Updates

The file is rebuilt automatically every 6 hours by `.github/workflows/update.yml`, which runs `scripts/build-combined.py`. To rebuild on demand: Actions -> Update combined blocklist -> Run workflow.

Do not edit `adblock/mini.txt` by hand - the next automatic run overwrites it.

## Licence and credit

Derived from [HaGeZi dns-blocklists](https://github.com/hagezi/dns-blocklists), GPL-3.0. This repository is not affiliated with HaGeZi.
