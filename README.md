# dns-blocklists

A combined, deduplicated DNS blocklist for AdGuard Home, built from
well-known upstream lists so you only need to subscribe to one URL
instead of four.

## Why is it called "mini"?

"mini" is a **relative name, not a claim that this list is small**.
It is the smallest tier in a planned family:

- **mini** (this file) — HaGeZi Multi PRO based, the balanced tier.
- **PRO** (planned) — based on HaGeZi Multi PRO++, a larger,
  more aggressive tier.
- **PRO MAX** (planned) — based on HaGeZi Multi ULTIMATE, the
  largest tier.

So "mini" means "the smallest of this family", compared with the
planned PRO / PRO MAX versions. In absolute terms it is still a
large list: about **582,000 rules, about 13 MB** (the exact count
is in the header of `adblock/mini.txt` and changes as upstream
lists update). Check the rule count shown in AdGuard Home's
Filters page — AdGuard Home may count rules differently from
the header.

### Raspberry Pi and low-memory devices: who should worry?

Most Raspberry Pi users do **not** need to worry. Be specific
about the cutoff, instead of warning everyone:

- **Not suitable: devices with less than 1 GB of RAM in total**
  (for example Raspberry Pi Zero, Pi 1 and Pi 2, or a router
  with 512 MB). AdGuard Home itself, the operating system and
  a 582,000-rule list together leave too little headroom, and
  memory use spikes further while a list is updating. Use a
  smaller list on these devices instead.
- **Borderline: 1 GB devices** (for example Raspberry Pi 3 and
  Pi Zero 2 W), especially if the same device also runs other
  services such as CasaOS, Docker containers or a media server.
  AdGuard Home alone can run, but a list update can push it
  into swap. If you try it, watch memory during a list update
  and consider shortening the query-log retention in AdGuard
  Home's DNS settings.
- **No special concern: 2 GB or more** (for example Raspberry
  Pi 4 / Pi 5 with 2 GB, 4 GB or 8 GB, a NAS, a mini PC or a
  VM with 2 GB+). This is the normal case for AdGuard Home
  with a list of this size. HaGeZi's own guidance for the
  TIF medium list alone is at least 1 GB for AdGuard Home;
  this combined list is larger than PRO + TIF alone, so treat
  1 GB as the floor, not as comfortable headroom.

Actual memory use also depends on what else runs on the same
device and on AdGuard Home's query-log retention, so treat the
cutoffs above as guidance, not as a guarantee for every setup.

## Use it in AdGuard Home

Filters -> DNS blocklists -> Add blocklist, with this URL:

```
https://raw.githubusercontent.com/backkampung/dns-blocklists/main/adblock/mini.txt
```

Then remove the separate lists it replaces, so you only keep this one.

If something stops working after you add it, disable this list
first and check AdGuard Home's Query Log for the blocked domain
before assuming your network is down.

## Want YouTube ads blocked? Use a browser extension as well

DNS alone cannot do this, and this is by design, not a bug in
the list. A YouTube video ad is served from the same domains as
the video itself, so blocking the domain at the DNS layer would
block the video too. To block YouTube ads, add a browser layer
on top of AdGuard Home:

1. Install the **AdGuard Browser Extension** for Chrome or
   Firefox, and keep its default filters enabled. It can see
   and hide page elements and video-ad requests in the browser,
   which DNS cannot, and that is what blocks YouTube ads.
2. If you also want this combined list inside the browser,
   open the extension's Settings -> Filters -> Custom ->
   Add custom filter, and paste the same `mini.txt` URL above.
   This is optional. Be clear about what each part does:
   adding `mini.txt` to the extension adds domain blocking
   in that browser; the YouTube video-ad blocking itself comes
   from the extension's own filters, not from adding
   `mini.txt` alone.

Two honest limits to keep in mind:

- The extension only protects the browser it is installed in.
  It does not block ads in the YouTube app on a phone or TV,
  or in other browsers on the same device. AdGuard Home still
  covers the whole network at the DNS layer; the extension
  covers YouTube in that one browser.
- YouTube actively fights ad blockers, so YouTube ad blocking
  is a moving target. If ads reappear, first update the
  extension's filters and check that YouTube is not on the
  extension's allowlist, before blaming the DNS list.

## What is inside

`adblock/mini.txt` is built from these lists, in AdBlock format,
deduplicated by exact rule:

- HaGeZi Multi PRO: https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.txt
- HaGeZi Threat Intelligence Feeds, medium version: https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/tif.medium.txt
- AdGuard DNS filter: https://adguardteam.github.io/AdGuardSDNSFilter/Filters/filter.txt
- HaGeZi DynDNS: https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/dyndns.txt

Note: HaGeZi Fake is intentionally not included — 99.94% of its
rules are already in Multi PRO (verified 2026-11-01: only 5
Fake-only rules), so it adds nothing material.

### This list is not a pure blocklist: it contains allow rules

