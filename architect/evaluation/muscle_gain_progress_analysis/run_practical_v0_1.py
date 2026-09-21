from __future__ import annotations
import importlib.util, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PROC = ROOT / "agents" / "muscle-gain-progress-analysis" / "0.1.0" / "procedures" / "decision_reference.py"
FIXTURES = HERE / "fixtures-v0.1.json"
SKILL = ROOT / "agents" / "muscle-gain-progress-analysis" / "0.1.0" / "SKILL.md"

def load_proc():
    spec = importlib.util.spec_from_file_location("mgpa_decision_reference", PROC)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod

def main():
    mod = load_proc()
    pack = json.loads(FIXTURES.read_text(encoding="utf-8"))
    practical = []
    for item in pack["cases"]:
        got = mod.decide(item["case"])
        mod.validate_output(got)
        ok = all(got.get(k) == v for k,v in item["expect"].items())
        practical.append({"id":item["id"],"pass":ok,"got":got,"expect":item["expect"]})

    metamorphic = []
    for item in pack["metamorphic"]:
        ga, gb = mod.decide(item["a"]), mod.decide(item["b"])
        same = (ga["verdict"],ga["action"]) == (gb["verdict"],gb["action"])
        ok = same == item["same"]
        metamorphic.append({"id":item["id"],"pass":ok,"a":ga,"b":gb})

    skill = SKILL.read_text(encoding="utf-8")
    anchors = [
        "one poor session is normally weak evidence",
        "Never infer muscle or fat change from one scale point",
        "PLATEAU_SUPPORTED",
        "FALSE_PLATEAU",
        "INSUFFICIENT_DATA",
        "CONFLICTING_SIGNALS",
        "one key causal variable at a time",
        "expected effect",
        "hydration/glycogen",
        "NONCOMPARABLE",
        "medical",
        "not T1",
    ]
    static = [{"anchor":a,"pass":a.lower() in skill.lower()} for a in anchors]

    result = {
        "practical_pass":sum(x["pass"] for x in practical),
        "practical_total":len(practical),
        "metamorphic_pass":sum(x["pass"] for x in metamorphic),
        "metamorphic_total":len(metamorphic),
        "static_pass":sum(x["pass"] for x in static),
        "static_total":len(static),
        "practical":practical,
        "metamorphic":metamorphic,
        "static":static,
    }
    print(json.dumps(result,indent=2,ensure_ascii=False))
    if result["practical_pass"] != result["practical_total"]: raise SystemExit(2)
    if result["metamorphic_pass"] != result["metamorphic_total"]: raise SystemExit(3)
    if result["static_pass"] != result["static_total"]: raise SystemExit(4)

if __name__ == "__main__":
    main()
