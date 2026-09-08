from pathlib import Path

ROOT = Path(__file__).resolve().parent
MODEL = ROOT / "professional-model-candidate-v0.1.md"
SKILL = ROOT / "candidate" / "SKILL.md"
PLAN = ROOT / "qualification-plan-v0.1.md"

errors = []

for p in [MODEL, SKILL, PLAN]:
    if not p.exists():
        errors.append(f"missing:{p.name}")

if not errors:
    model = MODEL.read_text(encoding="utf-8")
    skill = SKILL.read_text(encoding="utf-8")
    plan = PLAN.read_text(encoding="utf-8")

    required_model = [
        "CANDIDATE / NOT QUALIFIED",
        "SOURCE_READY_FOR_POST",
        "actual observed source media",
        "unsafe physical instruction",
        "fabricated device capability",
        "Post-Production",
        "Live research triggers",
    ]
    for s in required_model:
        if s not in model:
            errors.append(f"model_missing:{s}")

    required_skill = [
        "candidate-not-qualified",
        "READY_TO_CAPTURE",
        "RESHOOT_REQUIRED",
        "SOURCE_READY_FOR_POST",
        "ESCALATE_SPECIALIST",
        "communication/proof intent outranks decorative cinematography",
    ]
    for s in required_skill:
        if s not in skill:
            errors.append(f"skill_missing:{s}")

    required_plan = [
        "P0 tolerance: zero",
        "real source-media practical gate",
        "never QUALIFIED",
        "NOT_EXECUTABLE",
    ]
    for s in required_plan:
        if s not in plan:
            errors.append(f"plan_missing:{s}")

if errors:
    print("STATIC_PRELIGHT_FAIL")
    for e in errors:
        print(e)
    raise SystemExit(1)

print("STATIC_PREFLIGHT_PASS")
