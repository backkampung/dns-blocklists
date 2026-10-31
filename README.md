# dns-blocklists

Combined, deduplicated blocklist for AdGuard Home.

## Use it in AdGuard Home

Filters -> DNS blocklists -> Add blocklist, with this URL:

```
https://raw.githubusercontent.com/backkampung/dns-blocklists/main/adblock/mini.txt
```

Then remove the separate lists it replaces, so you only keep this one.

## What is inside

`adblock/mini.txt` is built from these lists, in AdBlock format, deduplicated by exact rule:

- HaGeZi Multi PRO: https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.txt
- HaGeZi Threat Intelligence Feeds, medium version: https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/tif.medium.txt
- AdGuard DNS filter: https://adguardteam.github.io/AdGuardSDNSFilter/Filters/filter.txt
- HaGeZi DynDNS: https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/dyndns.txt

Note: HaGeZi Fake is intentionally not included - 99.94% of its rules are already in Multi PRO (verified 2026-11-01), so it adds nothing material. DynDNS blocks whole dynamic-DNS providers, including legitimate personal DDNS services (e.g. duckdns.org, no-ip, asuscomm.com, diskstation.me) - allowlist any you actually use for remote access.

## Updates

The file is rebuilt automatically every 6 hours by `.github/workflows/update.yml`, which runs `scripts/build-combined.py`. To rebuild on demand: Actions -> Update combined blocklist -> Run workflow.

Do not edit `adblock/mini.txt` by hand - the next automatic run overwrites it.

## Licence and credit

Derived from [HaGeZi dns-blocklists](https://github.com/hagezi/dns-blocklists), GPL-3.0, and [AdGuardSDNSFilter](https://github.com/AdguardTeam/AdGuardSDNSFilter). This repository is not affiliated with HaGeZi or AdGuard.