This is important to know before you subscribe. The generated
file contains, in addition to domain block rules, about **212
`@@` allow rules** inherited from the AdGuard DNS filter, plus a
small number (about 130) of non-domain patterns that are useless
at the DNS layer. In AdGuard Home, an allow rule takes precedence
over a block rule, so those 212 domains are deliberately allowed
even if another source blocks them. They come from the upstream
AdGuard filter's breakage exceptions (for example, some ad,
affiliate and analytics domains that certain sites need in order
to work). They are not added by this repository, and this
repository does not hide them — you can see them by searching
`mini.txt` for lines starting with `@@`.

If you want maximum blocking and would rather manage exceptions
yourself, do not rely on this file alone: add your own allow
rules in AdGuard Home (Filters -> Custom filtering rules,
`@@||domain^`) only for sites you actually need, and consider
subscribing to the upstream lists directly instead (see
"Run it yourself" below).

## What this list is, and is not

It is:

- A DNS-layer blocklist: it stops a domain from resolving, for
  ads, tracking, telemetry, phishing, malware, scam and dynamic
  DNS abuse domains covered by the four sources above.

It is not:

- A VPN, a firewall, or a malware scanner.
- A YouTube / in-video ad blocker. DNS cannot see inside a video
  stream, so ads served from the same domain as the content will
  not be blocked by this list. See "Want YouTube ads blocked?
  Use a browser extension as well" above for the browser-layer
  solution.
- A defence against DNS bypass. A device using its own DoH, VPN
  or proxy can bypass AdGuard Home entirely; blocking that needs
  network-level rules, not just this list.
- A guarantee against new phishing domains. Threat feeds cover
  known bad domains; a domain registered minutes ago may not be
  in any list yet.
- A vendor native-tracker list. Xiaomi, Huawei and other vendors'
  native telemetry is only partially covered by these sources.
  A dedicated vendor tracker list is a separate decision, and
  blocking vendor telemetry can affect system updates and cloud
  services, so test it separately before adding it.

## DynDNS warning: read this before you enable it

HaGeZi DynDNS blocks whole dynamic-DNS providers, including
legitimate personal services you may use for remote access, for
example `duckdns.org`, `no-ip.com`, `asuscomm.com` and
`diskstation.me`. If you use any of them for a NAS, router or
home server:

1. Add an allow rule for the exact domain you use in AdGuard
   Home (Filters -> Custom filtering rules, for example
   `@@||your-name.duckdns.org^`) **before** you enable this list,
   or
2. Do not use this list, and subscribe to the upstream lists
   without DynDNS instead.

Do not discover this by losing remote access to your own server.

## Updates

The file is rebuilt automatically every 6 hours (UTC) by
`.github/workflows/update.yml`, which runs
`scripts/build-combined.py`. To rebuild on demand: Actions ->
Update combined blocklist -> Run workflow.

Do not edit `adblock/mini.txt` by hand — the next automatic run
overwrites it, and hand edits would hide the real source of a
rule.

If an update fails, AdGuard Home keeps the last version it
successfully fetched; it does not suddenly become unprotected,
it just becomes stale. You can check freshness yourself in the
header at the top of `mini.txt` (`Last modified` and `Version`).

## How you can verify this repository

You do not have to trust this repository blindly. Everything
needed to check it is public:

- **The build script is short and readable.**
  `scripts/build-combined.py` is about 90 lines. It only
  downloads the four source URLs listed above over HTTPS,
  deduplicates by exact line, sorts the result and writes
  `adblock/mini.txt`. It does not collect, upload or send any
  of your data, and it does not run anything else.
- **The generated file is never hand-edited.** Every change to
  `adblock/mini.txt` in the commit history is made by the
  `github-actions[bot]` account from the workflow run, not by a
  person editing the file directly.
- **You can reproduce it locally.** Clone the repository and
  run `python3 scripts/build-combined.py`; you should get a
  file with a comparable rule count (upstream lists change
  during the day, so the exact count will differ slightly).
- **You can run it yourself.** If you would rather trust no
  third party at all, fork this repository, read
  `scripts/build-combined.py` once, and subscribe to the
  `mini.txt` URL from your own fork. That way the only code
  you trust is the upstream lists plus a script you have read.

## False positives and feedback

This is a personally maintained combined list, not an official
HaGeZi or AdGuard product. If a legitimate site or service is
blocked:

1. Find the domain in AdGuard Home's Query Log.
2. Add a temporary allow rule for it in AdGuard Home.
3. Report it in this repository's Issues, with the domain and
   which source list you think it came from, so the source or
   the build can be checked.

## Licence and credit

Derived from [HaGeZi dns-blocklists](https://github.com/hagezi/dns-blocklists), GPL-3.0, and [AdGuardSDNSFilter](https://github.com/AdguardTeam/AdGuardSDNSFilter), GPL-3.0. This repository is not affiliated with HaGeZi or AdGuard.
