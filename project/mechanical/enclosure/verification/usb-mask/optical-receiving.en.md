# Directional acceptance testing of the J101 mask

Release the subassembly for pressing when the inspection script returns **`release_pass = true`**. The check includes the five measured perimeters, centering, axial distance between film and metal, and the full view cone allowed by the qualified enclosure. In the release calculation, all adhesive layers are transparent. [Acceptance script](check_measured_profiles.py) · [Projection calculation](registered_optics.py) · [Qualified enclosure and PETG section](projection-datums.json)

## Measurement on an optical comparator

1. Mount J101 and the laminate in the pressing position. Record the assembly identifier, connector batch numbers, PET, adhesive, print, tool, calibrated photographs, and date. The X-axis extends from outside to PCB. The origin of the YZ coordinates in the image may be the center of the hole. The same rigid reference point must appear in all images.
2. Export five YZ contours in mm as closed point lists, ordered. `metal_bore` describes the bore through which the plug inserts, `metal_outer` denotes the outer boundary of the metal lip in its supporting plane, `pet_hole` is the skirt opening, `psa_hole` is the adhesive cutout, and `psa_outer` is the outer boundary of the adhesive with ears. Verify both sides of the PET cutout. Include in uncertainty the cut taper, burrs, interpolation error between points, and registration error between planes.
3. In `expanded_pairwise_uncertainty_mm` enter the combined uncertainty of errors between two recorded contours relative to each other at the documented coverage level. Include scale, segmentation, calibration, and positional transfer between images. If budgets are individual, combine them conservatively prior to entry. The allowed limit is 0.010 mm. A target of 0.003–0.005 mm simplifies alignment. On images after pressing, verify the final position and repeat the calculation if the film has shifted.
4. In `pet_back_to_steel_upper_mm` measure the maximum axial distance between the **back of the opaque PET layer** and the metal lip plane, including uncertainty and variation around the opening. Nominal value is 0.050 mm. Use a calibrated microscope, optical profilometer, or cross-section of an identically prepared sample that limits the measurable thickness of the layer, curl, and lot pressing variation. Measure the film lift at each piece. In examples, 0.055 mm is already an upper limit.
5. Record the CAD revision’s checksum in `case_step_sha256` on the inspection sheet. Verify that the complete rigid section at X = −8.750 mm encloses the outer trace and remains within the calibration window. On the reference part, the Y dimension is 17.120 mm. Absolute Z coordinates are −4.395 mm and +5.820 mm. The maximum deviation of each printed edge outward is 0.250 mm along the axis. The center of J101 referenced to this section's origin may vary by at most 0.350 mm along each Y and Z axis. This budget includes the optical origin from `metal_bore`. The axial distance measured between the section and the metal plane is at least 8.400 mm. Include positioning and measurement uncertainties of the enclosure within these limits. Record measurements on the lot sheet and confirm `pocket_within_projection_bounds = true` for samples that meet the criteria. The CAD identity and calibration sheet are part of the program's artifacts.

## Acceptance criteria

| Feature after allowing for measurement uncertainty | Limit |
|---|---:|
| PET window must leave the entire metal opening clear | ≥0.025 mm |
| Adhesive edge setback relative to the PET | ≥0.010 mm |
| The continuous contact width between PSA and steel | ≥0.035 mm |
| Radial eccentricity of the skirt relative to the opening | ≤0.035 mm |
| The distance between the projection of all rays admitted by the PET window and the exterior of the steel | **≥0.005 mm** |

The first three limits require the PET window to clear the bore by 0.025 mm and the steel outline to extend 0.045 mm beyond the PET window. The latter allowance combines the 0.010 mm adhesive setback and the 0.035 mm contact band. At oblique incidence, a ray may shift within the axial space between PET and metal. The final check measures this displacement in each direction.

For a ray passing through point `s` of the PETG section and point `p` of the PET opening at the back, the ray intersects the metal plane at `(1 + g/L)p − (g/L)s`. `g` is the film-to-metal distance, and `L` is the section-to-film distance, of at least `8.400 − g` mm. The program covers all directions simultaneously through the convex hull of the PET window and the four corners of the rectangle encompassing the entire rounded PETG section within the above tolerances. In the steel plane, measure the minimum distance from this projection to the actual outer contour and subtract `(1 + g/L) × U`, where `U` is the combined uncertainty. The skirt’s peripheral shield has a separation of more than 1.251 mm in the Y direction and 0.710 mm in the Z direction at the enclosure's tolerances. Internal shields J101 block sightlines passing through the functional bore. Measurements in STEP · Verification of shields J101

