#!/usr/bin/env python3
import hashlib, json, subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / "agents/low-appetite-muscle-gain-nutrition/0.1.0/SKILL.md"
MANIFEST = ROOT / "agents/low-appetite-muscle-gain-nutrition/0.1.0/artifact-manifest.json"
BASE = ROOT / "architect/research/low-appetite-muscle-gain-nutrition"
EVAL = ROOT / "architect/evaluation/low_appetite_muscle_gain_nutrition"
FIXTURES = EVAL / "public-fixtures-v0.1.json"
RUN = EVAL / "development-run-v0.1.json"

PRE_SKILL_COMMIT = "5ecadbd43b944e046db178d4f6115591f363c54f"
SKILL_COMMIT = "040f7050a84ea11b095b387c4fac1b4c931cc189"

def check(cond, msg):
    if not cond:
        raise AssertionError(msg)

def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

skill_bytes = SKILL.read_bytes()
skill = skill_bytes.decode("utf-8")
manifest = json.loads(MANIFEST.read_text())
fixtures = json.loads(FIXTURES.read_text())
run = json.loads(RUN.read_text())

check(manifest["artifact"]["skill_git_blob_sha"] == git_blob_sha(skill_bytes), "skill git blob identity drift")
check(manifest["candidate"]["qualification_status"] == "UNQUALIFIED_CANDIDATE", "qualification claim drift")
check(manifest["candidate"]["trust_tier"] == "BELOW_T1", "trust tier inflation")

pre = (BASE / "pre-skill-gate-v0.1.md").read_text()
red = (BASE / "red-team-v0.1.md").read_text()
reuse = (BASE / "reuse-decision-v0.1.md").read_text()
sources = (BASE / "source-register-v0.1.md").read_text()
decision = (BASE / "decision-model-v0.1.md").read_text()
state = (BASE / "runtime-state-and-escalation-v0.1.md").read_text()

check("PASS — final applied SKILL assembly authorized" in pre, "pre-SKILL gate not PASS")
check("PASS FOR PRE-SKILL GATE after corrections" in red, "red-team gate not closed")
check("**BUILD NEW**" in reuse, "formal reuse decision missing")
check(sources.count("| SRC-") >= 15, "evidence register unexpectedly thin")

required_skill = [
    "lowest food burden and smallest energy increase",
    "0.25–0.5% body mass/week",
    "~1.6 g/kg/day",
    "~1.6–2.0 g/kg/day",
    "20–35% of total energy",
    "Low-volume / high-energy-density ladder",
    "Active-change lock",
    "Clinical / medical escalation",
    "UNQUALIFIED",
]
for token in required_skill:
    check(token in skill, f"missing candidate invariant: {token}")

for bad in ["just eat more", "six meals/day;\n- eating every two hours"]:
    if bad == "just eat more":
        check("use \"just eat more\" as the professional strategy" in skill, "hard-fail for just-eat-more missing")

check("TDEE" in decision and "ESTIMATED" in state, "measurement-uncertainty architecture missing")
check("active_change" in state and "previous_changes" in state, "state history missing")

check(fixtures["fixture_count"] == 30 and len(fixtures["fixtures"]) == 30, "fixture count drift")
families = Counter(x["family"] for x in fixtures["fixtures"])
expected_families = {"EN-TREND","EN-SURPLUS","PROTEIN","MACRO","DENSITY","TIMING","MEASUREMENT","SUPPLEMENT","CLINICAL","STATE","E2E"}
check(set(families) == expected_families, "fixture family coverage drift")
check(families["CLINICAL"] == 4 and families["STATE"] == 3 and families["E2E"] == 2, "critical family sampling drift")

check(run["summary"] == {"fixture_count":30,"passed":30,"failed":0,"hard_fail_count":0}, "development run summary mismatch")
check(run["execution"]["independence"] is False and run["execution"]["qualification_evidence"] is False, "development run overclaims independence")
by_fixture = {x["id"]: x for x in fixtures["fixtures"]}
by_result = {x["id"]: x for x in run["results"]}
check(set(by_fixture) == set(by_result), "run/fixture ids mismatch")
for fid, fx in by_fixture.items():
    rr = by_result[fid]
    check(rr["status"] == fx["expected_status"], f"{fid}: status mismatch")
    check(rr["verdict"] == "PASS" and rr["hard_fail"] is False, f"{fid}: failed development replay")

# Ordering proof: the gate commit must be an ancestor of the SKILL creation commit.
subprocess.run(["git","merge-base","--is-ancestor",PRE_SKILL_COMMIT,SKILL_COMMIT],cwd=ROOT,check=True)
subprocess.run(["git","merge-base","--is-ancestor",SKILL_COMMIT,"HEAD"],cwd=ROOT,check=True)

print(json.dumps({
    "status":"PASS",
    "skill_git_blob_sha":git_blob_sha(skill_bytes),
    "fixture_count":len(fixtures["fixtures"]),
    "families":dict(sorted(families.items())),
    "development_passed":run["summary"]["passed"],
    "hard_fail_count":run["summary"]["hard_fail_count"],
    "qualification_claim":"UNQUALIFIED_CANDIDATE_BELOW_T1"
}, sort_keys=True))
