# A solar e-paper weather station

A build journal and prototype design by Acceleratu. Read the [English article](index.html) or the [Romanian article](ro.html). Both articles work directly from disk. The HTTP preview opens Markdown documents in the selected language. For the compact hardware download, open [station-project.zip](station-project.zip).

The design uses an nRF54L15 module, a 4.2-inch Waveshare e-paper panel, BME280, solar harvesting and USB-C charging. The hardware has been checked in software. Power-up, battery charging, radio range, USB plug fit and the fit of the printed enclosure still need to be tested on a prototype.

## Inside the project download

- Open `schematic/astra.sch`, `board/astra.brd` and `hardware/astra.lbr` as editable Autodesk Electronics / EAGLE sources. The PDF and assembly drawing are also included.
- `fab/` contains the manufacturing layers, drills, IPC netlist, BOM, placements, stencil geometry and test pad map. The catalog availability snapshot records the design date.
- `mechanical/` contains the populated board and assembled case in STEP, the enclosure generator, 11 printable STL files, drawings for the cut parts and the illustrated assembly guide. STEP preserves the assembly geometry. The CAD generator supplies editable dimensions and construction logic.
- `firmware/` contains the Zephyr source, host-side tests and the compiled Intel HEX. See its README for the pinned build environment.
- `docs/`, `verification/` and the project journal record engineering decisions, digital tests, exceptions and outstanding physical tests.

## Reading the evidence

The article uses the original test reports. SHA-256 values inside historical reports identify the files used for those runs. The distributed STEP headers, image/PDF metadata, drawing metadata, STL headers and Gerber export comments have been cleaned. STEP geometry and STL triangles are preserved. The USB inspection comparator uses the distributed assembly's checksum. Use the root `SHA256SUMS` to verify the download and the distributed files.

The archives contain the selected engineering deliverables. Third-party toolchains, vendor part libraries, cloud project archives, raw agent sessions and machine-specific build products are excluded. The usage table contains aggregate counts for the three hardware requests.

## Interactive explorer

Both articles include the same local viewer. Use it over HTTP. The seven schematic sheets have selectable reference designators and net labels. The PCB view combines the ten manufacturing plots with five CAD overlays. It includes a distance ruler in millimetres and component and net lookup. The 3D board includes 139 fitted components. The enclosure adds 111 named meshes and an exploded assembly, section cut and USB close-up. Rendered meshes are for inspection. The STEP assemblies and Gerber/drill exports remain the engineering files.

Open `?view=case&pose=spread#explorer` for the exploded assembly or `?view=pcb3&part=J101#explorer` for the USB connector. Use drag and pinch on touchscreens, or focus the viewport and use the arrow keys, +, − and 0. The viewer serves its own assets and Three.js. To rebuild the JavaScript, run `npm install` and `npm run build` in `explorer/`. The generator in `explorer/tools/drawings.py` takes the vector schematic PDF as its input. The public PDF is flattened. The mesh converter takes the original CAD presentation mesh manifest and the populated PCB STEP.

### Fusion workspace

The explorer opens with Fusion Electronics colours. All seven native schematic exports are registered to the interactive labels. Both standard PCB faces use the original Fusion exports. Custom layer combinations use the 37 individually exported design layers, registered on the board outline. The vector PDF and manufacturing plot views are available in the display selector.

The 3D canvas uses the saved Fusion orthographic cameras, the shaded assembly, a selectable orientation cube, grid, component browser and optional visible edges. The finished board uses meshes from the native 3D PCB, including the package bodies, plated holes, exposed lands and solder mask. Surface colours come from Fusion captures. Each projected sample is matched to the visible body and its depth. The component cameras cover the USB-C and FPC connectors, radio module, solar harvester, sensor and button. The original screenshots are available for direct comparison at full resolution. Their pixels are preserved losslessly. Browser rendering in freely chosen orientations uses WebGL.

Use `?workspace=1&view=case&camera=05-usb#explorer` to open the USB inspection camera in the full-window workspace. The local release contains all the data used by these views.
