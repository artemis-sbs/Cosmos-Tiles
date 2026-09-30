"""Refuse to release a 3D pack whose ship data points at the wrong folder.

    python .github/check_artroots.py <pack folder> <asset zip name>

A 3D pack (it has `<pack>/ships/*_ships.json`) names each piece's art by `artfileroot`,
a path relative to the engine's folder that must be exactly where THIS release unpacks:

    data/missions/__lib__/media/<asset without .zip>/ships/<key>

The asset name carries the tag, so a pack published for one tag and released under
another points every piece at a folder that does not exist - and the engine answers
that with a modal assert on the first client that draws one, not with an error. A pack
with no ships folder (a tile pack) passes untouched.
"""
import json
import os
import sys


def check(pack, asset):
    ships = os.path.join(pack, "ships")
    if not os.path.isdir(ships):
        print(f"{pack}: no ships/ - nothing to check")
        return 0
    want = "data/missions/__lib__/media/%s/ships/" % asset[:-4] if asset.endswith(".zip") \
        else "data/missions/__lib__/media/%s/ships/" % asset
    bad = 0
    files = [f for f in sorted(os.listdir(ships)) if f.endswith("_ships.json")]
    if not files:
        print(f"{pack}: ships/ has no *_ships.json")
        return 1
    for name in files:
        with open(os.path.join(ships, name), encoding="utf-8") as f:
            text = f.read()
        if not text.endswith("\n"):
            print(f"{name}: no final newline - the engine rejects the whole file")
            bad += 1
        body = json.loads("".join(l for l in text.splitlines(True)
                                  if not l.lstrip().startswith("#")))
        for e in body.get("#ship-list", []):
            root = str(e.get("artfileroot", ""))
            key = str(e.get("key", "?"))
            if root != want + key:
                print(f"{name}: {key} -> {root!r}, expected {want + key!r}")
                bad += 1
            elif not os.path.exists(os.path.join(ships, key + ".obj")):
                print(f"{name}: {key} has no {key}.obj in the pack")
                bad += 1
        print(f"{name}: {len(body.get('#ship-list', []))} entries checked")
    if bad:
        print(f"FAILED: {bad} problem(s). Re-run Cosmos-Tiles-Art/_art/publish.py "
              f"--set {os.path.basename(os.path.normpath(pack))} for this tag.")
    return 1 if bad else 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    sys.exit(check(sys.argv[1], sys.argv[2]))
