# Scene reconstruction and acceptance

Use this reference for diagrams, hybrid figures, and the final acceptance pass.

A raster image is the result of layout, fonts, shapes, data and rendering; recovering its original editable objects is not unique. Do not confuse faithful visible reconstruction with scientific re-analysis. Keep three independent dimensions in the report: visual fidelity, editable coverage, and data provenance.

## Intermediate representation

Before generating a complex figure, record a scene in the source image's pixel coordinate system: canvas size, panel regions, text, geometry, colors, connections, z-order, and raster exceptions. Preserve every panel, key label and semantic connection. Do not replace a detailed diagram with a few summary boxes unless explicitly requested. Unprocessed content is pending, not impossible. For each raster exception state whether it is an illustration, experimental image, or quantitative panel, and what is needed to replace it.

`scripts/render_scene.py scene.json output.pptx` renders a verified scene with `python-pptx` and `Pillow`. This is a rendering helper, not an image recognizer. The agent must build and check the scene from the supplied image. Schema:

```json
{"size":[1000,600],"source":"input.png","objects":[
 {"kind":"rect","box":[100,100,250,80],"fill":"E4EDF8","stroke":"334455","text":"Input","font":28},
 {"kind":"line","box":[350,140,150,0],"end":[500,140],"arrow":true,"stroke":"334455"},
 {"kind":"raster","box":[600,50,200,200],"crop":[600,50,800,250],"id":"retained-source-illustration"}
]}
```

Kinds: `text`, `rect`, `round`, `ellipse`, `line`, `raster`. `box` is x,y,width,height. Font and line width are in source pixels and scale with the canvas. `rotation` is degrees, colors are six hex digits. Source paths resolve relative to the scene file. Raster crops are embedded without being scientifically regenerated. Each object may have an `id` for later editing. The renderer emits counts, not a quality score. It does not automatically group shapes, OCR, transcribe text, reconstruct datasets or infer missing geometry. Do not call a slide made only of reference crops a reconstruction.

## Acceptance

1. Confirm every source panel appears in the manifest. Record `complete`, `partial`, `pending`, or `blocked`, the actual output files, retained raster regions, missing items and evidence for blockers. `blocked` requires a concrete failed method or missing evidence; complexity alone is not a blocker.
2. Open the actual PPTX/XLSX in a compatible application and export previews when available. A separate Python plot does not prove that an Office chart renders correctly. Compare those previews with the source for omissions, clipping, font substitution, arrow direction and semantic changes.
3. For Excel, edit a copy of an input value, recalculate, and verify linked chart/formula behavior; restore it. Error-bar ranges must reference documented uncertainty values; do not invent them. Preserve cached values by recalculating in a spreadsheet engine where possible. Mark missing recalculation/rendering explicitly.
4. For PPT, verify text, shapes and connectors are independent objects and that raster exceptions are listed. Object count alone does not prove fidelity or coverage. Never conceal source pixels as an editable reconstruction.
5. Reconcile discrepancies in author source data, filtering, sample size and plotting parameters. The author attachment can contain more records than the plot. Do not choose a convenient subset merely to match its appearance. Report this mismatch until the plotting rule is found.
6. Package runnable source, scene/config, data and provenance with the output. Do not publish user images or third-party source assets to the skill repository merely because publication of the skill is authorized.
