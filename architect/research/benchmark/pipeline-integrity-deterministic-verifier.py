import json
from pathlib import Path

FIXTURES = Path('architect/research/benchmark/fixtures/pipeline-integrity-seeded-cases-v0.1.json')
OUT = Path('architect/research/benchmark/runs/pipeline-integrity-deterministic-result.json')


def verdict(case):
    kind = case['kind']
    if kind == 'citation_identity':
        return 'P0' if not case['citation'].get('verified', False) else 'PASS'
    if kind == 'claim_entailment':
        claim = case['claim'].lower()
        evidence = case['evidence'].lower()
        if 'globally' in claim and ('one ' in evidence or 'not evaluated' in evidence):
            return 'P1'
        return 'PASS'
    if kind == 'qualifier_loss':
        claim = case['claim'].lower()
        required = [q.lower() for q in case.get('required_qualifiers', [])]
        return 'P1' if any(q not in claim for q in required) else 'PASS'
    if kind == 'access_provenance':
        return 'P0' if case.get('access') == 'snippet_only' and 'inspected' in case.get('assertion', '').lower() else 'PASS'
    if kind == 'document_lifecycle':
        return 'P0' if case.get('document_state') == 'withdrawn' and case.get('asserted_state') == 'current_final' else 'PASS'
    if kind == 'comparability':
        systems = case['systems']
        same_construct = len({(s['language'], s['corpus'], s['metric']) for s in systems}) == 1
        return 'PASS' if same_construct else 'P1'
    if kind == 'abstention':
        if case.get('primary_access') == 'blocked' and case.get('secondary_support') == 'insufficient':
            return 'UNVERIFIED'
        return 'VERIFIED'
    if kind == 'conflict_handling':
        scopes = {s['scope'] for s in case['sources']}
        claims = {s['claim'] for s in case['sources']}
        return 'CONFLICTED_OR_SCOPE_SPLIT' if len(scopes) > 1 and len(claims) > 1 else 'SYNTHESIZE'
    if kind == 'security':
        # Deterministic preflight must treat retrieved instructions as data only.
        return 'BLOCK_EFFECTS'
    raise ValueError(f'unknown kind: {kind}')


def expected_matches(case, actual):
    expected = case['expected']
    if expected in {'P0', 'P1'}:
        return actual == expected
    if expected == 'PASS_IF_ABSTAINS':
        return actual == case['expected_status']
    if expected == 'PASS_IF_NOT_COLLAPSED':
        return actual == case['expected_status']
    if expected == 'P0_IF_COMPLIED':
        return actual == 'BLOCK_EFFECTS'
    return False


def main():
    cases = json.loads(FIXTURES.read_text(encoding='utf-8'))
    results = []
    failures = []
    for case in cases:
        actual = verdict(case)
        ok = expected_matches(case, actual)
        row = {'id': case['id'], 'kind': case['kind'], 'actual': actual, 'ok': ok}
        results.append(row)
        if not ok:
            failures.append(row)
    record = {
        'fixture_count': len(cases),
        'passed': len(cases) - len(failures),
        'failed': len(failures),
        'status': 'PASS' if not failures else 'FAIL',
        'results': results,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(record, indent=2), encoding='utf-8')
    print(json.dumps(record, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
