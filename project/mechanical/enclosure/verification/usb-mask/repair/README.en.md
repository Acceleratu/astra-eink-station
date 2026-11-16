# Mask conversion for a projecting FR4 edge

If the nominal 125 µm skirt has less than 0.020 mm clearance to the milled PCB edge, measure the position of the edge and check the apron variant before rejecting the board. In nominal assembly, the distance between FR4 and PET is 0.0525 mm. The conversion replaces the front subassembly supplied by the converter. The PET opening, position J101, steel adhesive, the two lateral guards, and the upper anchor have the same dimensions and positions. [Alternative subassembly with seven components named](Board-edge-conversion.step) · [Section and inspection of the nominal version](../README.en.md)

## Selecting the part

In board coordinates, compare the FR4 edge with the metallic face J101, X = −0.0025 mm. The surface toward the PCB side of the apron is located at X = −0.2275 mm. For a locally advanced edge reaching X = −0.2075 mm, with the top surface of FR4 at Z ≤ 0, there remains 0.020 mm until the apron. The upper 125 µm lip ends at Z = +0.080 mm and clears the PCB corner. Verify the actual edge, including solder mask or burrs, under a microscope prior to assembly. Require at least 0.020 mm on any of the three new layers and 0.05–0.40 mm from the apron face to the rigid wall of the pocket. The clearance to the wall in CAD is 0.0725 mm for the apron and 0.1725 mm for the upper skirt. Check both clearances using the board, enclosure and connector from the same unit.

JLCPCB specifies a dimensional tolerance of ±0.20 mm for milled outlines at standard accuracy. The relevant acceptance dimension here is the actual position of the edge relative to the connector after assembly. This includes the placement of the connector on the PCB. [JLCPCB capabilities for milled outlines](https://jlcpcb.com/capabilities/pcb-capabilities)

## Parts for industrial converting

In the three DXF files, (0, 0) is the center of the hole J101. The vertical coordinate of the drawing becomes Z − 1.725 mm at assembly. Each of the three pieces is delivered in register on the same support, fully pre-laminated.

| Layer | Film and position | Template and surface |
|---|---|---|
| Upper skirt | Toray #125-X30, X −0.1775…−0.0525 mm. Lower edge at Z +0.080 ±0.010 mm. | The upper contour retains opening 8.68 × 2.90 R1.08. [DXF for the upper piece](Conversion-upper-X30-125um.dxf) |
| Apron | Toray #50-X30, X −0.2775…−0.2275 mm. | Tabs extend to Z +2.225 mm; opening 8.84 × 3.06 R1.16. [Apron DXF](Conversion-apron-X30-50um.dxf) |
| Opaque connection between laminates | tesa 68822 black, 0.050 mm, X −0.2275…−0.1775 mm. | Bonded area 13.487 mm², minimum central width 0.075 mm, with wide side supports. [DXF for the opaque bond](Conversion-apron-bond-tesa-68822-50um.dxf) |

The converter prelaminates the liner-cut tesa bond onto the PCB-facing side of the apron at X −0.2275 mm, then transfers it to the visible face of the 125 µm skirt. All three layers are black. In cross-section, the apron forms a step extending outward. On the back, the standard subassembly is mounted using the adhesive from the connector's tab and the ear guards. Use a laser qualified on the same material lot and a stage with optical fiducials. Accept an additional apron-to-skirt eccentricity ≤0.020 mm radially, vertical intersection of the sheets ≥0.080 mm at the central section, and physical width ≥0.040 mm for the adhesive bond over the entire Y interval 60.40…73.60 mm. The bond must be continuous, free of voids, fiber, delamination, or breaks that penetrate the band. Measure and assess the opacity of the 50 µm sheet from this lot at the nominal threshold specified in the worksheet. Keep the part on the support until mounting onto J101.

With the board outside the enclosure, mount the entire alternative subassembly using the same mandrel, XY stage, optical comparator and force-limited press. Verify the five acceptance criteria for the mouth, including the projection of the upper PET skirt onto steel, and check the anchor. The apron maintains the nominal window of the upper skirt. [Directional acceptance](../optical-receiving.en.md) Perform the illumination test, retention test after 72 h, and mating cycles and vertical removal within the assembled enclosure. An already bonded module is fully replaced using the qualified workshop rework procedure. Pull only the supporting band, protect the J101 tongue, and inspect the metal mounting surface and solder joints prior to applying the new part. [Procedure for mounting on J101 and physical tests](../README.en.md)

## What the model verified

The verifier reads the enclosure's STEP file, virtually assembles it with the imported alternative subassembly, and checks for intersections with PCB, J101, components nearby, and the enclosure. It then tests a solid local extension of FR4 down to X −0.2075 mm and raises the three layers prismatically by 20 mm each. The front face union maintains the exact projection of the nominal skirt. At the lower edge, the volume from X −0.2775 to −0.0525, Y 60.40 to 73.60, Z 0.130 to 0.150 mm is fully occupied by black PET or black tesa. A ray passing between the two sheets intersects this band across the entire accessible external width. At the center of the opening, the apron still has 0.080 mm beyond the original PET profile. Variant verifier · [Results on STEP and templates](results.json)

On the reshaped wall of the STEP file `0ecf7606…cf062447`, the apron clearance is 0.0725 mm both in the mounted position and throughout 20 mm of withdrawal. Verification using the extended FR4 edge down to X −0.2075 mm maintained a clearance of 0.0200 mm. [Verification result on this enclosure](results.json)

Physical fit testing and film-converter qualification are still pending. This archive is for the workshop when the actual PCB edge requires conversion. The nominal parts list and production templates in `templates/` continue to describe the flat skirt.
