#!/usr/bin/env python3
"""Stage A deterministic verification for issue #319 (Motion Graphics v0.3).

Zero model calls. Reads only frozen git objects from the freeze commit.
Exit 0 => STAGE_A_PASS. Exit 1 => STATIC_CONTRACT_FAIL.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys

REPO = "/home/user/professional-ai-agents"
BRANCH = "repair/motion-graphics-v0-3-production-incident-2026-09-16"
FREEZE = "83fed979f9dd0c2cbed51fd2a4703a5e2f415c0d"
EVDIR = "architect/evaluation/video_motion_graphics"
FREEZE_MANIFEST = f"{EVDIR}/candidate-freeze-v0.3.json"

PARENT_DIR = "architect/library/cores/video-editing-post-production/0.1.0"
HIST_V02_DIGEST = "sha256:55e04a52f789f42e0213d75534d9772ccca0c6a26e372b7c54d57004258f1fe6"

checks: list[tuple[str, bool, str]] = []


def git(*args: str) -> str:
    return subprocess.run(
        ["git", "-C", REPO, *args], capture_output=True, text=True, check=True
    ).stdout.strip()


def blob(path: str, rev: str = FREEZE) -> str:
    return git("rev-parse", f"{rev}:{path}")


def show(path: str, rev: str = FREEZE) -> str:
    return git("show", f"{rev}:{path}")


def check(name: str, ok: bool, detail: str = "") -> None:
    checks.append((name, bool(ok), detail))


# A1 — exact branch + freeze commit
head = git("rev-parse", f"refs/remotes/origin/{BRANCH}")
check("A1_branch_head_is_freeze_commit", head == FREEZE, f"origin/{BRANCH}={head}")
check("A1_freeze_object_is_commit", git("cat-file", "-t", FREEZE) == "commit", FREEZE)

manifest = json.loads(show(FREEZE_MANIFEST))

# A2 — candidate identity
check(
    "A2_candidate_identity",
    manifest["candidate_id"] == "motion-graphics-visual-explanation-video"
    and manifest["candidate_version"] == "0.3.0-candidate",
    f'{manifest["candidate_id"]}@{manifest["candidate_version"]}',
)

# A3 — 18 visible development fixtures, ids unique and equal to the frozen list
fixtures = json.loads(show(f"{EVDIR}/semantic-fixtures-v0.3-production-incident.json"))
ids = [f["id"] for f in fixtures]
expected_ids = [f"MG3-D{i:02d}" for i in range(1, 19)]
check("A3_fixture_count_18", len(fixtures) == 18, f"count={len(fixtures)}")
check("A3_fixture_ids_unique", len(ids) == len(set(ids)), "")
check("A3_fixture_ids_contiguous_D01_D18", ids == expected_ids, ",".join(ids))
check(
    "A3_fixture_ids_match_freeze_manifest",
    ids == manifest["visible_development_cases"],
    "",
)
check(
    "A3_every_fixture_has_prompt_and_criteria",
    all(f.get("prompt") and f.get("must_observe") and f.get("priority") for f in fixtures),
    "",
)

# A4 — exact v0.3 model/router blobs match freeze manifest
for comp in manifest["candidate_components"]:
    actual = blob(comp["path"])
    check(
        f'A4_blob_{comp["path"].split("/")[-1]}',
        actual == comp["git_blob_sha"],
        f'expected={comp["git_blob_sha"]} actual={actual}',
    )
for pre in manifest["preregistered_before_candidate"]:
    actual = blob(pre["path"])
    check(
        f'A4_blob_{pre["path"].split("/")[-1]}',
        actual == pre["git_blob_sha"],
        f'expected={pre["git_blob_sha"]} actual={actual}',
    )

# A5 — preregistration + transfer protocol predate implementation
def introducing_commit(path: str) -> str:
    return git("log", "--format=%H", FREEZE, "--", path).splitlines()[-1]


def commit_time(rev: str) -> int:
    return int(git("show", "-s", "--format=%ct", rev))


prereg_paths = [p["path"] for p in manifest["preregistered_before_candidate"]]
impl_paths = [c["path"] for c in manifest["candidate_components"]]
prereg_last = max(commit_time(introducing_commit(p)) for p in prereg_paths)
impl_first = min(commit_time(introducing_commit(p)) for p in impl_paths)
check(
    "A5_preregistration_and_protocol_predate_implementation",
    prereg_last < impl_first,
    f"prereg_last={prereg_last} impl_first={impl_first}",
)
for p in prereg_paths:
    c = introducing_commit(p)
    for ip in impl_paths:
        ic = introducing_commit(ip)
        anc = subprocess.run(
            ["git", "-C", REPO, "merge-base", "--is-ancestor", c, ic]
        ).returncode == 0
        check(
            f"A5_ancestry_{p.split('/')[-1]}_before_{ip.split('/')[-1]}",
            anc,
            f"{c[:8]}->{ic[:8]}",
        )

# A6 — qualified parent unchanged (blob identity + independently recomputed digest)
qp = manifest["qualified_parent"]
pm_blob = blob(f"{PARENT_DIR}/professional-model.md")
ev_blob = blob(f"{PARENT_DIR}/evidence-and-reuse.md")
check(
    "A6_parent_professional_model_blob",
    pm_blob == qp["professional_model_blob"],
    f'expected={qp["professional_model_blob"]} actual={pm_blob}',
)
canon = (
    f"{PARENT_DIR}/professional-model.md:{pm_blob}\n"
    f"{PARENT_DIR}/evidence-and-reuse.md:{ev_blob}\n"
)
recomputed = "sha256:" + hashlib.sha256(canon.encode("utf-8")).hexdigest()
check(
    "A6_parent_content_digest_recomputed",
    recomputed == qp["content_digest"],
    f'expected={qp["content_digest"]} recomputed={recomputed}',
)
parent_diff = git("diff", "--name-only", "origin/main", FREEZE, "--", PARENT_DIR)
check("A6_parent_not_mutated_vs_main", parent_diff == "", parent_diff or "no diff")
check("A6_parent_mutation_forbidden_flag", qp["mutation_allowed"] is False, "")

# A7 — v0.1 accessible baseline unchanged
base = manifest["accessible_baseline"]
base_blob = blob(base["professional_model_path"])
check(
    "A7_v01_baseline_blob_matches_freeze",
    base_blob == base["git_blob_sha"],
    f'expected={base["git_blob_sha"]} actual={base_blob}',
)
hist = git("log", "--format=%H", FREEZE, "--", base["professional_model_path"]).splitlines()
blobs_over_history = {
    git("rev-parse", f'{c}:{base["professional_model_path"]}') for c in hist
}
check(
    "A7_v01_baseline_single_immutable_blob",
    blobs_over_history == {base_blob},
    f"revisions={len(hist)} distinct_blobs={len(blobs_over_history)}",
)

# A8 — historical v0.2 identity/digest preserved and not reused
h = manifest["historical_frozen_candidate"]
check("A8_v02_digest_preserved", h["digest"] == HIST_V02_DIGEST, h["digest"])
check("A8_v02_version_recorded", h["version"] == "0.2.0-candidate", h["version"])
check(
    "A8_v02_provenance_gap_declared",
    h["source_reachable_in_current_repo"] is False
    and h["provenance_status"] == "PROVENANCE_GAP"
    and h["inheritance_claim"] == "NO_BYTE_INHERITANCE_CLAIM",
    json.dumps(h),
)
# v0.2 source genuinely unreachable across every ref
all_refs = git("rev-list", "--all").splitlines()
tree_paths: set[str] = set()
for c in all_refs:
    tree_paths.update(
        subprocess.run(
            ["git", "-C", REPO, "ls-tree", "-r", "--name-only", c],
            capture_output=True,
            text=True,
        ).stdout.splitlines()
    )
v02_artifacts = sorted(p for p in tree_paths if "0.2" in p and "motion" in p.lower())
check(
    "A8_no_v02_source_artifact_in_any_ref",
    v02_artifacts == [],
    ",".join(v02_artifacts) or "none",
)
# the candidate must not declare the 0.2 identity as its own version
skill_text = show(f"{EVDIR}/candidate-v0.3/SKILL.md")
model_text = show(f"{EVDIR}/professional-model-candidate-v0.3.md")
check(
    "A8_candidate_does_not_reuse_v02_identity",
    "version: 0.3.0-candidate" in skill_text
    and "version: 0.2.0-candidate" not in skill_text,
    "",
)
check(
    "A8_no_byte_inheritance_claim_in_candidate",
    "Do not claim byte inheritance from 0.2." in skill_text
    and "does not claim byte-for-byte inheritance from 0.2" in model_text,
    "",
)

# A9 — candidate status NOT_QUALIFIED
check("A9_manifest_verdict_not_qualified", manifest["current_verdict"] == "NOT_QUALIFIED", "")
check(
    "A9_skill_status_candidate_not_qualified",
    "status: candidate-not-qualified" in skill_text,
    "",
)
check("A9_model_status_not_qualified", "Status: CANDIDATE — NOT QUALIFIED" in model_text, "")
check(
    "A9_status_ceiling_present",
    "Never output `QUALIFIED`" in skill_text
    and "HIDDEN_TRANSFER_NOT_RUN" in json.dumps(manifest["promotion_blockers"]),
    "",
)

# A10 — frozen transfer protocol exists and contains no hidden prompts (Stage E)
proto = show(f"{EVDIR}/heldout-transfer-protocol-v0.3.md")
check(
    "A10_transfer_protocol_frozen_without_hidden_cases",
    "PREREGISTERED PROTOCOL ONLY — hidden cases do not exist yet" in proto,
    "",
)

# A11 — coupled historical cases resolvable in the frozen v0.1 fixture pack
hist_fixtures = {f["id"]: f for f in json.loads(show(f"{EVDIR}/semantic-fixtures-v0.1.json"))}
coupled = manifest["coupled_historical_cases"]
check(
    "A11_coupled_cases_exact_set",
    coupled == ["MG-S3", "MG-S4", "MG-S5", "MG-S7", "MG-S8", "MG-S9"],
    ",".join(coupled),
)
check(
    "A11_coupled_cases_resolvable",
    all(c in hist_fixtures for c in coupled),
    ",".join(sorted(hist_fixtures)),
)
check(
    "A11_uncoupled_cases_excluded",
    all(c not in coupled for c in ("MG-S1", "MG-S2", "MG-S6")),
    "",
)

failed = [c for c in checks if not c[1]]
result = {
    "stage": "A",
    "verdict": "STAGE_A_PASS" if not failed else "STATIC_CONTRACT_FAIL",
    "branch": BRANCH,
    "freeze_commit": FREEZE,
    "candidate": f'{manifest["candidate_id"]}@{manifest["candidate_version"]}',
    "checks_total": len(checks),
    "checks_failed": len(failed),
    "model_calls": 0,
    "paid_api_calls": 0,
    "checks": [{"name": n, "ok": ok, "detail": d} for n, ok, d in checks],
}
print(json.dumps(result, ensure_ascii=False, indent=2))
sys.exit(0 if not failed else 1)
