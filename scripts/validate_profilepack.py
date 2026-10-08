#!/usr/bin/env python3
"""Validate an aitest.profilepack.v1 before it may enter schedule."""
import json, os, subprocess, sys, tempfile

def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: validate_profilepack.py <pack.json> [lstest_dir]")
    pack = json.load(open(sys.argv[1], encoding="utf-8"))
    if pack.get("schema") != "aitest.profilepack.v1":
        raise SystemExit("schema must be aitest.profilepack.v1")
    profile = pack.get("lstest_profile") or {}
    if profile.get("schema_version") != 2 or str(profile.get("contract_mode", "")).lower() != "formal":
        raise SystemExit("formal lstest profile required")
    refs = pack.get("methodology_refs") or []
    covered = {str(item.get("claim")) for item in refs if isinstance(item, dict) and item.get("refs")}
    required = (pack.get("case_contract") or {}).get("required_facts") or []
    missing = ["required_facts." + str(item) for item in required if "required_facts." + str(item) not in covered]
    for key in ((pack.get("oracle") or {}).get("thresholds") or {}):
        if "threshold." + str(key) not in covered:
            missing.append("threshold." + str(key))
    if missing:
        raise SystemExit("missing methodology_refs: " + ", ".join(missing))
    if len(sys.argv) > 2:
        lstest_dir = os.path.abspath(sys.argv[2])
        script = os.path.join(lstest_dir, "scripts", "lstest.py")
        if not os.path.isfile(script):
            raise SystemExit("lstest.py not found: " + script)
        with tempfile.TemporaryDirectory(prefix="profilepack_") as directory:
            profile_path = os.path.join(directory, "profile.json")
            with open(profile_path, "w", encoding="utf-8") as handle:
                json.dump(profile, handle, ensure_ascii=False)
            preflight = subprocess.run([sys.executable, script, "preflight", "--profile", profile_path], text=True, capture_output=True, check=False)
            if preflight.returncode != 0:
                raise SystemExit("lstest preflight failed: " + (preflight.stderr or preflight.stdout)[-1000:])
            formal = subprocess.run([sys.executable, "-c", "from scripts.profile import DeviceProfile; p=DeviceProfile.load(__import__('sys').argv[1]); p.assert_formal_ready(); print('FORMAL_FIXTURES_OK')", profile_path], cwd=lstest_dir, text=True, capture_output=True, check=False)
            if formal.returncode != 0:
                raise SystemExit("lstest formal fixture failed: " + (formal.stderr or formal.stdout)[-1000:])
    print("PROFILEPACK_VALID")

if __name__ == "__main__":
    main()
