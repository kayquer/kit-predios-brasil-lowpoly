# CLAUDE.md

Kit of low poly 3D **Brazilian-style buildings** (CC0): houses, sobrados, apartment blocks, shops, towers, sheds,
factories, public buildings and lot details, one Blender Python script per model. Made to replace third-party
city kits in the educational game Guardião da Água with buildings that look like a Brazilian town. Blender 4.5 LTS:
"C:/Program Files/Blender Foundation/Blender 4.5/blender.exe".

## Commands

- `blender -b --factory-startup --python src/<grupo>/<id>.py` — one model → `models/<grupo>/<id>.glb` (prints `MODELO {tris, kb}`)
- `blender -b --factory-startup --python tools/medir.py -- <grupo>/<id> ...` — measures the exported `.glb` against `tools/alvos.json`
- `blender -b --factory-startup --python src/vitrine.py -- <grupo> --cada` — `previews/<grupo>.jpg` + `previews/<grupo>/<id>.jpg`
- `blender -b --factory-startup --python src/gerar_todos.py` — regenerate all + rewrite `models/catalogo.json` (never in parallel)
- `py -3 tools/atualizar_readme.py` — rebuild the catalog in the READMEs and `llms.txt` (needs `tools/nomes_en.json`)

## Conventions

- Groups (folders): residencial, comercial, industrial, publico, verde, mobiliario, carga. File id = pt-BR snake_case without accents.
- **Dimensions come from `tools/alvos.json`** (Blender units: w = X, d = Y, h = Z). w and d are hard ceilings (the
  game fits each piece inside a lot by its bounding box); h within ±15%. Model directly at that size (no
  normalization on export). Base on z = 0, centered on x/y.
- Front toward Blender **-Y**, right side (+X) finished too (the isometric camera sees -Y and +X). `lib.exportar`
  rotates 180° so the glTF front ends up at -Z.
- Budget ≤ 1,500 triangles and ≤ 150 KB per model (aim for 500–1,200 on buildings; details as written in alvos.json).
- Flat colors only, from `lib.PALETA` (Brazilian colors at the end: telha `terracota`, `tijolo_baiano`, `fibra_azul`,
  `grade`, pastel facades, `toldo_*`, `pastilha`, `granito`, `fibrocimento`...). No textures, no UVs.
- Light bevel (`chanfro` 0.01–0.03) only on main volumes; never on small details.
- Brazilian character, not generic: clay tile roofs, walls and iron gates in front of houses, window grilles, blue
  fiber water tank on roofs, exposed brick on self-built houses, pastel paint, awnings, steel roll-up shop doors,
  balconies with railings, cobogó, pastilha, fiber-cement corrugated sheds. Recognizable at small size: big shapes
  and color blocks first, details second.
- **No text, letters, numbers, logos or real brands** (signs are color bands). No people. Nothing third-party.
- First docstring sentence in pt-BR describes the model (becomes the README description).
- Never touch or push the Guardião da Água repo from kit work.

## Gotchas

- A `.glb` re-imported into Blender comes back rotated 180°.
- Previews are JPEG. To look at a render, scale it first: `ffmpeg -y -i previews/<g>/<id>.jpg -vf scale=640:-1 -q:v 8 <tmp>.jpg` (large images are blocked).
- Create scripts with Write, not a bash heredoc (an apostrophe breaks it).
- Triangle costs (lib): box 12; cylinder of n sides 4n−4; cone 2n−2; icosphere sub=1 20; ring (anel) 8n; `janelas` = n × (12 + moldura 12).