```sh
python check_measured_profiles.py specimen.json --suggest-recenter --output receptie.json
```

Exit code 0 means the measurement meets every limit. Code 1 preserves the report and rejection reason. If the axial distance is missing, the recess has not been verified or the enclosure revision differs, acceptance remains pending measurement or requalification. Keep the raw scans, input file and report together.

## Correction before bonding

First, use the suggested displacement on the XY stage. This refers to the registered PET and PSA assembly, viewed along the Y and Z axes of the board. Rescan **all five actual contours**, with the board secured in the new position, then rerun the control. The search grid has a resolution of 0.005 mm and suggests a position for physical verification. [Example before adjustment](examples/04-fail-before-recentering.json) · [Example after adjustment](examples/05-pass-after-recentering.json)

If achievable positions do not provide sufficient margin, order a new laminate. For workshop use, specify a cut offset **0.020 mm inward along the contour normal**, i.e., 8.64 × 2.86 mm R1.06, and initial radial centering ≤0.010 mm on the XY stage. The cut remains within the drawing tolerance zone of ±0.050 mm. The converter starts from a full sheet. A hole already too large requires a new sheet. Measure the sample again, record it on the same piece J101, and verify the plug clearance, adhesive setback and contact width according to all five criteria. [DXF optional for workshop at 1:1 scale, in mm](examples/Optional-PET-target-minus-20um.dxf)

| Synthetic example | Directional margin after uncertainty | Decision |
|---|---:|---|
| 01, center (+0.004, −0.003), PET error +0.003, `U = 0.003` | +0.00566 mm | Accepted |
| 02, centering (+0.022, −0.022), PET error +0.020, `U = 0.002` | −0.03207 mm | Failed the oblique-view test. The other four measurements passed. |
| 03, the same steel, PSA and centering as in 02, PET new at −0.020 | +0.00818 mm | Accepted. Gain of 0.04026 mm. |
| 04, before realignment | −0.00217 mm | Rejected |
| 05, after displacing the assembly by (−0.009, +0.004) mm from 04 | +0.00591 mm | Accepted in the new synthetic capture |

Example 03 maintains 0.1260 mm at the hole, 0.05199 mm from PSA, and 0.04631 mm of steel–PSA contact, after uncertainty. All examples include a maximum axial clearance of 0.055 mm. [Input 01](examples/01-pass-nonzero.json) · [Input 02](examples/02-fail-oblique.json) · [Input 03](examples/03-pass-recut-same-connector.json) · [Results and output codes for all five examples](examples/qualification-results.json)

## Testing the physical batch

The tesa datasheet features a central black PET film with acrylic adhesive on both faces. The position of the black layer and lateral optical transmission of the thin acrylic layers are verified per lot. Individually measure the opacity of the two Toray films and the tape strip on a sample. Inspect the opaque annular ring and pressure transfer around the entire perimeter. For diagnostics, the value `deepest_opaque_carrier_to_steel_upper_mm` may be introduced, representing the maximum distance from the black layer surface, toward steel, to the steel plane, including any potential air zone and uncertainty. The field is obtained by sectioning a sample under mounting pressure and optical inspection per lot. The report separately presents the hypothetical result for this opaque layer. The decision `release_pass` uses exclusively the PET–steel projection with all PSA layers transparent. [tesa 68822 datasheet](https://www.tesa.com/en/industry/tesa-68822.html)

On synthetic geometry 02, a ray passes at 0.00649 mm beyond the actual steel contour and first strikes FR4 at X = 1.47656, Y = 73.36595, Z = 0, with transparent PSA. The same ray passes through the annular material at a depth of 0.020 mm from the steel, if a physical continuous black layer exists at that location. If measurements on the lot confirm that assumption, the calculated margin for example 02 is +0.0134 mm. The mandatory check assumes transparent adhesive throughout, so this example still fails. The geometric test was performed on STEP. On the first physical item, photograph the empty port illuminated from the back under the same exposure and open reference, verify both connector orientations, and repeat the inspection after 100 cycles from the base procedure. [Ray and first body contacted in BRep](examples/native-ray.json) · [Reproduction program](examples/verify_native_witness.py) · [Inspection procedure on the first article](README.en.md)
