# Cosmos Tiles

Ready-made tile art for **Artemis Cosmos** tile maps: 3/4-view people and creatures that
face and walk in four directions, props, and ground that blends where one kind meets
another. Each pack is a media pack you pin in a mission. It contains no code.

| Pack | Set name | What is in it |
|---|---|---|
| `frontier` | `frontier` | Planet surfaces, colonies and outposts: desert, salt flats, caves, lava; prefab buildings; crew, colonists, salvagers, the Skaraan; camp and survey kit; Precursor ruins |
| `station` | `station` | Space-station and ship interiors: deck floors, bulkheads and hull, doors and hatches; the bridge, crew quarters, medbay and cryo, cargo and engineering; the crew who work there |

More packs (towns, ship exteriors...) will join. They all share one vocabulary, so
a mission can use several at once and a later pack can redraw an earlier pack's keys.

## Using a pack

1. Pin it in the mission's `story.json`, with the release tag you want:

   ```json
   "shared_media": ["artemis-sbs.Cosmos-Tiles.frontier.v0.3.0.zip",
                    "artemis-sbs.Cosmos-Tiles.station.v0.3.0.zip"]
   ```

   `sbs fetch` downloads it from this repository's releases.

2. Select the set in `settings.yaml` (or a profile):

   ```yaml
   TILE_ART: frontier, station      # later sets win key by key
   ```

3. Load the art where the mission sets up its tiles:

   ```python
   from sbs_utils.procedural.tilemap import tilemap_tileset
   from sbs_utils.procedural.tilemap_art import tilemap_art_use
   tilemap_tileset("mymap", {"dust": {"look": "dirt"},
                             "wall": {"walk": False, "look": "wall_metal"}})
   tilemap_art_use(tileset="mymap")        # the mission's builtin set, then TILE_ART
   ```

4. Name the shared keys in sprites: `Sprite: fig:skaraan_chief`, `Sprite: prop:crate`.

A mission should keep its own `builtin` set that draws every key it uses. A pack
overlays that set key by key, so the mission still plays on a machine without the
pack. See `sbs_utils/procedural/tilemap_art.py` for the manifest format.

## The vocabulary

- `fig:<model>` are people and creatures, named for what they are (`fig:junker_m`,
  `fig:skaraan_chief`, `fig:glassback`). Each has four facings (`_s _e _n _w`), each
  standing (`_idle`) and in two strides (`_a`, `_b`), plus `_down`.
- `prop:<thing>` are things that stand on a cell (`prop:crate`, `prop:hauler`,
  `prop:vault_door_open`).
- Ground looks are named for the material (`dirt`, `salt`, `water`, `floor_metal`,
  `wall_ancient`...). A map's tile kinds point at them with `look:`.

Each pack's `tileart/<set>/manifest.json` lists every key it draws.

## Releases

Each release tag carries one zip per pack, built flat by the workflow from the folders
listed in `__lib__.json`. To test a change locally, run `python sbs.pyz lib Cosmos-Tiles`
from the missions folder; it builds the same zips into `__lib__`.

The art is rendered from Synty POLYGON assets.
