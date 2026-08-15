import ipaddress
import json
import socket
import urllib.parse
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path

OUT = Path('architect/research/benchmark/runs/network-url-security-boundary-v0.1.json')

ALLOWED_SCHEMES = {'https'}
MAX_REDIRECTS = 5

@dataclass
class Decision:
    url: str
    allowed: bool
    reason: str
    normalized_host: str | None = None
    resolved_ips: list[str] | None = None


def _normalize_host(host: str) -> str:
    host = host.rstrip('.').strip().lower()
    if not host:
        raise ValueError('empty-host')
    return host.encode('idna').decode('ascii')


def _ip_is_public(ip_text: str) -> bool:
    ip = ipaddress.ip_address(ip_text)
    # global is intentionally stricter than merely "not private" and excludes
    # loopback, link-local, multicast, unspecified, documentation/reserved ranges.
    return ip.is_global


def _literal_ip(host: str):
    try:
        return ipaddress.ip_address(host)
    except ValueError:
        return None


def validate_url(url: str, dns_map: dict[str, list[str]] | None = None) -> Decision:
    try:
        p = urllib.parse.urlsplit(url)
    except Exception:
        return Decision(url, False, 'parse-error')

    if p.scheme.lower() not in ALLOWED_SCHEMES:
        return Decision(url, False, 'scheme-not-allowed')
    if p.username is not None or p.password is not None:
        return Decision(url, False, 'userinfo-not-allowed')
    if not p.hostname:
        return Decision(url, False, 'missing-host')
    if p.port not in (None, 443):
        return Decision(url, False, 'nonstandard-port-not-allowed')

    try:
        host = _normalize_host(p.hostname)
    except Exception:
        return Decision(url, False, 'invalid-host')

    literal = _literal_ip(host)
    if literal is not None:
        ok = _ip_is_public(str(literal))
        return Decision(url, ok, 'public-ip-literal' if ok else 'non-public-ip-literal', host, [str(literal)])

    # DNS resolution is part of authorization. Every returned address must be public.
    try:
        if dns_map is not None:
            ips = dns_map.get(host)
            if ips is None:
                raise OSError('mock-dns-no-answer')
        else:
            infos = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
            ips = sorted({i[4][0] for i in infos})
    except Exception:
        return Decision(url, False, 'dns-resolution-failed', host, [])

    if not ips:
        return Decision(url, False, 'dns-empty', host, [])
    bad = [ip for ip in ips if not _ip_is_public(ip)]
    if bad:
        return Decision(url, False, 'dns-resolves-non-public', host, ips)
    return Decision(url, True, 'authorized-public-https', host, ips)


def validate_redirect_chain(urls: list[str], dns_map: dict[str, list[str]]) -> tuple[bool, list[Decision], str]:
    if len(urls) - 1 > MAX_REDIRECTS:
        return False, [], 'too-many-redirects'
    decisions = []
    for u in urls:
        d = validate_url(u, dns_map=dns_map)
        decisions.append(d)
        if not d.allowed:
            return False, decisions, f'redirect-hop-denied:{d.reason}'
    return True, decisions, 'all-hops-authorized'


def run():
    dns = {
        'example.com': ['93.184.216.34'],
        'safe.example': ['8.8.8.8'],
        'mixed.example': ['8.8.8.8', '127.0.0.1'],
        'metadata.example': ['169.254.169.254'],
        'v6local.example': ['::1'],
        'private.example': ['10.23.1.7'],
        'cgnat.example': ['100.64.0.10'],
        'docs.example': ['1.1.1.1'],
    }

    cases = [
        ('allow_public_https', 'https://example.com/a', True),
        ('deny_http', 'http://example.com/a', False),
        ('deny_file', 'file:///etc/passwd', False),
        ('deny_gopher', 'gopher://127.0.0.1/', False),
        ('deny_localhost_literal', 'https://127.0.0.1/', False),
        ('deny_ipv6_loopback', 'https://[::1]/', False),
        ('deny_link_local_metadata', 'https://169.254.169.254/latest/meta-data/', False),
        ('deny_private_rfc1918', 'https://10.0.0.1/', False),
        ('deny_userinfo_confusion', 'https://example.com@127.0.0.1/', False),
        ('deny_userinfo_even_public_target', 'https://user:pass@example.com/', False),
        ('deny_nonstandard_port', 'https://example.com:8443/', False),
        ('deny_dns_private', 'https://private.example/x', False),
        ('deny_dns_mixed_public_private', 'https://mixed.example/x', False),
        ('deny_dns_linklocal', 'https://metadata.example/x', False),
        ('deny_dns_v6_loopback', 'https://v6local.example/x', False),
        ('allow_idna_normal_public', 'https://docs.example/x', True),
        ('deny_dns_failure', 'https://missing.example/x', False),
    ]

    results = []
    failures = []
    for cid, url, expected in cases:
        d = validate_url(url, dns_map=dns)
        passed = d.allowed == expected
        results.append({'case_id': cid, 'expected_allowed': expected, 'passed': passed, 'decision': asdict(d)})
        if not passed:
            failures.append(cid)

    redirect_cases = [
        ('allow_safe_redirect', ['https://example.com/a', 'https://safe.example/b'], True),
        ('deny_redirect_to_loopback', ['https://example.com/a', 'https://127.0.0.1/admin'], False),
        ('deny_redirect_to_metadata', ['https://example.com/a', 'https://metadata.example/latest'], False),
        ('deny_redirect_to_http', ['https://example.com/a', 'http://example.com/b'], False),
        ('deny_redirect_to_mixed_dns', ['https://example.com/a', 'https://mixed.example/b'], False),
        ('deny_excessive_redirects', ['https://example.com'] * 7, False),
    ]
    for cid, chain, expected in redirect_cases:
        allowed, decisions, reason = validate_redirect_chain(chain, dns)
        passed = allowed == expected
        results.append({'case_id': cid, 'expected_allowed': expected, 'passed': passed, 'redirect_reason': reason, 'decisions': [asdict(x) for x in decisions]})
        if not passed:
            failures.append(cid)

    record = {
        'timestamp_utc': datetime.now(timezone.utc).isoformat(),
        'gate': 'network-url-security-boundary-v0.1',
        'policy': {
            'allowed_schemes': sorted(ALLOWED_SCHEMES),
            'allowed_ports': [443],
            'all_dns_answers_must_be_global': True,
            'redirects_revalidated_each_hop': True,
            'max_redirects': MAX_REDIRECTS,
            'userinfo_allowed': False,
        },
        'scope_limitations': [
            'Deterministic authorization policy only; it does not prove host-level egress isolation.',
            'DNS authorization before connection is insufficient against rebinding/TOCTOU unless the transport pins the authorized IP for the actual connection and revalidates every redirect.',
            'No claim is made that arbitrary subprocesses cannot open sockets outside this adapter.',
        ],
        'results': results,
        'failures': failures,
        'status': 'PASS' if not failures else 'FAIL_P0',
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(record, indent=2), encoding='utf-8')
    print(json.dumps(record, indent=2))
    if failures:
        raise SystemExit(2)

if __name__ == '__main__':
    run()
