<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE eagle SYSTEM "eagle.dtd">
<eagle version="9.6.2">
  <drawing>
    <settings>
      <setting alwaysvectorfont="no" />
      <setting verticaltext="up" />
    </settings>
    <grid distance="0.1" unitdist="inch" unit="inch" style="lines" multiple="1" display="no" altdistance="0.01" altunitdist="inch" altunit="inch" />
    <layers>
      <layer number="1" name="Top" color="4" fill="1" visible="yes" active="yes" />
      <layer number="16" name="Bottom" color="1" fill="1" visible="yes" active="yes" />
      <layer number="17" name="Pads" color="2" fill="1" visible="yes" active="yes" />
      <layer number="18" name="Vias" color="2" fill="1" visible="yes" active="yes" />
      <layer number="19" name="Unrouted" color="6" fill="1" visible="yes" active="yes" />
      <layer number="20" name="Dimension" color="15" fill="1" visible="yes" active="yes" />
      <layer number="21" name="tPlace" color="7" fill="1" visible="yes" active="yes" />
      <layer number="22" name="bPlace" color="7" fill="1" visible="yes" active="yes" />
      <layer number="23" name="tOrigins" color="7" fill="1" visible="no" active="yes" />
      <layer number="24" name="bOrigins" color="7" fill="1" visible="no" active="yes" />
      <layer number="25" name="tNames" color="7" fill="1" visible="yes" active="yes" />
      <layer number="26" name="bNames" color="7" fill="1" visible="yes" active="yes" />
      <layer number="27" name="tValues" color="7" fill="1" visible="no" active="yes" />
      <layer number="28" name="bValues" color="7" fill="1" visible="no" active="yes" />
      <layer number="29" name="tStop" color="7" fill="1" visible="no" active="yes" />
      <layer number="30" name="bStop" color="7" fill="1" visible="no" active="yes" />
      <layer number="31" name="tCream" color="7" fill="1" visible="no" active="yes" />
      <layer number="32" name="bCream" color="7" fill="1" visible="no" active="yes" />
      <layer number="33" name="tFinish" color="7" fill="1" visible="no" active="yes" />
      <layer number="34" name="bFinish" color="7" fill="1" visible="no" active="yes" />
      <layer number="35" name="tGlue" color="7" fill="1" visible="no" active="yes" />
      <layer number="36" name="bGlue" color="7" fill="1" visible="no" active="yes" />
      <layer number="37" name="tTest" color="7" fill="1" visible="no" active="yes" />
      <layer number="38" name="bTest" color="7" fill="1" visible="no" active="yes" />
      <layer number="39" name="tKeepout" color="7" fill="1" visible="no" active="yes" />
      <layer number="40" name="bKeepout" color="7" fill="1" visible="no" active="yes" />
      <layer number="41" name="tRestrict" color="4" fill="1" visible="no" active="yes" />
      <layer number="42" name="bRestrict" color="1" fill="1" visible="no" active="yes" />
      <layer number="43" name="vRestrict" color="2" fill="1" visible="no" active="yes" />
      <layer number="44" name="Drills" color="7" fill="1" visible="no" active="yes" />
      <layer number="45" name="Holes" color="7" fill="1" visible="no" active="yes" />
      <layer number="46" name="Milling" color="7" fill="1" visible="yes" active="yes" />
      <layer number="47" name="Measures" color="7" fill="1" visible="no" active="yes" />
      <layer number="48" name="Document" color="7" fill="1" visible="no" active="yes" />
      <layer number="49" name="Reference" color="7" fill="1" visible="no" active="yes" />
      <layer number="51" name="tDocu" color="7" fill="1" visible="no" active="yes" />
      <layer number="52" name="bDocu" color="7" fill="1" visible="no" active="yes" />
      <layer number="91" name="Nets" color="2" fill="1" visible="yes" active="yes" />
      <layer number="92" name="Busses" color="1" fill="1" visible="yes" active="yes" />
      <layer number="93" name="Pins" color="2" fill="1" visible="no" active="yes" />
      <layer number="94" name="Symbols" color="4" fill="1" visible="yes" active="yes" />
      <layer number="95" name="Names" color="7" fill="1" visible="yes" active="yes" />
      <layer number="96" name="Values" color="7" fill="1" visible="yes" active="yes" />
      <layer number="97" name="Info" color="7" fill="1" visible="yes" active="yes" />
      <layer number="98" name="Guide" color="6" fill="1" visible="no" active="yes" />
    </layers>
    <schematic xreflabel="%F%N/%S.%C%R" xrefpart="/%S.%C%R">
      <libraries>
        <library name="ASTRA">
          <description>Astra e-ink weather station. Locally editable parts and land patterns.</description>
          <packages>
            <package name="ABRACON_ABS07">
              <description>Abracon ABS07 sheet p.4: 1.1 x 1.9, inside gap 1.4. Symmetric crystal.</description>
              <smd name="1" x="-1.25" y="0" dx="1.1" dy="1.9" layer="1" roundness="0" />
              <smd name="2" x="1.25" y="0" dx="1.1" dy="1.9" layer="1" roundness="0" />
              <wire x1="-1.6" y1="-0.75" x2="1.6" y2="-0.75" width="0.08" layer="51" />
              <wire x1="1.6" y1="-0.75" x2="1.6" y2="0.75" width="0.08" layer="51" />
              <wire x1="1.6" y1="0.75" x2="-1.6" y2="0.75" width="0.08" layer="51" />
              <wire x1="-1.6" y1="0.75" x2="-1.6" y2="-0.75" width="0.08" layer="51" />
            </package>
            <package name="ALPS_SKRP">
              <description>Alps SKRPABE010 product page: land bounding box 5.2 x 2.8, central gap 3.1 x 1.5. 1/2 and 3/4 internally common; press joins pairs.</description>
              <smd name="1" x="-2.075" y="1.075" dx="1.05" dy="0.65" layer="1" roundness="0" />
              <smd name="2" x="2.075" y="1.075" dx="1.05" dy="0.65" layer="1" roundness="0" />
              <smd name="3" x="-2.075" y="-1.075" dx="1.05" dy="0.65" layer="1" roundness="0" />
              <smd name="4" x="2.075" y="-1.075" dx="1.05" dy="0.65" layer="1" roundness="0" />
              <wire x1="-2.1" y1="-1.6" x2="2.1" y2="-1.6" width="0.08" layer="51" />
              <wire x1="2.1" y1="-1.6" x2="2.1" y2="1.6" width="0.08" layer="51" />
              <wire x1="2.1" y1="1.6" x2="-2.1" y2="1.6" width="0.08" layer="51" />
              <wire x1="-2.1" y1="1.6" x2="-2.1" y2="-1.6" width="0.08" layer="51" />
            </package>
            <package name="BOSCH_BME280">
              <description>Bosch BST-BME280-DS001-24 Fig. 21. Clockwise numbering in top view. Pin 1 UPPER RIGHT, next to vent.</description>
              <smd name="1" x="1.025" y="0.975" dx="0.5" dy="0.35" layer="1" roundness="0" />
              <smd name="2" x="1.025" y="0.325" dx="0.5" dy="0.35" layer="1" roundness="0" />
              <smd name="3" x="1.025" y="-0.325" dx="0.5" dy="0.35" layer="1" roundness="0" />
              <smd name="4" x="1.025" y="-0.975" dx="0.5" dy="0.35" layer="1" roundness="0" />
              <smd name="5" x="-1.025" y="-0.975" dx="0.5" dy="0.35" layer="1" roundness="0" />
              <smd name="6" x="-1.025" y="-0.325" dx="0.5" dy="0.35" layer="1" roundness="0" />
              <smd name="7" x="-1.025" y="0.325" dx="0.5" dy="0.35" layer="1" roundness="0" />
              <smd name="8" x="-1.025" y="0.975" dx="0.5" dy="0.35" layer="1" roundness="0" />
              <wire x1="-1.25" y1="-1.25" x2="1.25" y2="-1.25" width="0.08" layer="51" />
              <wire x1="1.25" y1="-1.25" x2="1.25" y2="1.25" width="0.08" layer="51" />
              <wire x1="1.25" y1="1.25" x2="-1.25" y2="1.25" width="0.08" layer="51" />
              <wire x1="-1.25" y1="1.25" x2="-1.25" y2="-1.25" width="0.08" layer="51" />
            </package>
            <package name="BOURNS_SRN3015">
              <description>Bourns SRN3015 series, recommended layout p1 rotated 90 degrees: inner gap 1.2 mm. https://www.bourns.com/docs/product-datasheets/srn3015.pdf</description>
              <smd name="1" x="-1.1" y="0" dx="1" dy="2.7" layer="1" roundness="0" />
              <smd name="2" x="1.1" y="0" dx="1" dy="2.7" layer="1" roundness="0" />
              <wire x1="-1.55" y1="-1.55" x2="1.55" y2="-1.55" width="0.08" layer="51" />
              <wire x1="1.55" y1="-1.55" x2="1.55" y2="1.55" width="0.08" layer="51" />
              <wire x1="1.55" y1="1.55" x2="-1.55" y2="1.55" width="0.08" layer="51" />
              <wire x1="-1.55" y1="1.55" x2="-1.55" y2="-1.55" width="0.08" layer="51" />
            </package>
            <package name="BSS138_CASE318">
              <description>onsemi BSS138LT1/D rev 15 case 318 issue AU land pattern (top view).</description>
              <smd name="1" x="-0.95" y="-0.975" dx="0.56" dy="0.95" layer="1" roundness="0" />
              <smd name="2" x="0.95" y="-0.975" dx="0.56" dy="0.95" layer="1" roundness="0" />
              <smd name="3" x="0" y="0.975" dx="0.56" dy="0.95" layer="1" roundness="0" />
              <wire x1="-1.45" y1="-0.65" x2="1.45" y2="-0.65" width="0.08" layer="51" />
              <wire x1="1.45" y1="-0.65" x2="1.45" y2="0.65" width="0.08" layer="51" />
              <wire x1="1.45" y1="0.65" x2="-1.45" y2="0.65" width="0.08" layer="51" />
              <wire x1="-1.45" y1="0.65" x2="-1.45" y2="-0.65" width="0.08" layer="51" />
              <circle x="-1.7" y="-1.29" radius="0.12" width="0.15" layer="21" />
            </package>
            <package name="C0402">
              <description>IPC-7351 nominal chip land dimensions checked against KiCad C0402 metric SMD library; verify part-specific body height in assembly BOM.</description>
              <smd name="1" x="-0.48" y="0" dx="0.56" dy="0.62" layer="1" roundness="50" />
              <smd name="2" x="0.48" y="0" dx="0.56" dy="0.62" layer="1" roundness="50" />
              <wire x1="-0.5" y1="-0.25" x2="0.5" y2="-0.25" width="0.08" layer="51" />
              <wire x1="0.5" y1="-0.25" x2="0.5" y2="0.25" width="0.08" layer="51" />
              <wire x1="0.5" y1="0.25" x2="-0.5" y2="0.25" width="0.08" layer="51" />
              <wire x1="-0.5" y1="0.25" x2="-0.5" y2="-0.25" width="0.08" layer="51" />
            </package>
            <package name="C0603">
              <description>IPC-7351 nominal chip land dimensions checked against KiCad C0603 metric SMD library; verify part-specific body height in assembly BOM.</description>
              <smd name="1" x="-0.775" y="0" dx="0.9" dy="0.95" layer="1" roundness="50" />
              <smd name="2" x="0.775" y="0" dx="0.9" dy="0.95" layer="1" roundness="50" />
              <wire x1="-0.8" y1="-0.4" x2="0.8" y2="-0.4" width="0.08" layer="51" />
              <wire x1="0.8" y1="-0.4" x2="0.8" y2="0.4" width="0.08" layer="51" />
              <wire x1="0.8" y1="0.4" x2="-0.8" y2="0.4" width="0.08" layer="51" />
              <wire x1="-0.8" y1="0.4" x2="-0.8" y2="-0.4" width="0.08" layer="51" />
            </package>
            <package name="C0805">
              <description>IPC-7351 nominal chip land dimensions checked against KiCad C0805 metric SMD library; verify part-specific body height in assembly BOM.</description>
              <smd name="1" x="-0.95" y="0" dx="1" dy="1.45" layer="1" roundness="50" />
              <smd name="2" x="0.95" y="0" dx="1" dy="1.45" layer="1" roundness="50" />
              <wire x1="-1" y1="-0.625" x2="1" y2="-0.625" width="0.08" layer="51" />
              <wire x1="1" y1="-0.625" x2="1" y2="0.625" width="0.08" layer="51" />
              <wire x1="1" y1="0.625" x2="-1" y2="0.625" width="0.08" layer="51" />
              <wire x1="-1" y1="0.625" x2="-1" y2="-0.625" width="0.08" layer="51" />
            </package>
            <package name="C1206P">
              <description>Murata GRM31 through 3216 M metric, land pattern for reflow. 1.65 mm inner gap with 1.25 mm opposing lands.</description>
              <smd name="1" x="-1.45" y="0" dx="1.25" dy="1.75" layer="1" roundness="25" />
              <smd name="2" x="1.45" y="0" dx="1.25" dy="1.75" layer="1" roundness="25" />
              <wire x1="-1.6" y1="-0.8" x2="1.6" y2="-0.8" width="0.08" layer="51" />
              <wire x1="1.6" y1="-0.8" x2="1.6" y2="0.8" width="0.08" layer="51" />
              <wire x1="1.6" y1="0.8" x2="-1.6" y2="0.8" width="0.08" layer="51" />
              <wire x1="-1.6" y1="0.8" x2="-1.6" y2="-0.8" width="0.08" layer="51" />
            </package>
            <package name="COIL_XGL4015">
              <description>Coilcraft XGL4015 document 1660-3, recommended land pattern. https://www.coilcraft.com/getmedia/c5d04454-742d-473e-8b80-06c97338c587/xgl4015.pdf</description>
              <smd name="1" x="-1.185" y="0" dx="0.98" dy="3.4" layer="1" roundness="0" />
              <smd name="2" x="1.185" y="0" dx="0.98" dy="3.4" layer="1" roundness="0" />
              <wire x1="-2.15" y1="-2.15" x2="2.15" y2="-2.15" width="0.08" layer="51" />
              <wire x1="2.15" y1="-2.15" x2="2.15" y2="2.15" width="0.08" layer="51" />
              <wire x1="2.15" y1="2.15" x2="-2.15" y2="2.15" width="0.08" layer="51" />
              <wire x1="-2.15" y1="2.15" x2="-2.15" y2="-2.15" width="0.08" layer="51" />
            </package>
            <package name="EBYTE_08S1F_LGA40">
              <description>Ebyte orderable drawing §3.1 + original Altium E73-2G4M08S1F.PcbLib. Peripheral land centers and all land sizes use manufacturer CAD. Central lands 37–40 indexed from dimensioned package drawing; see verification/radio/pad-verification.json.</description>
              <smd name="1" x="-5.15" y="2.55" dx="1" dy="1" layer="1" roundness="0" />
              <smd name="2" x="-5.15" y="1.25" dx="1" dy="0.6" layer="1" roundness="100" />
              <smd name="3" x="-5.15" y="0.15" dx="1" dy="0.6" layer="1" roundness="100" />
              <smd name="4" x="-5.15" y="-0.95" dx="1" dy="0.6" layer="1" roundness="100" />
              <smd name="5" x="-5.15" y="-2.05" dx="1" dy="0.6" layer="1" roundness="100" />
              <smd name="6" x="-5.15" y="-3.15" dx="1" dy="0.6" layer="1" roundness="100" />
              <smd name="7" x="-5.15" y="-4.25" dx="1" dy="0.6" layer="1" roundness="100" />
              <smd name="8" x="-5.15" y="-5.35" dx="1" dy="0.6" layer="1" roundness="100" />
              <smd name="9" x="-5.15" y="-6.45" dx="1" dy="0.6" layer="1" roundness="100" />
              <smd name="10" x="-5.15" y="-7.75" dx="1" dy="1" layer="1" roundness="100" />
              <smd name="11" x="-3.85" y="-7.75" dx="0.6" dy="1" layer="1" roundness="100" />
              <smd name="12" x="-2.75" y="-7.75" dx="0.6" dy="1" layer="1" roundness="100" />
              <smd name="13" x="-1.65" y="-7.75" dx="0.6" dy="1" layer="1" roundness="100" />
              <smd name="14" x="-0.55" y="-7.75" dx="0.6" dy="1" layer="1" roundness="100" />
              <smd name="15" x="0.55" y="-7.75" dx="0.6" dy="1" layer="1" roundness="100" />
              <smd name="16" x="1.65" y="-7.75" dx="0.6" dy="1" layer="1" roundness="100" />
              <smd name="17" x="2.75" y="-7.75" dx="0.6" dy="1" layer="1" roundness="100" />
              <smd name="18" x="3.85" y="-7.75" dx="0.6" dy="1" layer="1" roundness="100" />
              <smd name="19" x="5.15" y="-7.75" dx="1" dy="1" layer="1" roundness="100" />
              <smd name="20" x="5.15" y="-6.45" dx="1" dy="0.6" layer="1" roundness="100" />
              <smd name="21" x="5.15" y="-5.35" dx="1" dy="0.6" layer="1" roundness="100" />
              <smd name="22" x="5.15" y="-4.25" dx="1" dy="0.6" layer="1" roundness="100" />
              <smd name="23" x="5.15" y="-3.15" dx="1" dy="0.6" layer="1" roundness="100" />
              <smd name="24" x="5.15" y="-2.05" dx="1" dy="0.6" layer="1" roundness="100" />
              <smd name="25" x="5.15" y="-0.95" dx="1" dy="0.6" layer="1" roundness="100" />
              <smd name="26" x="5.15" y="0.15" dx="1" dy="0.6" layer="1" roundness="100" />
              <smd name="27" x="5.15" y="1.25" dx="1" dy="0.6" layer="1" roundness="100" />
              <smd name="28" x="5.15" y="2.55" dx="1" dy="1" layer="1" roundness="100" />
              <smd name="29" x="3.85" y="2.55" dx="0.6" dy="1" layer="1" roundness="100" />
              <smd name="30" x="2.75" y="2.55" dx="0.6" dy="1" layer="1" roundness="100" />
              <smd name="31" x="1.65" y="2.55" dx="0.6" dy="1" layer="1" roundness="100" />
              <smd name="32" x="0.55" y="2.55" dx="0.6" dy="1" layer="1" roundness="100" />
              <smd name="33" x="-0.55" y="2.55" dx="0.6" dy="1" layer="1" roundness="100" />
              <smd name="34" x="-1.65" y="2.55" dx="0.6" dy="1" layer="1" roundness="100" />
              <smd name="35" x="-2.75" y="2.55" dx="0.6" dy="1" layer="1" roundness="100" />
              <smd name="36" x="-3.85" y="2.55" dx="0.6" dy="1" layer="1" roundness="100" />
              <smd name="37" x="-0.675" y="-1.725" dx="1.2" dy="1.2" layer="1" roundness="100" />
              <smd name="38" x="-0.675" y="-3.125" dx="1.2" dy="1.2" layer="1" roundness="100" />
              <smd name="39" x="0.725" y="-3.125" dx="1.2" dy="1.2" layer="1" roundness="100" />
              <smd name="40" x="0.725" y="-1.725" dx="1.2" dy="1.2" layer="1" roundness="100" />
              <wire x1="-6" y1="-8.6" x2="6" y2="-8.6" width="0.08" layer="51" />
              <wire x1="6" y1="-8.6" x2="6" y2="8.6" width="0.08" layer="51" />
              <wire x1="6" y1="8.6" x2="-6" y2="8.6" width="0.08" layer="51" />
              <wire x1="-6" y1="8.6" x2="-6" y2="-8.6" width="0.08" layer="51" />
            </package>
            <package name="EPD_C1206">
              <description>3216 metric MLCC symmetric land adapted from IPC-7351 nominal and Samsung CL31B105KCHNNN body/termination dimensions.</description>
              <smd name="1" x="-1.4" y="0" dx="1.1" dy="1.8" layer="1" roundness="30" />
              <smd name="2" x="1.4" y="0" dx="1.1" dy="1.8" layer="1" roundness="30" />
              <wire x1="-1.6" y1="-0.8" x2="1.6" y2="-0.8" width="0.08" layer="51" />
              <wire x1="1.6" y1="-0.8" x2="1.6" y2="0.8" width="0.08" layer="51" />
              <wire x1="1.6" y1="0.8" x2="-1.6" y2="0.8" width="0.08" layer="51" />
              <wire x1="-1.6" y1="0.8" x2="-1.6" y2="-0.8" width="0.08" layer="51" />
            </package>
            <package name="EPD_C1210">
              <description>3216/3225 metric MLCC IPC nominal toe/heel, symmetric, Samsung CL32B475KBJNNN 3.20 × 2.50 × 2.70 mm nominal.</description>
              <smd name="1" x="-1.5" y="0" dx="1.3" dy="2.7" layer="1" roundness="30" />
              <smd name="2" x="1.5" y="0" dx="1.3" dy="2.7" layer="1" roundness="30" />
              <wire x1="-1.6" y1="-1.25" x2="1.6" y2="-1.25" width="0.08" layer="51" />
              <wire x1="1.6" y1="-1.25" x2="1.6" y2="1.25" width="0.08" layer="51" />
              <wire x1="1.6" y1="1.25" x2="-1.6" y2="1.25" width="0.08" layer="51" />
              <wire x1="-1.6" y1="1.25" x2="-1.6" y2="-1.25" width="0.08" layer="51" />
            </package>
            <package name="FH12_24S_05SH">
              <description>Hirose FH12 catalogue (drawing p4/lands p11, 24-way row A11.5/B17.1/C13.5). Pin 1 left with entry south. Body is plastic section; anchoring tabs extend to 16.1 mm overall.</description>
              <polygon width="0" layer="31">
                <vertex x="-5.875" y="2.8" />
                <vertex x="-5.625" y="2.8" />
                <vertex x="-5.625" y="4.1" />
                <vertex x="-5.875" y="4.1" />
              </polygon>
              <smd name="1" x="-5.75" y="3.45" cream="no" dx="0.3" dy="1.3" layer="1" roundness="0" />
              <polygon width="0" layer="31">
                <vertex x="-5.375" y="2.8" />
                <vertex x="-5.125" y="2.8" />
                <vertex x="-5.125" y="4.1" />
                <vertex x="-5.375" y="4.1" />
              </polygon>
              <smd name="2" x="-5.25" y="3.45" cream="no" dx="0.3" dy="1.3" layer="1" roundness="0" />
              <polygon width="0" layer="31">
                <vertex x="-4.875" y="2.8" />
                <vertex x="-4.625" y="2.8" />
                <vertex x="-4.625" y="4.1" />
                <vertex x="-4.875" y="4.1" />
              </polygon>
              <smd name="3" x="-4.75" y="3.45" cream="no" dx="0.3" dy="1.3" layer="1" roundness="0" />
              <polygon width="0" layer="31">
                <vertex x="-4.375" y="2.8" />
                <vertex x="-4.125" y="2.8" />
                <vertex x="-4.125" y="4.1" />
                <vertex x="-4.375" y="4.1" />
              </polygon>
              <smd name="4" x="-4.25" y="3.45" cream="no" dx="0.3" dy="1.3" layer="1" roundness="0" />
              <polygon width="0" layer="31">
                <vertex x="-3.875" y="2.8" />
                <vertex x="-3.625" y="2.8" />
                <vertex x="-3.625" y="4.1" />
                <vertex x="-3.875" y="4.1" />
              </polygon>
              <smd name="5" x="-3.75" y="3.45" cream="no" dx="0.3" dy="1.3" layer="1" roundness="0" />
              <polygon width="0" layer="31">
                <vertex x="-3.375" y="2.8" />
                <vertex x="-3.125" y="2.8" />
                <vertex x="-3.125" y="4.1" />
                <vertex x="-3.375" y="4.1" />
              </polygon>
              <smd name="6" x="-3.25" y="3.45" cream="no" dx="0.3" dy="1.3" layer="1" roundness="0" />
              <polygon width="0" layer="31">
                <vertex x="-2.875" y="2.8" />
                <vertex x="-2.625" y="2.8" />
                <vertex x="-2.625" y="4.1" />
                <vertex x="-2.875" y="4.1" />
              </polygon>
              <smd name="7" x="-2.75" y="3.45" cream="no" dx="0.3" dy="1.3" layer="1" roundness="0" />
              <polygon width="0" layer="31">
                <vertex x="-2.375" y="2.8" />
                <vertex x="-2.125" y="2.8" />
                <vertex x="-2.125" y="4.1" />
                <vertex x="-2.375" y="4.1" />
              </polygon>
              <smd name="8" x="-2.25" y="3.45" cream="no" dx="0.3" dy="1.3" layer="1" roundness="0" />
              <polygon width="0" layer="31">
                <vertex x="-1.875" y="2.8" />
                <vertex x="-1.625" y="2.8" />
                <vertex x="-1.625" y="4.1" />
                <vertex x="-1.875" y="4.1" />
              </polygon>
              <smd name="9" x="-1.75" y="3.45" cream="no" dx="0.3" dy="1.3" layer="1" roundness="0" />
              <polygon width="0" layer="31">
                <vertex x="-1.375" y="2.8" />
                <vertex x="-1.125" y="2.8" />
                <vertex x="-1.125" y="4.1" />
                <vertex x="-1.375" y="4.1" />
              </polygon>
              <smd name="10" x="-1.25" y="3.45" cream="no" dx="0.3" dy="1.3" layer="1" roundness="0" />
              <polygon width="0" layer="31">
                <vertex x="-0.875" y="2.8" />
                <vertex x="-0.625" y="2.8" />
                <vertex x="-0.625" y="4.1" />
                <vertex x="-0.875" y="4.1" />
              </polygon>
              <smd name="11" x="-0.75" y="3.45" cream="no" dx="0.3" dy="1.3" layer="1" roundness="0" />
              <polygon width="0" layer="31">
                <vertex x="-0.375" y="2.8" />
                <vertex x="-0.125" y="2.8" />
                <vertex x="-0.125" y="4.1" />
                <vertex x="-0.375" y="4.1" />
              </polygon>
              <smd name="12" x="-0.25" y="3.45" cream="no" dx="0.3" dy="1.3" layer="1" roundness="0" />
              <polygon width="0" layer="31">
                <vertex x="0.125" y="2.8" />
                <vertex x="0.375" y="2.8" />
                <vertex x="0.375" y="4.1" />
                <vertex x="0.125" y="4.1" />
              </polygon>
              <smd name="13" x="0.25" y="3.45" cream="no" dx="0.3" dy="1.3" layer="1" roundness="0" />
              <polygon width="0" layer="31">
                <vertex x="0.625" y="2.8" />
                <vertex x="0.875" y="2.8" />
                <vertex x="0.875" y="4.1" />
                <vertex x="0.625" y="4.1" />
              </polygon>
              <smd name="14" x="0.75" y="3.45" cream="no" dx="0.3" dy="1.3" layer="1" roundness="0" />
              <polygon width="0" layer="31">
                <vertex x="1.125" y="2.8" />
                <vertex x="1.375" y="2.8" />
                <vertex x="1.375" y="4.1" />
                <vertex x="1.125" y="4.1" />
              </polygon>
              <smd name="15" x="1.25" y="3.45" cream="no" dx="0.3" dy="1.3" layer="1" roundness="0" />
              <polygon width="0" layer="31">
                <vertex x="1.625" y="2.8" />
                <vertex x="1.875" y="2.8" />
                <vertex x="1.875" y="4.1" />
                <vertex x="1.625" y="4.1" />
              </polygon>
              <smd name="16" x="1.75" y="3.45" cream="no" dx="0.3" dy="1.3" layer="1" roundness="0" />
              <polygon width="0" layer="31">
                <vertex x="2.125" y="2.8" />
                <vertex x="2.375" y="2.8" />
                <vertex x="2.375" y="4.1" />
                <vertex x="2.125" y="4.1" />
              </polygon>
              <smd name="17" x="2.25" y="3.45" cream="no" dx="0.3" dy="1.3" layer="1" roundness="0" />
              <polygon width="0" layer="31">
                <vertex x="2.625" y="2.8" />
                <vertex x="2.875" y="2.8" />
                <vertex x="2.875" y="4.1" />
                <vertex x="2.625" y="4.1" />
              </polygon>
              <smd name="18" x="2.75" y="3.45" cream="no" dx="0.3" dy="1.3" layer="1" roundness="0" />
              <polygon width="0" layer="31">
                <vertex x="3.125" y="2.8" />
                <vertex x="3.375" y="2.8" />
                <vertex x="3.375" y="4.1" />
                <vertex x="3.125" y="4.1" />
              </polygon>
              <smd name="19" x="3.25" y="3.45" cream="no" dx="0.3" dy="1.3" layer="1" roundness="0" />
              <polygon width="0" layer="31">
                <vertex x="3.625" y="2.8" />
                <vertex x="3.875" y="2.8" />
                <vertex x="3.875" y="4.1" />
                <vertex x="3.625" y="4.1" />
              </polygon>
              <smd name="20" x="3.75" y="3.45" cream="no" dx="0.3" dy="1.3" layer="1" roundness="0" />
              <polygon width="0" layer="31">
                <vertex x="4.125" y="2.8" />
                <vertex x="4.375" y="2.8" />
                <vertex x="4.375" y="4.1" />
                <vertex x="4.125" y="4.1" />
              </polygon>
              <smd name="21" x="4.25" y="3.45" cream="no" dx="0.3" dy="1.3" layer="1" roundness="0" />
              <polygon width="0" layer="31">
                <vertex x="4.625" y="2.8" />
                <vertex x="4.875" y="2.8" />
                <vertex x="4.875" y="4.1" />
                <vertex x="4.625" y="4.1" />
              </polygon>
              <smd name="22" x="4.75" y="3.45" cream="no" dx="0.3" dy="1.3" layer="1" roundness="0" />
              <polygon width="0" layer="31">
                <vertex x="5.125" y="2.8" />
                <vertex x="5.375" y="2.8" />
                <vertex x="5.375" y="4.1" />
                <vertex x="5.125" y="4.1" />
              </polygon>
              <smd name="23" x="5.25" y="3.45" cream="no" dx="0.3" dy="1.3" layer="1" roundness="0" />
              <polygon width="0" layer="31">
                <vertex x="5.625" y="2.8" />
                <vertex x="5.875" y="2.8" />
                <vertex x="5.875" y="4.1" />
                <vertex x="5.625" y="4.1" />
              </polygon>
              <smd name="24" x="5.75" y="3.45" cream="no" dx="0.3" dy="1.3" layer="1" roundness="0" />
              <smd name="MP1" x="-7.65" y="0.2" dx="1.8" dy="2.2" layer="1" roundness="0" />
              <smd name="MP2" x="7.65" y="0.2" dx="1.8" dy="2.2" layer="1" roundness="0" />
              <wire x1="-7.55" y1="-2.8" x2="7.55" y2="-2.8" width="0.08" layer="51" />
              <wire x1="7.55" y1="-2.8" x2="7.55" y2="2.8" width="0.08" layer="51" />
              <wire x1="7.55" y1="2.8" x2="-7.55" y2="2.8" width="0.08" layer="51" />
              <wire x1="-7.55" y1="2.8" x2="-7.55" y2="-2.8" width="0.08" layer="51" />
              <wire x1="-6.25" y1="-2.8" x2="6.25" y2="-2.8" width="0.1" layer="51" />
              <circle x="-6.55" y="3.45" radius="0.14" width="0.15" layer="21" />
            </package>
            <package name="GCT_USB4135">
              <description>GCT USB4135 drawing rev A2, top-side Recommended PCB Layout. Origin on nominal case center; mating face y=-3.45 mm. Shell terminals outside case width. Worst-case mechanical envelope 3.35 mm. https://gct.co/files/drawings/usb4135.pdf</description>
              <smd name="B12" x="-2.75" y="3.03" dx="0.8" dy="1.2" layer="1" roundness="0" />
              <smd name="B9" x="-1.52" y="3.03" dx="0.76" dy="1.2" layer="1" roundness="0" />
              <smd name="A5" x="-0.5" y="3.03" dx="0.7" dy="1.2" layer="1" roundness="0" />
              <smd name="B5" x="0.5" y="3.03" dx="0.7" dy="1.2" layer="1" roundness="0" />
              <smd name="A9" x="1.52" y="3.03" dx="0.76" dy="1.2" layer="1" roundness="0" />
              <smd name="A12" x="2.75" y="3.03" dx="0.8" dy="1.2" layer="1" roundness="0" />
              <smd name="SH1" x="-5.125" y="2.98" dx="1.8" dy="1.35" layer="1" roundness="0" />
              <smd name="SH2" x="5.125" y="2.98" dx="1.8" dy="1.35" layer="1" roundness="0" />
              <smd name="SH3" x="-5.125" y="-0.6" dx="1.8" dy="1.5" layer="1" roundness="0" />
              <smd name="SH4" x="5.125" y="-0.6" dx="1.8" dy="1.5" layer="1" roundness="0" />
              <wire x1="-4.47" y1="-3.45" x2="4.47" y2="-3.45" width="0.08" layer="51" />
              <wire x1="4.47" y1="-3.45" x2="4.47" y2="3.45" width="0.08" layer="51" />
              <wire x1="4.47" y1="3.45" x2="-4.47" y2="3.45" width="0.08" layer="51" />
              <wire x1="-4.47" y1="3.45" x2="-4.47" y2="-3.45" width="0.08" layer="51" />
            </package>
            <package name="JST_ACH03P_POWER">
              <description>JST ACH connector component-side PCB layout. Top-entry latch, wires exit local -X. Topmost contact in vendor orientation is #1. https://www.jst.com/wp-content/uploads/2021/01/eACH-new.pdf</description>
              <smd name="1" x="2.025" y="1.2" dx="0.85" dy="0.6" layer="1" roundness="0" />
              <smd name="2" x="2.025" y="0" dx="0.85" dy="0.6" layer="1" roundness="0" />
              <smd name="3" x="2.025" y="-1.2" dx="0.85" dy="0.6" layer="1" roundness="0" />
              <smd name="M1" x="-1.75" y="2.35" dx="0.8" dy="0.7" layer="1" roundness="0" />
              <smd name="M2" x="-1.75" y="-2.35" dx="0.8" dy="0.7" layer="1" roundness="0" />
              <wire x1="-2.15" y1="-2.7" x2="2.15" y2="-2.7" width="0.08" layer="51" />
              <wire x1="2.15" y1="-2.7" x2="2.15" y2="2.7" width="0.08" layer="51" />
              <wire x1="2.15" y1="2.7" x2="-2.15" y2="2.7" width="0.08" layer="51" />
              <wire x1="-2.15" y1="2.7" x2="-2.15" y2="-2.7" width="0.08" layer="51" />
            </package>
            <package name="MBR0530_CASE425">
              <description>onsemi MBR0530T1/D rev 9 case 425 issue H 98ASB42927B; banded cathode on pad 1.</description>
              <smd name="1" x="-1.635" y="0" dx="0.91" dy="1.22" layer="1" roundness="0" />
              <smd name="2" x="1.635" y="0" dx="0.91" dy="1.22" layer="1" roundness="0" />
              <wire x1="-1.345" y1="-0.8" x2="1.345" y2="-0.8" width="0.08" layer="51" />
              <wire x1="1.345" y1="-0.8" x2="1.345" y2="0.8" width="0.08" layer="51" />
              <wire x1="1.345" y1="0.8" x2="-1.345" y2="0.8" width="0.08" layer="51" />
              <wire x1="-1.345" y1="0.8" x2="-1.345" y2="-0.8" width="0.08" layer="51" />
              <wire x1="-2.48" y1="-0.57" x2="-2.48" y2="0.57" width="0.17" layer="21" />
            </package>
            <package name="MC_MSOP8_TEMP">
              <description>Microchip MSOP 3x3, C04-2111-MS rev E. Pin1 top left. https://ww1.microchip.com/downloads/aemDocuments/documents/product-documents/package-drawings/08L-MSOP-3x3-MS-C04-00111e.pdf</description>
              <smd name="1" x="-2.2" y="0.975" dx="1.45" dy="0.45" layer="1" roundness="0" />
              <smd name="2" x="-2.2" y="0.325" dx="1.45" dy="0.45" layer="1" roundness="0" />
              <smd name="3" x="-2.2" y="-0.325" dx="1.45" dy="0.45" layer="1" roundness="0" />
              <smd name="4" x="-2.2" y="-0.975" dx="1.45" dy="0.45" layer="1" roundness="0" />
              <smd name="5" x="2.2" y="-0.975" dx="1.45" dy="0.45" layer="1" roundness="0" />
              <smd name="6" x="2.2" y="-0.325" dx="1.45" dy="0.45" layer="1" roundness="0" />
              <smd name="7" x="2.2" y="0.325" dx="1.45" dy="0.45" layer="1" roundness="0" />
              <smd name="8" x="2.2" y="0.975" dx="1.45" dy="0.45" layer="1" roundness="0" />
              <wire x1="-1.5" y1="-1.5" x2="1.5" y2="-1.5" width="0.08" layer="51" />
              <wire x1="1.5" y1="-1.5" x2="1.5" y2="1.5" width="0.08" layer="51" />
              <wire x1="1.5" y1="1.5" x2="-1.5" y2="1.5" width="0.08" layer="51" />
              <wire x1="-1.5" y1="1.5" x2="-1.5" y2="-1.5" width="0.08" layer="51" />
            </package>
            <package name="NXP_CFP3_DIODE">
              <description>Nexperia PMEG2010ER/CFP3 SOD123W reflow land figure; cathode terminal 1. https://assets.nexperia.com/documents/data-sheet/PMEG2010ER.pdf</description>
              <polygon width="0" layer="31">
                <vertex x="-1.95" y="-0.55" />
                <vertex x="-0.85" y="-0.55" />
                <vertex x="-0.85" y="0.55" />
                <vertex x="-1.95" y="0.55" />
              </polygon>
              <smd name="1" x="-1.4" y="0" cream="no" dx="1.2" dy="1.2" layer="1" roundness="0" />
              <polygon width="0" layer="31">
                <vertex x="0.85" y="-0.55" />
                <vertex x="1.95" y="-0.55" />
                <vertex x="1.95" y="0.55" />
                <vertex x="0.85" y="0.55" />
              </polygon>
              <smd name="2" x="1.4" y="0" cream="no" dx="1.2" dy="1.2" layer="1" roundness="0" />
              <wire x1="-1.35" y1="-0.85" x2="1.35" y2="-0.85" width="0.08" layer="51" />
              <wire x1="1.35" y1="-0.85" x2="1.35" y2="0.85" width="0.08" layer="51" />
              <wire x1="1.35" y1="0.85" x2="-1.35" y2="0.85" width="0.08" layer="51" />
              <wire x1="-1.35" y1="0.85" x2="-1.35" y2="-0.85" width="0.08" layer="51" />
            </package>
            <package name="NXP_SO8_RTC">
              <description>NXP SOT96-1 / Nexperia SOT96-1, Fig 2. Land toe span 6.60 mm, heel gap 4.00 mm.</description>
              <smd name="1" x="-2.65" y="1.905" dx="1.3" dy="0.6" layer="1" roundness="0" />
              <smd name="2" x="-2.65" y="0.635" dx="1.3" dy="0.6" layer="1" roundness="0" />
              <smd name="3" x="-2.65" y="-0.635" dx="1.3" dy="0.6" layer="1" roundness="0" />
              <smd name="4" x="-2.65" y="-1.905" dx="1.3" dy="0.6" layer="1" roundness="0" />
              <smd name="5" x="2.65" y="-1.905" dx="1.3" dy="0.6" layer="1" roundness="0" />
              <smd name="6" x="2.65" y="-0.635" dx="1.3" dy="0.6" layer="1" roundness="0" />
              <smd name="7" x="2.65" y="0.635" dx="1.3" dy="0.6" layer="1" roundness="0" />
              <smd name="8" x="2.65" y="1.905" dx="1.3" dy="0.6" layer="1" roundness="0" />
              <wire x1="-1.95" y1="-2.45" x2="1.95" y2="-2.45" width="0.08" layer="51" />
              <wire x1="1.95" y1="-2.45" x2="1.95" y2="2.45" width="0.08" layer="51" />
              <wire x1="1.95" y1="2.45" x2="-1.95" y2="2.45" width="0.08" layer="51" />
              <wire x1="-1.95" y1="2.45" x2="-1.95" y2="-2.45" width="0.08" layer="51" />
            </package>
            <package name="NXP_SOT23_DIODE">
              <description>Nexperia BAT54C, SOT23 / TO-236AB package, top view left/right anodes pin1/pin2, opposite common cathode pin3. https://assets.nexperia.com/documents/data-sheet/BAT54C.pdf</description>
              <smd name="1" x="-0.95" y="-1" dx="0.7" dy="1.05" layer="1" roundness="0" />
              <smd name="2" x="0.95" y="-1" dx="0.7" dy="1.05" layer="1" roundness="0" />
              <smd name="3" x="0" y="1" dx="0.7" dy="1.05" layer="1" roundness="0" />
              <wire x1="-1.475" y1="-0.825" x2="1.475" y2="-0.825" width="0.08" layer="51" />
              <wire x1="1.475" y1="-0.825" x2="1.475" y2="0.825" width="0.08" layer="51" />
              <wire x1="1.475" y1="0.825" x2="-1.475" y2="0.825" width="0.08" layer="51" />
              <wire x1="-1.475" y1="0.825" x2="-1.475" y2="-0.825" width="0.08" layer="51" />
            </package>
            <package name="NXP_TSSOP16_MONO">
              <description>Nexperia SOT403-1 Fig.2, copper toe span 7.20, heel gap 4.50, land length 1.35, width 0.40.</description>
              <smd name="1" x="-2.925" y="2.275" dx="1.35" dy="0.4" layer="1" roundness="0" />
              <smd name="2" x="-2.925" y="1.625" dx="1.35" dy="0.4" layer="1" roundness="0" />
              <smd name="3" x="-2.925" y="0.975" dx="1.35" dy="0.4" layer="1" roundness="0" />
              <smd name="4" x="-2.925" y="0.325" dx="1.35" dy="0.4" layer="1" roundness="0" />
              <smd name="5" x="-2.925" y="-0.325" dx="1.35" dy="0.4" layer="1" roundness="0" />
              <smd name="6" x="-2.925" y="-0.975" dx="1.35" dy="0.4" layer="1" roundness="0" />
              <smd name="7" x="-2.925" y="-1.625" dx="1.35" dy="0.4" layer="1" roundness="0" />
              <smd name="8" x="-2.925" y="-2.275" dx="1.35" dy="0.4" layer="1" roundness="0" />
              <smd name="9" x="2.925" y="-2.275" dx="1.35" dy="0.4" layer="1" roundness="0" />
              <smd name="10" x="2.925" y="-1.625" dx="1.35" dy="0.4" layer="1" roundness="0" />
              <smd name="11" x="2.925" y="-0.975" dx="1.35" dy="0.4" layer="1" roundness="0" />
              <smd name="12" x="2.925" y="-0.325" dx="1.35" dy="0.4" layer="1" roundness="0" />
              <smd name="13" x="2.925" y="0.325" dx="1.35" dy="0.4" layer="1" roundness="0" />
              <smd name="14" x="2.925" y="0.975" dx="1.35" dy="0.4" layer="1" roundness="0" />
              <smd name="15" x="2.925" y="1.625" dx="1.35" dy="0.4" layer="1" roundness="0" />
              <smd name="16" x="2.925" y="2.275" dx="1.35" dy="0.4" layer="1" roundness="0" />
              <wire x1="-2.2" y1="-2.5" x2="2.2" y2="-2.5" width="0.08" layer="51" />
              <wire x1="2.2" y1="-2.5" x2="2.2" y2="2.5" width="0.08" layer="51" />
              <wire x1="2.2" y1="2.5" x2="-2.2" y2="2.5" width="0.08" layer="51" />
              <wire x1="-2.2" y1="2.5" x2="-2.2" y2="-2.5" width="0.08" layer="51" />
            </package>
            <package name="PV_WIRE_PAIR">
              <description>Custom paired hand-solder lands for panel wire and return. Positive land 1. Provide strain relief on enclosure for the panel pigtail.</description>
              <smd name="1" x="-1.75" y="0" cream="no" dx="2.2" dy="3" layer="1" roundness="0" />
              <smd name="2" x="1.75" y="0" cream="no" dx="2.2" dy="3" layer="1" roundness="0" />
              <wire x1="-2.85" y1="-1.5" x2="2.85" y2="-1.5" width="0.08" layer="51" />
              <wire x1="2.85" y1="-1.5" x2="2.85" y2="1.5" width="0.08" layer="51" />
              <wire x1="2.85" y1="1.5" x2="-2.85" y2="1.5" width="0.08" layer="51" />
              <wire x1="-2.85" y1="1.5" x2="-2.85" y2="-1.5" width="0.08" layer="51" />
            </package>
            <package name="R0402">
              <description>IPC-7351 nominal chip land dimensions checked against KiCad R0402 metric SMD library; verify part-specific body height in assembly BOM.</description>
              <smd name="1" x="-0.51" y="0" dx="0.54" dy="0.64" layer="1" roundness="50" />
              <smd name="2" x="0.51" y="0" dx="0.54" dy="0.64" layer="1" roundness="50" />
              <wire x1="-0.5" y1="-0.25" x2="0.5" y2="-0.25" width="0.08" layer="51" />
              <wire x1="0.5" y1="-0.25" x2="0.5" y2="0.25" width="0.08" layer="51" />
              <wire x1="0.5" y1="0.25" x2="-0.5" y2="0.25" width="0.08" layer="51" />
              <wire x1="-0.5" y1="0.25" x2="-0.5" y2="-0.25" width="0.08" layer="51" />
            </package>
            <package name="R0603">
              <description>IPC-7351 nominal chip land dimensions checked against KiCad R0603 metric SMD library; verify part-specific body height in assembly BOM.</description>
              <smd name="1" x="-0.825" y="0" dx="0.8" dy="0.95" layer="1" roundness="50" />
              <smd name="2" x="0.825" y="0" dx="0.8" dy="0.95" layer="1" roundness="50" />
              <wire x1="-0.8" y1="-0.4" x2="0.8" y2="-0.4" width="0.08" layer="51" />
              <wire x1="0.8" y1="-0.4" x2="0.8" y2="0.4" width="0.08" layer="51" />
              <wire x1="0.8" y1="0.4" x2="-0.8" y2="0.4" width="0.08" layer="51" />
              <wire x1="-0.8" y1="0.4" x2="-0.8" y2="-0.4" width="0.08" layer="51" />
            </package>
            <package name="RT_WLCSP15">
              <description>Richtek RT6160A DS6160A-05 p4 top view and p32 SMD option. 0.25 copper / 0.22 mask within specified ±0.025 mm. ENIG, 0.08 mm local stencil. https://www.richtek.com/assets/product_file/RT6160A/DS6160A-05.pdf</description>
              <circle x="-0.4" y="0.8" radius="0.055" width="0.11" layer="29" />
              <circle x="-0.4" y="0.8" radius="0.055" width="0.11" layer="31" />
              <smd name="A1" x="-0.4" y="0.8" stop="no" cream="no" dx="0.25" dy="0.25" layer="1" roundness="100" />
              <circle x="0" y="0.8" radius="0.055" width="0.11" layer="29" />
              <circle x="0" y="0.8" radius="0.055" width="0.11" layer="31" />
              <smd name="A2" x="0" y="0.8" stop="no" cream="no" dx="0.25" dy="0.25" layer="1" roundness="100" />
              <circle x="0.4" y="0.8" radius="0.055" width="0.11" layer="29" />
              <circle x="0.4" y="0.8" radius="0.055" width="0.11" layer="31" />
              <smd name="A3" x="0.4" y="0.8" stop="no" cream="no" dx="0.25" dy="0.25" layer="1" roundness="100" />
              <circle x="-0.4" y="0.4" radius="0.055" width="0.11" layer="29" />
              <circle x="-0.4" y="0.4" radius="0.055" width="0.11" layer="31" />
              <smd name="B1" x="-0.4" y="0.4" stop="no" cream="no" dx="0.25" dy="0.25" layer="1" roundness="100" />
              <circle x="0" y="0.4" radius="0.055" width="0.11" layer="29" />
              <circle x="0" y="0.4" radius="0.055" width="0.11" layer="31" />
              <smd name="B2" x="0" y="0.4" stop="no" cream="no" dx="0.25" dy="0.25" layer="1" roundness="100" />
              <circle x="0.4" y="0.4" radius="0.055" width="0.11" layer="29" />
              <circle x="0.4" y="0.4" radius="0.055" width="0.11" layer="31" />
              <smd name="B3" x="0.4" y="0.4" stop="no" cream="no" dx="0.25" dy="0.25" layer="1" roundness="100" />
              <circle x="-0.4" y="0" radius="0.055" width="0.11" layer="29" />
              <circle x="-0.4" y="0" radius="0.055" width="0.11" layer="31" />
              <smd name="C1" x="-0.4" y="0" stop="no" cream="no" dx="0.25" dy="0.25" layer="1" roundness="100" />
              <circle x="0" y="0" radius="0.055" width="0.11" layer="29" />
              <circle x="0" y="0" radius="0.055" width="0.11" layer="31" />
              <smd name="C2" x="0" y="0" stop="no" cream="no" dx="0.25" dy="0.25" layer="1" roundness="100" />
              <circle x="0.4" y="0" radius="0.055" width="0.11" layer="29" />
              <circle x="0.4" y="0" radius="0.055" width="0.11" layer="31" />
              <smd name="C3" x="0.4" y="0" stop="no" cream="no" dx="0.25" dy="0.25" layer="1" roundness="100" />
              <circle x="-0.4" y="-0.4" radius="0.055" width="0.11" layer="29" />
              <circle x="-0.4" y="-0.4" radius="0.055" width="0.11" layer="31" />
              <smd name="D1" x="-0.4" y="-0.4" stop="no" cream="no" dx="0.25" dy="0.25" layer="1" roundness="100" />
              <circle x="0" y="-0.4" radius="0.055" width="0.11" layer="29" />
              <circle x="0" y="-0.4" radius="0.055" width="0.11" layer="31" />
              <smd name="D2" x="0" y="-0.4" stop="no" cream="no" dx="0.25" dy="0.25" layer="1" roundness="100" />
              <circle x="0.4" y="-0.4" radius="0.055" width="0.11" layer="29" />
              <circle x="0.4" y="-0.4" radius="0.055" width="0.11" layer="31" />
              <smd name="D3" x="0.4" y="-0.4" stop="no" cream="no" dx="0.25" dy="0.25" layer="1" roundness="100" />
              <circle x="-0.4" y="-0.8" radius="0.055" width="0.11" layer="29" />
              <circle x="-0.4" y="-0.8" radius="0.055" width="0.11" layer="31" />
              <smd name="E1" x="-0.4" y="-0.8" stop="no" cream="no" dx="0.25" dy="0.25" layer="1" roundness="100" />
              <circle x="0" y="-0.8" radius="0.055" width="0.11" layer="29" />
              <circle x="0" y="-0.8" radius="0.055" width="0.11" layer="31" />
              <smd name="E2" x="0" y="-0.8" stop="no" cream="no" dx="0.25" dy="0.25" layer="1" roundness="100" />
              <circle x="0.4" y="-0.8" radius="0.055" width="0.11" layer="29" />
              <circle x="0.4" y="-0.8" radius="0.055" width="0.11" layer="31" />
              <smd name="E3" x="0.4" y="-0.8" stop="no" cream="no" dx="0.25" dy="0.25" layer="1" roundness="100" />
              <wire x1="-0.72" y1="-1.17" x2="0.72" y2="-1.17" width="0.08" layer="51" />
              <wire x1="0.72" y1="-1.17" x2="0.72" y2="1.17" width="0.08" layer="51" />
              <wire x1="0.72" y1="1.17" x2="-0.72" y2="1.17" width="0.08" layer="51" />
              <wire x1="-0.72" y1="1.17" x2="-0.72" y2="-1.17" width="0.08" layer="51" />
            </package>
            <package name="SOT23_AO3401A">
              <description>Alpha &amp; Omega Semiconductor AO3401A SOT-23 top view, 1 G (bottom left), 2 S (bottom right), 3 D (top). https://www.aosmd.com/sites/default/files/res/datasheets/AO3401A.pdf</description>
              <smd name="1" x="-0.95" y="-1" dx="0.7" dy="1.05" layer="1" roundness="0" />
              <smd name="2" x="0.95" y="-1" dx="0.7" dy="1.05" layer="1" roundness="0" />
              <smd name="3" x="0" y="1" dx="0.7" dy="1.05" layer="1" roundness="0" />
              <wire x1="-1.475" y1="-0.825" x2="1.475" y2="-0.825" width="0.08" layer="51" />
              <wire x1="1.475" y1="-0.825" x2="1.475" y2="0.825" width="0.08" layer="51" />
              <wire x1="1.475" y1="0.825" x2="-1.475" y2="0.825" width="0.08" layer="51" />
              <wire x1="-1.475" y1="0.825" x2="-1.475" y2="-0.825" width="0.08" layer="51" />
            </package>
            <package name="SOT23_WAKE">
              <description>SOT23 (TO-236AB). Centre spacing 2.16 and pitch 1.90, matches lead toe span nominal 2.4 mm. Pin1 at upper left; pin2 lower left.</description>
              <smd name="1" x="-1.08" y="0.95" dx="1.1" dy="0.78" layer="1" roundness="0" />
              <smd name="2" x="-1.08" y="-0.95" dx="1.1" dy="0.78" layer="1" roundness="0" />
              <smd name="3" x="1.08" y="0" dx="1.1" dy="0.78" layer="1" roundness="0" />
              <wire x1="-0.65" y1="-1.45" x2="0.65" y2="-1.45" width="0.08" layer="51" />
              <wire x1="0.65" y1="-1.45" x2="0.65" y2="1.45" width="0.08" layer="51" />
              <wire x1="0.65" y1="1.45" x2="-0.65" y2="1.45" width="0.08" layer="51" />
              <wire x1="-0.65" y1="1.45" x2="-0.65" y2="-1.45" width="0.08" layer="51" />
            </package>
            <package name="SPV_VFQFPN20">
              <description>ST SPV1050 DS10044 rev8, manufacturer footprint figure 26, p25. 3.75 overall, 0.80 by 0.25 edge lands (ST nominal 0.20 widened to match JLC 0.25 ordinary pad minimum and maximum terminal width), 1.75 EP. Pin numbering per top view. https://www.st.com/resource/en/datasheet/spv1050.pdf</description>
              <smd name="1" x="-1.475" y="0.8" dx="0.8" dy="0.25" layer="1" roundness="15" />
              <smd name="2" x="-1.475" y="0.4" dx="0.8" dy="0.25" layer="1" roundness="15" />
              <smd name="3" x="-1.475" y="0" dx="0.8" dy="0.25" layer="1" roundness="15" />
              <smd name="4" x="-1.475" y="-0.4" dx="0.8" dy="0.25" layer="1" roundness="15" />
              <smd name="5" x="-1.475" y="-0.8" dx="0.8" dy="0.25" layer="1" roundness="15" />
              <smd name="6" x="-0.8" y="-1.475" dx="0.25" dy="0.8" layer="1" roundness="15" />
              <smd name="7" x="-0.4" y="-1.475" dx="0.25" dy="0.8" layer="1" roundness="15" />
              <smd name="8" x="-0" y="-1.475" dx="0.25" dy="0.8" layer="1" roundness="15" />
              <smd name="9" x="0.4" y="-1.475" dx="0.25" dy="0.8" layer="1" roundness="15" />
              <smd name="10" x="0.8" y="-1.475" dx="0.25" dy="0.8" layer="1" roundness="15" />
              <smd name="11" x="1.475" y="-0.8" dx="0.8" dy="0.25" layer="1" roundness="15" />
              <smd name="12" x="1.475" y="-0.4" dx="0.8" dy="0.25" layer="1" roundness="15" />
              <smd name="13" x="1.475" y="-0" dx="0.8" dy="0.25" layer="1" roundness="15" />
              <smd name="14" x="1.475" y="0.4" dx="0.8" dy="0.25" layer="1" roundness="15" />
              <smd name="15" x="1.475" y="0.8" dx="0.8" dy="0.25" layer="1" roundness="15" />
              <smd name="16" x="0.8" y="1.475" dx="0.25" dy="0.8" layer="1" roundness="15" />
              <smd name="17" x="0.4" y="1.475" dx="0.25" dy="0.8" layer="1" roundness="15" />
              <smd name="18" x="0" y="1.475" dx="0.25" dy="0.8" layer="1" roundness="15" />
              <smd name="19" x="-0.4" y="1.475" dx="0.25" dy="0.8" layer="1" roundness="15" />
              <smd name="20" x="-0.8" y="1.475" dx="0.25" dy="0.8" layer="1" roundness="15" />
              <smd name="EP" x="0" y="0" cream="no" dx="1.75" dy="1.75" layer="1" roundness="0" />
              <wire x1="-1.5" y1="-1.5" x2="1.5" y2="-1.5" width="0.08" layer="51" />
              <wire x1="1.5" y1="-1.5" x2="1.5" y2="1.5" width="0.08" layer="51" />
              <wire x1="1.5" y1="1.5" x2="-1.5" y2="1.5" width="0.08" layer="51" />
              <wire x1="-1.5" y1="1.5" x2="-1.5" y2="-1.5" width="0.08" layer="51" />
              <rectangle x1="-0.785" y1="-0.785" x2="-0.095" y2="-0.095" layer="31" />
              <rectangle x1="-0.785" y1="0.095" x2="-0.095" y2="0.785" layer="31" />
              <rectangle x1="0.095" y1="-0.785" x2="0.785" y2="-0.095" layer="31" />
              <rectangle x1="0.095" y1="0.095" x2="0.785" y2="0.785" layer="31" />
            </package>
            <package name="SRN4018">
              <description>Bourns SRN4018 data sheet p1 recommended land layout. SRN4018-100M max 1.8 mm high; body maximum 4.2 x 4.2 mm.</description>
              <smd name="1" x="-1.525" y="0" dx="1.5" dy="3.6" layer="1" roundness="0" />
              <smd name="2" x="1.525" y="0" dx="1.5" dy="3.6" layer="1" roundness="0" />
              <wire x1="-2" y1="-2" x2="2" y2="-2" width="0.08" layer="51" />
              <wire x1="2" y1="-2" x2="2" y2="2" width="0.08" layer="51" />
              <wire x1="2" y1="2" x2="-2" y2="2" width="0.08" layer="51" />
              <wire x1="-2" y1="2" x2="-2" y2="-2" width="0.08" layer="51" />
            </package>
            <package name="ST_SOT23_6_ESD">
              <description>ST USBLC6-2SC6 SOT23-6L recommended footprint. Pins 1–3 descending left and 4–6 ascending right. https://www.st.com/resource/en/datasheet/usblc6-2.pdf</description>
              <smd name="1" x="-1.3" y="0.95" dx="1.1" dy="0.6" layer="1" roundness="0" />
              <smd name="2" x="-1.3" y="0" dx="1.1" dy="0.6" layer="1" roundness="0" />
              <smd name="3" x="-1.3" y="-0.95" dx="1.1" dy="0.6" layer="1" roundness="0" />
              <smd name="4" x="1.3" y="-0.95" dx="1.1" dy="0.6" layer="1" roundness="0" />
              <smd name="5" x="1.3" y="0" dx="1.1" dy="0.6" layer="1" roundness="0" />
              <smd name="6" x="1.3" y="0.95" dx="1.1" dy="0.6" layer="1" roundness="0" />
              <wire x1="-0.875" y1="-1.5" x2="0.875" y2="-1.5" width="0.08" layer="51" />
              <wire x1="0.875" y1="-1.5" x2="0.875" y2="1.5" width="0.08" layer="51" />
              <wire x1="0.875" y1="1.5" x2="-0.875" y2="1.5" width="0.08" layer="51" />
              <wire x1="-0.875" y1="1.5" x2="-0.875" y2="-1.5" width="0.08" layer="51" />
            </package>
            <package name="SWD_FIXTURE_7">
              <description>Carrier-specific pogo pattern, pin 8 missing. The connector body belongs to the fixture.</description>
              <smd name="1" x="-3.81" y="1.27" stop="yes" cream="no" dx="1.45" dy="1.45" layer="1" roundness="100" />
              <smd name="2" x="-3.81" y="-1.27" stop="yes" cream="no" dx="1.45" dy="1.45" layer="1" roundness="100" />
              <smd name="3" x="-1.27" y="1.27" stop="yes" cream="no" dx="1.45" dy="1.45" layer="1" roundness="100" />
              <smd name="4" x="-1.27" y="-1.27" stop="yes" cream="no" dx="1.45" dy="1.45" layer="1" roundness="100" />
              <smd name="5" x="1.27" y="1.27" stop="yes" cream="no" dx="1.45" dy="1.45" layer="1" roundness="100" />
              <smd name="6" x="1.27" y="-1.27" stop="yes" cream="no" dx="1.45" dy="1.45" layer="1" roundness="100" />
              <smd name="7" x="3.81" y="1.27" stop="yes" cream="no" dx="1.45" dy="1.45" layer="1" roundness="100" />
              <wire x1="-4.575" y1="-2.05" x2="4.575" y2="-2.05" width="0.08" layer="51" />
              <wire x1="4.575" y1="-2.05" x2="4.575" y2="2.05" width="0.08" layer="51" />
              <wire x1="4.575" y1="2.05" x2="-4.575" y2="2.05" width="0.08" layer="51" />
              <wire x1="-4.575" y1="2.05" x2="-4.575" y2="-2.05" width="0.08" layer="51" />
            </package>
            <package name="TI_DBV5_W">
              <description>TI DBV0005A TPS7A02, board layout. 2.60 mm rows, 0.95 mm pitch.</description>
              <smd name="1" x="-1.3" y="0.95" dx="1.1" dy="0.6" layer="1" roundness="0" />
              <smd name="2" x="-1.3" y="0" dx="1.1" dy="0.6" layer="1" roundness="0" />
              <smd name="3" x="-1.3" y="-0.95" dx="1.1" dy="0.6" layer="1" roundness="0" />
              <smd name="4" x="1.3" y="-0.95" dx="1.1" dy="0.6" layer="1" roundness="0" />
              <smd name="5" x="1.3" y="0.95" dx="1.1" dy="0.6" layer="1" roundness="0" />
              <wire x1="-0.8" y1="-1.45" x2="0.8" y2="-1.45" width="0.08" layer="51" />
              <wire x1="0.8" y1="-1.45" x2="0.8" y2="1.45" width="0.08" layer="51" />
              <wire x1="0.8" y1="1.45" x2="-0.8" y2="1.45" width="0.08" layer="51" />
              <wire x1="-0.8" y1="1.45" x2="-0.8" y2="-1.45" width="0.08" layer="51" />
            </package>
            <package name="TI_DCK6_SENSE">
              <description>TI TPS22919 DCK0006A PCB layout.</description>
              <smd name="1" x="-1.1" y="0.65" dx="0.9" dy="0.4" layer="1" roundness="0" />
              <smd name="2" x="-1.1" y="0" dx="0.9" dy="0.4" layer="1" roundness="0" />
              <smd name="3" x="-1.1" y="-0.65" dx="0.9" dy="0.4" layer="1" roundness="0" />
              <smd name="4" x="1.1" y="-0.65" dx="0.9" dy="0.4" layer="1" roundness="0" />
              <smd name="5" x="1.1" y="0" dx="0.9" dy="0.4" layer="1" roundness="0" />
              <smd name="6" x="1.1" y="0.65" dx="0.9" dy="0.4" layer="1" roundness="0" />
              <wire x1="-0.625" y1="-1" x2="0.625" y2="-1" width="0.08" layer="51" />
              <wire x1="0.625" y1="-1" x2="0.625" y2="1" width="0.08" layer="51" />
              <wire x1="0.625" y1="1" x2="-0.625" y2="1" width="0.08" layer="51" />
              <wire x1="-0.625" y1="1" x2="-0.625" y2="-1" width="0.08" layer="51" />
            </package>
            <package name="TI_DCU8_KEY">
              <description>TI SN74AUP3G14 DCU0008A VSSOP board layout.</description>
              <smd name="1" x="-1.55" y="0.75" dx="0.85" dy="0.3" layer="1" roundness="0" />
              <smd name="2" x="-1.55" y="0.25" dx="0.85" dy="0.3" layer="1" roundness="0" />
              <smd name="3" x="-1.55" y="-0.25" dx="0.85" dy="0.3" layer="1" roundness="0" />
              <smd name="4" x="-1.55" y="-0.75" dx="0.85" dy="0.3" layer="1" roundness="0" />
              <smd name="5" x="1.55" y="-0.75" dx="0.85" dy="0.3" layer="1" roundness="0" />
              <smd name="6" x="1.55" y="-0.25" dx="0.85" dy="0.3" layer="1" roundness="0" />
              <smd name="7" x="1.55" y="0.25" dx="0.85" dy="0.3" layer="1" roundness="0" />
              <smd name="8" x="1.55" y="0.75" dx="0.85" dy="0.3" layer="1" roundness="0" />
              <wire x1="-0.9" y1="-1" x2="0.9" y2="-1" width="0.08" layer="51" />
              <wire x1="0.9" y1="-1" x2="0.9" y2="1" width="0.08" layer="51" />
              <wire x1="0.9" y1="1" x2="-0.9" y2="1" width="0.08" layer="51" />
              <wire x1="-0.9" y1="1" x2="-0.9" y2="-1" width="0.08" layer="51" />
            </package>
            <package name="TI_DDC6_TPL">
              <description>TI TPL5111 DDC0006A, example board layout, 1.10 x 0.60, rows 2.70, pitch 0.95. Pin 1 upper left.</description>
              <smd name="1" x="-1.35" y="0.95" dx="1.1" dy="0.6" layer="1" roundness="0" />
              <smd name="2" x="-1.35" y="0" dx="1.1" dy="0.6" layer="1" roundness="0" />
              <smd name="3" x="-1.35" y="-0.95" dx="1.1" dy="0.6" layer="1" roundness="0" />
              <smd name="4" x="1.35" y="-0.95" dx="1.1" dy="0.6" layer="1" roundness="0" />
              <smd name="5" x="1.35" y="0" dx="1.1" dy="0.6" layer="1" roundness="0" />
              <smd name="6" x="1.35" y="0.95" dx="1.1" dy="0.6" layer="1" roundness="0" />
              <wire x1="-0.8" y1="-1.45" x2="0.8" y2="-1.45" width="0.08" layer="51" />
              <wire x1="0.8" y1="-1.45" x2="0.8" y2="1.45" width="0.08" layer="51" />
              <wire x1="0.8" y1="1.45" x2="-0.8" y2="1.45" width="0.08" layer="51" />
              <wire x1="-0.8" y1="1.45" x2="-0.8" y2="-1.45" width="0.08" layer="51" />
            </package>
            <package name="TI_DRL8_MUX">
              <description>TI TPS2116 DRL0008A, board layout example 4224486/G p23. https://www.ti.com/lit/ds/symlink/tps2116.pdf</description>
              <smd name="1" x="-0.74" y="0.75" dx="0.67" dy="0.3" layer="1" roundness="0" />
              <smd name="2" x="-0.74" y="0.25" dx="0.67" dy="0.3" layer="1" roundness="0" />
              <smd name="3" x="-0.74" y="-0.25" dx="0.67" dy="0.3" layer="1" roundness="0" />
              <smd name="4" x="-0.74" y="-0.75" dx="0.67" dy="0.3" layer="1" roundness="0" />
              <smd name="5" x="0.74" y="-0.75" dx="0.67" dy="0.3" layer="1" roundness="0" />
              <smd name="6" x="0.74" y="-0.25" dx="0.67" dy="0.3" layer="1" roundness="0" />
              <smd name="7" x="0.74" y="0.25" dx="0.67" dy="0.3" layer="1" roundness="0" />
              <smd name="8" x="0.74" y="0.75" dx="0.67" dy="0.3" layer="1" roundness="0" />
              <wire x1="-0.6" y1="-0.8" x2="0.6" y2="-0.8" width="0.08" layer="51" />
              <wire x1="0.6" y1="-0.8" x2="0.6" y2="0.8" width="0.08" layer="51" />
              <wire x1="0.6" y1="0.8" x2="-0.6" y2="0.8" width="0.08" layer="51" />
              <wire x1="-0.6" y1="0.8" x2="-0.6" y2="-0.8" width="0.08" layer="51" />
            </package>
            <package name="TI_RGT16_BQ74">
              <description>TI BQ24074, RGT0016C current package supplement, 4222419E p53 (July 2025). 0.25 wide pads (nominal 0.24), 1.68 exposed land. https://www.ti.com/lit/ds/symlink/bq24074.pdf</description>
              <smd name="1" x="-1.4" y="0.75" dx="0.6" dy="0.25" layer="1" roundness="15" />
              <smd name="2" x="-1.4" y="0.25" dx="0.6" dy="0.25" layer="1" roundness="15" />
              <smd name="3" x="-1.4" y="-0.25" dx="0.6" dy="0.25" layer="1" roundness="15" />
              <smd name="4" x="-1.4" y="-0.75" dx="0.6" dy="0.25" layer="1" roundness="15" />
              <smd name="5" x="-0.75" y="-1.4" dx="0.25" dy="0.6" layer="1" roundness="15" />
              <smd name="6" x="-0.25" y="-1.4" dx="0.25" dy="0.6" layer="1" roundness="15" />
              <smd name="7" x="0.25" y="-1.4" dx="0.25" dy="0.6" layer="1" roundness="15" />
              <smd name="8" x="0.75" y="-1.4" dx="0.25" dy="0.6" layer="1" roundness="15" />
              <smd name="9" x="1.4" y="-0.75" dx="0.6" dy="0.25" layer="1" roundness="15" />
              <smd name="10" x="1.4" y="-0.25" dx="0.6" dy="0.25" layer="1" roundness="15" />
              <smd name="11" x="1.4" y="0.25" dx="0.6" dy="0.25" layer="1" roundness="15" />
              <smd name="12" x="1.4" y="0.75" dx="0.6" dy="0.25" layer="1" roundness="15" />
              <smd name="13" x="0.75" y="1.4" dx="0.25" dy="0.6" layer="1" roundness="15" />
              <smd name="14" x="0.25" y="1.4" dx="0.25" dy="0.6" layer="1" roundness="15" />
              <smd name="15" x="-0.25" y="1.4" dx="0.25" dy="0.6" layer="1" roundness="15" />
              <smd name="16" x="-0.75" y="1.4" dx="0.25" dy="0.6" layer="1" roundness="15" />
              <smd name="EP" x="0" y="0" cream="no" dx="1.68" dy="1.68" layer="1" roundness="0" />
              <wire x1="-1.5" y1="-1.5" x2="1.5" y2="-1.5" width="0.08" layer="51" />
              <wire x1="1.5" y1="-1.5" x2="1.5" y2="1.5" width="0.08" layer="51" />
              <wire x1="1.5" y1="1.5" x2="-1.5" y2="1.5" width="0.08" layer="51" />
              <wire x1="-1.5" y1="1.5" x2="-1.5" y2="-1.5" width="0.08" layer="51" />
              <rectangle x1="-0.765" y1="-0.765" x2="-0.075" y2="-0.075" layer="31" />
              <rectangle x1="-0.765" y1="0.075" x2="-0.075" y2="0.765" layer="31" />
              <rectangle x1="0.075" y1="-0.765" x2="0.765" y2="-0.075" layer="31" />
              <rectangle x1="0.075" y1="0.075" x2="0.765" y2="0.765" layer="31" />
            </package>
            <package name="TP">
              <description>Exposed round 1.0 mm ENIG test land, top, no stencil aperture.</description>
              <smd name="1" x="0" y="0" cream="no" dx="1" dy="1" layer="1" roundness="100" />
              <wire x1="-0.5" y1="-0.5" x2="0.5" y2="-0.5" width="0.08" layer="51" />
              <wire x1="0.5" y1="-0.5" x2="0.5" y2="0.5" width="0.08" layer="51" />
              <wire x1="0.5" y1="0.5" x2="-0.5" y2="0.5" width="0.08" layer="51" />
              <wire x1="-0.5" y1="0.5" x2="-0.5" y2="-0.5" width="0.08" layer="51" />
            </package>
          </packages>
          <symbols>
            <symbol name="USB4135-GF-A">
              <pin name="USB_CC1" x="-17.78" y="10.16" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="VBUS" x="-17.78" y="5.08" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="GND" x="-17.78" y="0" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="USB_CC2" x="-17.78" y="-5.08" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="VBUS@B9" x="-17.78" y="-10.16" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="GND@B12" x="17.78" y="10.16" length="short" direction="pas" visible="both" rot="R180" />
              <pin name="GND@SH1" x="17.78" y="5.08" length="short" direction="pas" visible="both" rot="R180" />
              <pin name="GND@SH2" x="17.78" y="0" length="short" direction="pas" visible="both" rot="R180" />
              <pin name="GND@SH3" x="17.78" y="-5.08" length="short" direction="pas" visible="both" rot="R180" />
              <pin name="GND@SH4" x="17.78" y="-10.16" length="short" direction="pas" visible="both" rot="R180" />
              <wire x1="-15.24" y1="-12.7" x2="15.24" y2="-12.7" width="0.254" layer="94" />
              <wire x1="15.24" y1="-12.7" x2="15.24" y2="12.7" width="0.254" layer="94" />
              <wire x1="15.24" y1="12.7" x2="-15.24" y2="12.7" width="0.254" layer="94" />
              <wire x1="-15.24" y1="12.7" x2="-15.24" y2="-12.7" width="0.254" layer="94" />
              <text x="-15.24" y="16.764" size="2.25" layer="95" font="proportional">&gt;NAME</text>
              <text x="-15.24" y="13.2588" size="1.7" layer="96" font="proportional">&gt;VALUE</text>
            </symbol>
            <symbol name="BM03B-ACHSS-GAN-ETF_LF__SN">
              <pin name="PACK_NEG" x="-20.32" y="5.08" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="NTC" x="-20.32" y="0" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="PACK_POS" x="-20.32" y="-5.08" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="MT1" x="20.32" y="5.08" length="short" direction="pas" visible="both" rot="R180" />
              <pin name="MT2" x="20.32" y="0" length="short" direction="pas" visible="both" rot="R180" />
              <wire x1="-17.78" y1="-7.62" x2="17.78" y2="-7.62" width="0.254" layer="94" />
              <wire x1="17.78" y1="-7.62" x2="17.78" y2="7.62" width="0.254" layer="94" />
              <wire x1="17.78" y1="7.62" x2="-17.78" y2="7.62" width="0.254" layer="94" />
              <wire x1="-17.78" y1="7.62" x2="-17.78" y2="-7.62" width="0.254" layer="94" />
              <text x="-17.78" y="11.684" size="2.25" layer="95" font="proportional">&gt;NAME</text>
              <text x="-17.78" y="8.1788" size="1.7" layer="96" font="proportional">&gt;VALUE</text>
            </symbol>
            <symbol name="PCB-FEATURE">
              <pin name="PV_POS" x="-17.78" y="0" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="PV_NEG" x="17.78" y="0" length="short" direction="pas" visible="both" rot="R180" />
              <wire x1="-15.24" y1="-5.08" x2="15.24" y2="-5.08" width="0.254" layer="94" />
              <wire x1="15.24" y1="-5.08" x2="15.24" y2="5.08" width="0.254" layer="94" />
              <wire x1="15.24" y1="5.08" x2="-15.24" y2="5.08" width="0.254" layer="94" />
              <wire x1="-15.24" y1="5.08" x2="-15.24" y2="-5.08" width="0.254" layer="94" />
              <text x="-15.24" y="9.144" size="2.25" layer="95" font="proportional">&gt;NAME</text>
              <text x="-15.24" y="5.6388" size="1.7" layer="96" font="proportional">&gt;VALUE</text>
            </symbol>
            <symbol name="SPV1050TTR">
              <pin name="MPP" x="-25.4" y="25.4" length="short" direction="in" visible="both" rot="R0" />
              <pin name="MPP_SET" x="-25.4" y="20.32" length="short" direction="in" visible="both" rot="R0" />
              <pin name="MPP_REF" x="-25.4" y="15.24" length="short" direction="in" visible="both" rot="R0" />
              <pin name="GND" x="-25.4" y="10.16" length="short" direction="pwr" visible="both" rot="R0" />
              <pin name="LDO1_EN" x="-25.4" y="5.08" length="short" direction="in" visible="both" rot="R0" />
              <pin name="LDO2_EN" x="-25.4" y="0" length="short" direction="in" visible="both" rot="R0" />
              <pin name="BATT_CHG_N" x="-25.4" y="-5.08" length="short" direction="oc" visible="both" rot="R0" />
              <pin name="BATT_CONN_N" x="-25.4" y="-10.16" length="short" direction="oc" visible="both" rot="R0" />
              <pin name="EOC" x="-25.4" y="-15.24" length="short" direction="in" visible="both" rot="R0" />
              <pin name="UVP" x="-25.4" y="-20.32" length="short" direction="in" visible="both" rot="R0" />
              <pin name="LDO1" x="-25.4" y="-25.4" length="short" direction="out" visible="both" rot="R0" />
              <pin name="LDO2" x="25.4" y="25.4" length="short" direction="out" visible="both" rot="R180" />
              <pin name="CONF" x="25.4" y="20.32" length="short" direction="in" visible="both" rot="R180" />
              <pin name="BATT" x="25.4" y="15.24" length="short" direction="io" visible="both" rot="R180" />
              <pin name="STORE" x="25.4" y="10.16" length="short" direction="out" visible="both" rot="R180" />
              <pin name="IN_LV" x="25.4" y="5.08" length="short" direction="io" visible="both" rot="R180" />
              <pin name="NC" x="25.4" y="0" length="short" direction="nc" visible="both" rot="R180" />
              <pin name="PGND" x="25.4" y="-5.08" length="short" direction="pwr" visible="both" rot="R180" />
              <pin name="L_HV" x="25.4" y="-10.16" length="short" direction="io" visible="both" rot="R180" />
              <pin name="IN_HV" x="25.4" y="-15.24" length="short" direction="pwr" visible="both" rot="R180" />
              <pin name="EP" x="25.4" y="-20.32" length="short" direction="pwr" visible="both" rot="R180" />
              <wire x1="-22.86" y1="-27.94" x2="22.86" y2="-27.94" width="0.254" layer="94" />
              <wire x1="22.86" y1="-27.94" x2="22.86" y2="27.94" width="0.254" layer="94" />
              <wire x1="22.86" y1="27.94" x2="-22.86" y2="27.94" width="0.254" layer="94" />
              <wire x1="-22.86" y1="27.94" x2="-22.86" y2="-27.94" width="0.254" layer="94" />
              <text x="-22.86" y="32.004" size="2.25" layer="95" font="proportional">&gt;NAME</text>
              <text x="-22.86" y="28.4988" size="1.7" layer="96" font="proportional">&gt;VALUE</text>
            </symbol>
            <symbol name="BQ24074RGTR">
              <pin name="TS" x="-17.78" y="17.78" length="short" direction="in" visible="both" rot="R0" />
              <pin name="BAT_1" x="-17.78" y="12.7" length="short" direction="io" visible="both" rot="R0" />
              <pin name="BAT_2" x="-17.78" y="7.62" length="short" direction="io" visible="both" rot="R0" />
              <pin name="CE_N" x="-17.78" y="2.54" length="short" direction="in" visible="both" rot="R0" />
              <pin name="EN2" x="-17.78" y="-2.54" length="short" direction="in" visible="both" rot="R0" />
              <pin name="EN1" x="-17.78" y="-7.62" length="short" direction="in" visible="both" rot="R0" />
              <pin name="PGOOD_N" x="-17.78" y="-12.7" length="short" direction="oc" visible="both" rot="R0" />
              <pin name="VSS" x="-17.78" y="-17.78" length="short" direction="pwr" visible="both" rot="R0" />
              <pin name="CHG_N" x="17.78" y="17.78" length="short" direction="oc" visible="both" rot="R180" />
              <pin name="OUT" x="17.78" y="12.7" length="short" direction="out" visible="both" rot="R180" />
              <pin name="ILIM" x="17.78" y="7.62" length="short" direction="in" visible="both" rot="R180" />
              <pin name="IN" x="17.78" y="2.54" length="short" direction="pwr" visible="both" rot="R180" />
              <pin name="TMR" x="17.78" y="-2.54" length="short" direction="in" visible="both" rot="R180" />
              <pin name="ITERM" x="17.78" y="-7.62" length="short" direction="in" visible="both" rot="R180" />
              <pin name="ISET" x="17.78" y="-12.7" length="short" direction="io" visible="both" rot="R180" />
              <pin name="EP" x="17.78" y="-17.78" length="short" direction="pwr" visible="both" rot="R180" />
              <wire x1="-15.24" y1="-20.32" x2="15.24" y2="-20.32" width="0.254" layer="94" />
              <wire x1="15.24" y1="-20.32" x2="15.24" y2="20.32" width="0.254" layer="94" />
              <wire x1="15.24" y1="20.32" x2="-15.24" y2="20.32" width="0.254" layer="94" />
              <wire x1="-15.24" y1="20.32" x2="-15.24" y2="-20.32" width="0.254" layer="94" />
              <text x="-15.24" y="24.384" size="2.25" layer="95" font="proportional">&gt;NAME</text>
              <text x="-15.24" y="20.8788" size="1.7" layer="96" font="proportional">&gt;VALUE</text>
            </symbol>
            <symbol name="TPS2116DRLR">
              <pin name="GND" x="-12.7" y="7.62" length="short" direction="pwr" visible="both" rot="R0" />
              <pin name="VOUT" x="-12.7" y="2.54" length="short" direction="out" visible="both" rot="R0" />
              <pin name="VIN1" x="-12.7" y="-2.54" length="short" direction="pwr" visible="both" rot="R0" />
              <pin name="PR1" x="-12.7" y="-7.62" length="short" direction="in" visible="both" rot="R0" />
              <pin name="MODE" x="12.7" y="7.62" length="short" direction="in" visible="both" rot="R180" />
              <pin name="VIN2" x="12.7" y="2.54" length="short" direction="pwr" visible="both" rot="R180" />
              <pin name="ST" x="12.7" y="-2.54" length="short" direction="oc" visible="both" rot="R180" />
              <wire x1="-10.16" y1="-10.16" x2="10.16" y2="-10.16" width="0.254" layer="94" />
              <wire x1="10.16" y1="-10.16" x2="10.16" y2="10.16" width="0.254" layer="94" />
              <wire x1="10.16" y1="10.16" x2="-10.16" y2="10.16" width="0.254" layer="94" />
              <wire x1="-10.16" y1="10.16" x2="-10.16" y2="-10.16" width="0.254" layer="94" />
              <text x="-10.16" y="14.224" size="2.25" layer="95" font="proportional">&gt;NAME</text>
              <text x="-10.16" y="10.7188" size="1.7" layer="96" font="proportional">&gt;VALUE</text>
            </symbol>
            <symbol name="RT6160AWSC">
              <pin name="EN" x="-17.78" y="15.24" length="short" direction="in" visible="both" rot="R0" />
              <pin name="VIN_1" x="-17.78" y="10.16" length="short" direction="pwr" visible="both" rot="R0" />
              <pin name="VIN_2" x="-17.78" y="5.08" length="short" direction="pwr" visible="both" rot="R0" />
              <pin name="VSEL" x="-17.78" y="0" length="short" direction="in" visible="both" rot="R0" />
              <pin name="SW1_1" x="-17.78" y="-5.08" length="short" direction="io" visible="both" rot="R0" />
              <pin name="SW1_2" x="-17.78" y="-10.16" length="short" direction="io" visible="both" rot="R0" />
              <pin name="AGND" x="-17.78" y="-15.24" length="short" direction="pwr" visible="both" rot="R0" />
              <pin name="PGND_1" x="17.78" y="15.24" length="short" direction="pwr" visible="both" rot="R180" />
              <pin name="PGND_2" x="17.78" y="10.16" length="short" direction="pwr" visible="both" rot="R180" />
              <pin name="SCL" x="17.78" y="5.08" length="short" direction="in" visible="both" rot="R180" />
              <pin name="SW2_1" x="17.78" y="0" length="short" direction="io" visible="both" rot="R180" />
              <pin name="SW2_2" x="17.78" y="-5.08" length="short" direction="io" visible="both" rot="R180" />
              <pin name="SDA" x="17.78" y="-10.16" length="short" direction="io" visible="both" rot="R180" />
              <pin name="VOUT" x="17.78" y="-15.24" length="short" direction="out" visible="both" rot="R180" />
              <wire x1="-15.24" y1="-17.78" x2="15.24" y2="-17.78" width="0.254" layer="94" />
              <wire x1="15.24" y1="-17.78" x2="15.24" y2="17.78" width="0.254" layer="94" />
              <wire x1="15.24" y1="17.78" x2="-15.24" y2="17.78" width="0.254" layer="94" />
              <wire x1="-15.24" y1="17.78" x2="-15.24" y2="-17.78" width="0.254" layer="94" />
              <text x="-15.24" y="21.844" size="2.25" layer="95" font="proportional">&gt;NAME</text>
              <text x="-15.24" y="18.3388" size="1.7" layer="96" font="proportional">&gt;VALUE</text>
            </symbol>
            <symbol name="MCP6542-I/MS">
              <pin name="OUTA" x="-15.24" y="7.62" length="short" direction="out" visible="both" rot="R0" />
              <pin name="INA_N" x="-15.24" y="2.54" length="short" direction="in" visible="both" rot="R0" />
              <pin name="INA_P" x="-15.24" y="-2.54" length="short" direction="in" visible="both" rot="R0" />
              <pin name="VSS" x="-15.24" y="-7.62" length="short" direction="pwr" visible="both" rot="R0" />
              <pin name="INB_P" x="15.24" y="7.62" length="short" direction="in" visible="both" rot="R180" />
              <pin name="INB_N" x="15.24" y="2.54" length="short" direction="in" visible="both" rot="R180" />
              <pin name="OUTB" x="15.24" y="-2.54" length="short" direction="out" visible="both" rot="R180" />
              <pin name="VDD" x="15.24" y="-7.62" length="short" direction="pwr" visible="both" rot="R180" />
              <wire x1="-12.7" y1="-10.16" x2="12.7" y2="-10.16" width="0.254" layer="94" />
              <wire x1="12.7" y1="-10.16" x2="12.7" y2="10.16" width="0.254" layer="94" />
              <wire x1="12.7" y1="10.16" x2="-12.7" y2="10.16" width="0.254" layer="94" />
              <wire x1="-12.7" y1="10.16" x2="-12.7" y2="-10.16" width="0.254" layer="94" />
              <text x="-12.7" y="14.224" size="2.25" layer="95" font="proportional">&gt;NAME</text>
              <text x="-12.7" y="10.7188" size="1.7" layer="96" font="proportional">&gt;VALUE</text>
            </symbol>
            <symbol name="USBLC6-2SC6">
              <pin name="IO1A" x="-12.7" y="5.08" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="GND" x="-12.7" y="0" length="short" direction="pwr" visible="both" rot="R0" />
              <pin name="IO2A" x="-12.7" y="-5.08" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="IO2B" x="12.7" y="5.08" length="short" direction="pas" visible="both" rot="R180" />
              <pin name="VBUS" x="12.7" y="0" length="short" direction="pas" visible="both" rot="R180" />
              <pin name="IO1B" x="12.7" y="-5.08" length="short" direction="pas" visible="both" rot="R180" />
              <wire x1="-10.16" y1="-7.62" x2="10.16" y2="-7.62" width="0.254" layer="94" />
              <wire x1="10.16" y1="-7.62" x2="10.16" y2="7.62" width="0.254" layer="94" />
              <wire x1="10.16" y1="7.62" x2="-10.16" y2="7.62" width="0.254" layer="94" />
              <wire x1="-10.16" y1="7.62" x2="-10.16" y2="-7.62" width="0.254" layer="94" />
              <text x="-10.16" y="11.684" size="2.25" layer="95" font="proportional">&gt;NAME</text>
              <text x="-10.16" y="8.1788" size="1.7" layer="96" font="proportional">&gt;VALUE</text>
            </symbol>
            <symbol name="D_NXP_CFP3_DIODE">
              <pin name="K" x="-7.62" y="0" length="short" direction="pas" visible="off" rot="R0" />
              <pin name="A" x="7.62" y="0" length="short" direction="pas" visible="off" rot="R180" />
              <wire x1="-5.08" y1="0" x2="-1.2" y2="0" width="0.254" layer="94" />
              <wire x1="1.2" y1="0" x2="5.08" y2="0" width="0.254" layer="94" />
              <wire x1="1.2" y1="-1.55" x2="1.2" y2="1.55" width="0.254" layer="94" />
              <wire x1="1.2" y1="1.55" x2="-1.2" y2="0" width="0.254" layer="94" />
              <wire x1="-1.2" y1="0" x2="1.2" y2="-1.55" width="0.254" layer="94" />
              <wire x1="-1.2" y1="1.55" x2="-1.2" y2="-1.55" width="0.254" layer="94" />
              <text x="-1.55" y="-3.556" size="1.2" layer="94" font="proportional">K</text>
              <text x="0" y="2.8448" size="1.8" layer="95" font="proportional" align="bottom-center">&gt;NAME</text>
              <text x="0" y="-2.159" size="1.5" layer="96" font="proportional" align="top-center">&gt;VALUE</text>
            </symbol>
            <symbol name="AO3401A">
              <pin name="G" x="-12.7" y="2.54" length="short" direction="in" visible="both" rot="R0" />
              <pin name="S" x="-12.7" y="-2.54" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="D" x="12.7" y="2.54" length="short" direction="pas" visible="both" rot="R180" />
              <wire x1="-10.16" y1="-5.08" x2="10.16" y2="-5.08" width="0.254" layer="94" />
              <wire x1="10.16" y1="-5.08" x2="10.16" y2="5.08" width="0.254" layer="94" />
              <wire x1="10.16" y1="5.08" x2="-10.16" y2="5.08" width="0.254" layer="94" />
              <wire x1="-10.16" y1="5.08" x2="-10.16" y2="-5.08" width="0.254" layer="94" />
              <text x="-10.16" y="9.144" size="2.25" layer="95" font="proportional">&gt;NAME</text>
              <text x="-10.16" y="5.6388" size="1.7" layer="96" font="proportional">&gt;VALUE</text>
            </symbol>
            <symbol name="L_BOURNS_SRN3015">
              <pin name="1" x="-7.62" y="0" length="short" direction="pas" visible="off" rot="R0" />
              <pin name="2" x="7.62" y="0" length="short" direction="pas" visible="off" rot="R180" />
              <wire x1="-5.08" y1="0" x2="-3" y2="0" width="0.254" layer="94" />
              <wire x1="3" y1="0" x2="5.08" y2="0" width="0.254" layer="94" />
              <wire x1="-3" y1="0" x2="-1.5" y2="0" width="0.254" layer="94" curve="-180" />
              <wire x1="-1.5" y1="0" x2="0" y2="0" width="0.254" layer="94" curve="-180" />
              <wire x1="0" y1="0" x2="1.5" y2="0" width="0.254" layer="94" curve="-180" />
              <wire x1="1.5" y1="0" x2="3" y2="0" width="0.254" layer="94" curve="-180" />
              <text x="0" y="2.8448" size="1.8" layer="95" font="proportional" align="bottom-center">&gt;NAME</text>
              <text x="0" y="-2.159" size="1.5" layer="96" font="proportional" align="top-center">&gt;VALUE</text>
            </symbol>
            <symbol name="L_COIL_XGL4015">
              <pin name="1" x="-7.62" y="0" length="short" direction="pas" visible="off" rot="R0" />
              <pin name="2" x="7.62" y="0" length="short" direction="pas" visible="off" rot="R180" />
              <wire x1="-5.08" y1="0" x2="-3" y2="0" width="0.254" layer="94" />
              <wire x1="3" y1="0" x2="5.08" y2="0" width="0.254" layer="94" />
              <wire x1="-3" y1="0" x2="-1.5" y2="0" width="0.254" layer="94" curve="-180" />
              <wire x1="-1.5" y1="0" x2="0" y2="0" width="0.254" layer="94" curve="-180" />
              <wire x1="0" y1="0" x2="1.5" y2="0" width="0.254" layer="94" curve="-180" />
              <wire x1="1.5" y1="0" x2="3" y2="0" width="0.254" layer="94" curve="-180" />
              <text x="0" y="2.8448" size="1.8" layer="95" font="proportional" align="bottom-center">&gt;NAME</text>
              <text x="0" y="-2.159" size="1.5" layer="96" font="proportional" align="top-center">&gt;VALUE</text>
            </symbol>
            <symbol name="R_R0402">
              <pin name="1" x="-7.62" y="0" length="short" direction="pas" visible="off" rot="R0" />
              <pin name="2" x="7.62" y="0" length="short" direction="pas" visible="off" rot="R180" />
              <wire x1="-5.08" y1="0" x2="-2.25" y2="0" width="0.254" layer="94" />
              <wire x1="2.25" y1="0" x2="5.08" y2="0" width="0.254" layer="94" />
              <wire x1="-2.25" y1="-0.875" x2="2.25" y2="-0.875" width="0.254" layer="94" />
              <wire x1="2.25" y1="-0.875" x2="2.25" y2="0.875" width="0.254" layer="94" />
              <wire x1="2.25" y1="0.875" x2="-2.25" y2="0.875" width="0.254" layer="94" />
              <wire x1="-2.25" y1="0.875" x2="-2.25" y2="-0.875" width="0.254" layer="94" />
              <text x="0" y="2.8448" size="1.8" layer="95" font="proportional" align="bottom-center">&gt;NAME</text>
              <text x="0" y="-2.159" size="1.5" layer="96" font="proportional" align="top-center">&gt;VALUE</text>
            </symbol>
            <symbol name="C_C0402">
              <pin name="1" x="-7.62" y="0" length="short" direction="pas" visible="off" rot="R0" />
              <pin name="2" x="7.62" y="0" length="short" direction="pas" visible="off" rot="R180" />
              <wire x1="-5.08" y1="0" x2="-0.46" y2="0" width="0.254" layer="94" />
              <wire x1="-0.46" y1="-1.65" x2="-0.46" y2="1.65" width="0.254" layer="94" />
              <wire x1="5.08" y1="0" x2="0.46" y2="0" width="0.254" layer="94" />
              <wire x1="0.46" y1="-1.65" x2="0.46" y2="1.65" width="0.254" layer="94" />
              <text x="0" y="2.8448" size="1.8" layer="95" font="proportional" align="bottom-center">&gt;NAME</text>
              <text x="0" y="-2.159" size="1.5" layer="96" font="proportional" align="top-center">&gt;VALUE</text>
            </symbol>
            <symbol name="C_C0603">
              <pin name="1" x="-7.62" y="0" length="short" direction="pas" visible="off" rot="R0" />
              <pin name="2" x="7.62" y="0" length="short" direction="pas" visible="off" rot="R180" />
              <wire x1="-5.08" y1="0" x2="-0.46" y2="0" width="0.254" layer="94" />
              <wire x1="-0.46" y1="-1.65" x2="-0.46" y2="1.65" width="0.254" layer="94" />
              <wire x1="5.08" y1="0" x2="0.46" y2="0" width="0.254" layer="94" />
              <wire x1="0.46" y1="-1.65" x2="0.46" y2="1.65" width="0.254" layer="94" />
              <text x="0" y="2.8448" size="1.8" layer="95" font="proportional" align="bottom-center">&gt;NAME</text>
              <text x="0" y="-2.159" size="1.5" layer="96" font="proportional" align="top-center">&gt;VALUE</text>
            </symbol>
            <symbol name="C_C1206P">
              <pin name="1" x="-7.62" y="0" length="short" direction="pas" visible="off" rot="R0" />
              <pin name="2" x="7.62" y="0" length="short" direction="pas" visible="off" rot="R180" />
              <wire x1="-5.08" y1="0" x2="-0.46" y2="0" width="0.254" layer="94" />
              <wire x1="-0.46" y1="-1.65" x2="-0.46" y2="1.65" width="0.254" layer="94" />
              <wire x1="5.08" y1="0" x2="0.46" y2="0" width="0.254" layer="94" />
              <wire x1="0.46" y1="-1.65" x2="0.46" y2="1.65" width="0.254" layer="94" />
              <text x="0" y="2.8448" size="1.8" layer="95" font="proportional" align="bottom-center">&gt;NAME</text>
              <text x="0" y="-2.159" size="1.5" layer="96" font="proportional" align="top-center">&gt;VALUE</text>
            </symbol>
            <symbol name="BAT54C_215">
              <pin name="A1" x="-15.24" y="2.54" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="A2" x="-15.24" y="-2.54" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="K1_K2" x="15.24" y="2.54" length="short" direction="pas" visible="both" rot="R180" />
              <wire x1="-12.7" y1="-5.08" x2="12.7" y2="-5.08" width="0.254" layer="94" />
              <wire x1="12.7" y1="-5.08" x2="12.7" y2="5.08" width="0.254" layer="94" />
              <wire x1="12.7" y1="5.08" x2="-12.7" y2="5.08" width="0.254" layer="94" />
              <wire x1="-12.7" y1="5.08" x2="-12.7" y2="-5.08" width="0.254" layer="94" />
              <text x="-12.7" y="9.144" size="2.25" layer="95" font="proportional">&gt;NAME</text>
              <text x="-12.7" y="5.6388" size="1.7" layer="96" font="proportional">&gt;VALUE</text>
            </symbol>
            <symbol name="R_R0603">
              <pin name="1" x="-7.62" y="0" length="short" direction="pas" visible="off" rot="R0" />
              <pin name="2" x="7.62" y="0" length="short" direction="pas" visible="off" rot="R180" />
              <wire x1="-5.08" y1="0" x2="-2.25" y2="0" width="0.254" layer="94" />
              <wire x1="2.25" y1="0" x2="5.08" y2="0" width="0.254" layer="94" />
              <wire x1="-2.25" y1="-0.875" x2="2.25" y2="-0.875" width="0.254" layer="94" />
              <wire x1="2.25" y1="-0.875" x2="2.25" y2="0.875" width="0.254" layer="94" />
              <wire x1="2.25" y1="0.875" x2="-2.25" y2="0.875" width="0.254" layer="94" />
              <wire x1="-2.25" y1="0.875" x2="-2.25" y2="-0.875" width="0.254" layer="94" />
              <text x="0" y="2.8448" size="1.8" layer="95" font="proportional" align="bottom-center">&gt;NAME</text>
              <text x="0" y="-2.159" size="1.5" layer="96" font="proportional" align="top-center">&gt;VALUE</text>
            </symbol>
            <symbol name="TP_TP">
              <pin name="1" x="-7.62" y="0" length="short" direction="pas" visible="off" rot="R0" />
              <wire x1="-5.08" y1="0" x2="-0.9" y2="0" width="0.254" layer="94" />
              <circle x="0" y="0" radius=".9" width=".254" layer="94" />
              <text x="0" y="2.8448" size="1.8" layer="95" font="proportional" align="bottom-center">&gt;NAME</text>
              <text x="0" y="-2.159" size="1.5" layer="96" font="proportional" align="top-center">&gt;VALUE</text>
            </symbol>
            <symbol name="E73-2G4M08S1F">
              <pin name="P1.09" x="-22.86" y="48.26" length="short" direction="io" visible="both" rot="R0" />
              <pin name="P1.10" x="-22.86" y="43.18" length="short" direction="io" visible="both" rot="R0" />
              <pin name="P1.11" x="-22.86" y="38.1" length="short" direction="io" visible="both" rot="R0" />
              <pin name="P1.12" x="-22.86" y="33.02" length="short" direction="io" visible="both" rot="R0" />
              <pin name="P1.13" x="-22.86" y="27.94" length="short" direction="io" visible="both" rot="R0" />
              <pin name="P1.14" x="-22.86" y="22.86" length="short" direction="io" visible="both" rot="R0" />
              <pin name="P1.04_AIN0" x="-22.86" y="17.78" length="short" direction="io" visible="both" rot="R0" />
              <pin name="P1.02" x="-22.86" y="12.7" length="short" direction="io" visible="both" rot="R0" />
              <pin name="VDD" x="-22.86" y="7.62" length="short" direction="pwr" visible="both" rot="R0" />
              <pin name="GND_10" x="-22.86" y="2.54" length="short" direction="pwr" visible="both" rot="R0" />
              <pin name="SWCLK" x="-22.86" y="-2.54" length="short" direction="in" visible="both" rot="R0" />
              <pin name="SWDIO" x="-22.86" y="-7.62" length="short" direction="io" visible="both" rot="R0" />
              <pin name="P1.03" x="-22.86" y="-12.7" length="short" direction="io" visible="both" rot="R0" />
              <pin name="P1.06" x="-22.86" y="-17.78" length="short" direction="io" visible="both" rot="R0" />
              <pin name="P1.05" x="-22.86" y="-22.86" length="short" direction="io" visible="both" rot="R0" />
              <pin name="P1.07" x="-22.86" y="-27.94" length="short" direction="io" visible="both" rot="R0" />
              <pin name="P1.08" x="-22.86" y="-33.02" length="short" direction="io" visible="both" rot="R0" />
              <pin name="P2.00" x="-22.86" y="-38.1" length="short" direction="io" visible="both" rot="R0" />
              <pin name="nRESET" x="-22.86" y="-43.18" length="short" direction="in" visible="both" rot="R0" />
              <pin name="P2.01" x="-22.86" y="-48.26" length="short" direction="io" visible="both" rot="R0" />
              <pin name="P2.02" x="22.86" y="48.26" length="short" direction="io" visible="both" rot="R180" />
              <pin name="P2.03" x="22.86" y="43.18" length="short" direction="io" visible="both" rot="R180" />
              <pin name="P2.06" x="22.86" y="38.1" length="short" direction="io" visible="both" rot="R180" />
              <pin name="P2.08" x="22.86" y="33.02" length="short" direction="io" visible="both" rot="R180" />
              <pin name="P2.10" x="22.86" y="27.94" length="short" direction="io" visible="both" rot="R180" />
              <pin name="P0.01" x="22.86" y="22.86" length="short" direction="io" visible="both" rot="R180" />
              <pin name="P2.04" x="22.86" y="17.78" length="short" direction="io" visible="both" rot="R180" />
              <pin name="P2.05" x="22.86" y="12.7" length="short" direction="io" visible="both" rot="R180" />
              <pin name="P0.00" x="22.86" y="7.62" length="short" direction="io" visible="both" rot="R180" />
              <pin name="GND_30" x="22.86" y="2.54" length="short" direction="pwr" visible="both" rot="R180" />
              <pin name="GND_31" x="22.86" y="-2.54" length="short" direction="pwr" visible="both" rot="R180" />
              <pin name="P0.02" x="22.86" y="-7.62" length="short" direction="io" visible="both" rot="R180" />
              <pin name="P0.04" x="22.86" y="-12.7" length="short" direction="io" visible="both" rot="R180" />
              <pin name="P0.03" x="22.86" y="-17.78" length="short" direction="io" visible="both" rot="R180" />
              <pin name="P2.09" x="22.86" y="-22.86" length="short" direction="io" visible="both" rot="R180" />
              <pin name="P2.07" x="22.86" y="-27.94" length="short" direction="io" visible="both" rot="R180" />
              <pin name="GND_37" x="22.86" y="-33.02" length="short" direction="pwr" visible="both" rot="R180" />
              <pin name="GND_38" x="22.86" y="-38.1" length="short" direction="pwr" visible="both" rot="R180" />
              <pin name="GND_39" x="22.86" y="-43.18" length="short" direction="pwr" visible="both" rot="R180" />
              <pin name="GND_40" x="22.86" y="-48.26" length="short" direction="pwr" visible="both" rot="R180" />
              <wire x1="-20.32" y1="-50.8" x2="20.32" y2="-50.8" width="0.254" layer="94" />
              <wire x1="20.32" y1="-50.8" x2="20.32" y2="50.8" width="0.254" layer="94" />
              <wire x1="20.32" y1="50.8" x2="-20.32" y2="50.8" width="0.254" layer="94" />
              <wire x1="-20.32" y1="50.8" x2="-20.32" y2="-50.8" width="0.254" layer="94" />
              <text x="-20.32" y="54.864" size="2.25" layer="95" font="proportional">&gt;NAME</text>
              <text x="-20.32" y="51.3588" size="1.7" layer="96" font="proportional">&gt;VALUE</text>
            </symbol>
            <symbol name="PCB_pads_only">
              <pin name="GND" x="-25.4" y="7.62" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="VTREF_SENSE" x="-25.4" y="2.54" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="SWCLK" x="-25.4" y="-2.54" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="SWDIO" x="-25.4" y="-7.62" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="nRESET" x="25.4" y="7.62" length="short" direction="pas" visible="both" rot="R180" />
              <pin name="WAKE_MDRV" x="25.4" y="2.54" length="short" direction="pas" visible="both" rot="R180" />
              <pin name="VAON" x="25.4" y="-2.54" length="short" direction="pas" visible="both" rot="R180" />
              <wire x1="-22.86" y1="-10.16" x2="22.86" y2="-10.16" width="0.254" layer="94" />
              <wire x1="22.86" y1="-10.16" x2="22.86" y2="10.16" width="0.254" layer="94" />
              <wire x1="22.86" y1="10.16" x2="-22.86" y2="10.16" width="0.254" layer="94" />
              <wire x1="-22.86" y1="10.16" x2="-22.86" y2="-10.16" width="0.254" layer="94" />
              <text x="-22.86" y="14.224" size="2.25" layer="95" font="proportional">&gt;NAME</text>
              <text x="-22.86" y="10.7188" size="1.7" layer="96" font="proportional">&gt;VALUE</text>
            </symbol>
            <symbol name="FH12-24S-0.5SH_55">
              <pin name="NC1" x="-17.78" y="30.48" length="short" direction="nc" visible="both" rot="R0" />
              <pin name="GDR" x="-17.78" y="25.4" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="RESE" x="-17.78" y="20.32" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="NC4" x="-17.78" y="15.24" length="short" direction="nc" visible="both" rot="R0" />
              <pin name="VSH2" x="-17.78" y="10.16" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="TSCL" x="-17.78" y="5.08" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="TSDA" x="-17.78" y="0" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="BS1" x="-17.78" y="-5.08" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="BUSY" x="-17.78" y="-10.16" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="nRES" x="-17.78" y="-15.24" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="DC" x="-17.78" y="-20.32" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="nCS" x="-17.78" y="-25.4" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="SCL" x="-17.78" y="-30.48" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="SDA" x="17.78" y="30.48" length="short" direction="pas" visible="both" rot="R180" />
              <pin name="VDDIO" x="17.78" y="25.4" length="short" direction="pas" visible="both" rot="R180" />
              <pin name="VCI" x="17.78" y="20.32" length="short" direction="pas" visible="both" rot="R180" />
              <pin name="VSS" x="17.78" y="15.24" length="short" direction="pas" visible="both" rot="R180" />
              <pin name="VDD" x="17.78" y="10.16" length="short" direction="pas" visible="both" rot="R180" />
              <pin name="VPP" x="17.78" y="5.08" length="short" direction="pas" visible="both" rot="R180" />
              <pin name="VSH1" x="17.78" y="0" length="short" direction="pas" visible="both" rot="R180" />
              <pin name="VGH" x="17.78" y="-5.08" length="short" direction="pas" visible="both" rot="R180" />
              <pin name="VSL" x="17.78" y="-10.16" length="short" direction="pas" visible="both" rot="R180" />
              <pin name="VGL" x="17.78" y="-15.24" length="short" direction="pas" visible="both" rot="R180" />
              <pin name="VCOM" x="17.78" y="-20.32" length="short" direction="pas" visible="both" rot="R180" />
              <pin name="SHELL1" x="17.78" y="-25.4" length="short" direction="pas" visible="both" rot="R180" />
              <pin name="SHELL2" x="17.78" y="-30.48" length="short" direction="pas" visible="both" rot="R180" />
              <wire x1="-15.24" y1="-33.02" x2="15.24" y2="-33.02" width="0.254" layer="94" />
              <wire x1="15.24" y1="-33.02" x2="15.24" y2="33.02" width="0.254" layer="94" />
              <wire x1="15.24" y1="33.02" x2="-15.24" y2="33.02" width="0.254" layer="94" />
              <wire x1="-15.24" y1="33.02" x2="-15.24" y2="-33.02" width="0.254" layer="94" />
              <text x="-15.24" y="37.084" size="2.25" layer="95" font="proportional">&gt;NAME</text>
              <text x="-15.24" y="33.5788" size="1.7" layer="96" font="proportional">&gt;VALUE</text>
            </symbol>
            <symbol name="BSS138LT1G">
              <pin name="G" x="-12.7" y="2.54" length="short" direction="in" visible="both" rot="R0" />
              <pin name="S" x="-12.7" y="-2.54" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="D" x="12.7" y="2.54" length="short" direction="pas" visible="both" rot="R180" />
              <wire x1="-10.16" y1="-5.08" x2="10.16" y2="-5.08" width="0.254" layer="94" />
              <wire x1="10.16" y1="-5.08" x2="10.16" y2="5.08" width="0.254" layer="94" />
              <wire x1="10.16" y1="5.08" x2="-10.16" y2="5.08" width="0.254" layer="94" />
              <wire x1="-10.16" y1="5.08" x2="-10.16" y2="-5.08" width="0.254" layer="94" />
              <text x="-10.16" y="9.144" size="2.25" layer="95" font="proportional">&gt;NAME</text>
              <text x="-10.16" y="5.6388" size="1.7" layer="96" font="proportional">&gt;VALUE</text>
            </symbol>
            <symbol name="L_SRN4018">
              <pin name="1" x="-7.62" y="0" length="short" direction="pas" visible="off" rot="R0" />
              <pin name="2" x="7.62" y="0" length="short" direction="pas" visible="off" rot="R180" />
              <wire x1="-5.08" y1="0" x2="-3" y2="0" width="0.254" layer="94" />
              <wire x1="3" y1="0" x2="5.08" y2="0" width="0.254" layer="94" />
              <wire x1="-3" y1="0" x2="-1.5" y2="0" width="0.254" layer="94" curve="-180" />
              <wire x1="-1.5" y1="0" x2="0" y2="0" width="0.254" layer="94" curve="-180" />
              <wire x1="0" y1="0" x2="1.5" y2="0" width="0.254" layer="94" curve="-180" />
              <wire x1="1.5" y1="0" x2="3" y2="0" width="0.254" layer="94" curve="-180" />
              <text x="0" y="2.8448" size="1.8" layer="95" font="proportional" align="bottom-center">&gt;NAME</text>
              <text x="0" y="-2.159" size="1.5" layer="96" font="proportional" align="top-center">&gt;VALUE</text>
            </symbol>
            <symbol name="D_MBR0530_CASE425">
              <pin name="K" x="-7.62" y="0" length="short" direction="pas" visible="off" rot="R0" />
              <pin name="A" x="7.62" y="0" length="short" direction="pas" visible="off" rot="R180" />
              <wire x1="-5.08" y1="0" x2="-1.2" y2="0" width="0.254" layer="94" />
              <wire x1="1.2" y1="0" x2="5.08" y2="0" width="0.254" layer="94" />
              <wire x1="1.2" y1="-1.55" x2="1.2" y2="1.55" width="0.254" layer="94" />
              <wire x1="1.2" y1="1.55" x2="-1.2" y2="0" width="0.254" layer="94" />
              <wire x1="-1.2" y1="0" x2="1.2" y2="-1.55" width="0.254" layer="94" />
              <wire x1="-1.2" y1="1.55" x2="-1.2" y2="-1.55" width="0.254" layer="94" />
              <text x="-1.55" y="-3.556" size="1.2" layer="94" font="proportional">K</text>
              <text x="0" y="2.8448" size="1.8" layer="95" font="proportional" align="bottom-center">&gt;NAME</text>
              <text x="0" y="-2.159" size="1.5" layer="96" font="proportional" align="top-center">&gt;VALUE</text>
            </symbol>
            <symbol name="C_EPD_C1210">
              <pin name="1" x="-7.62" y="0" length="short" direction="pas" visible="off" rot="R0" />
              <pin name="2" x="7.62" y="0" length="short" direction="pas" visible="off" rot="R180" />
              <wire x1="-5.08" y1="0" x2="-0.46" y2="0" width="0.254" layer="94" />
              <wire x1="-0.46" y1="-1.65" x2="-0.46" y2="1.65" width="0.254" layer="94" />
              <wire x1="5.08" y1="0" x2="0.46" y2="0" width="0.254" layer="94" />
              <wire x1="0.46" y1="-1.65" x2="0.46" y2="1.65" width="0.254" layer="94" />
              <text x="0" y="2.8448" size="1.8" layer="95" font="proportional" align="bottom-center">&gt;NAME</text>
              <text x="0" y="-2.159" size="1.5" layer="96" font="proportional" align="top-center">&gt;VALUE</text>
            </symbol>
            <symbol name="C_C0805">
              <pin name="1" x="-7.62" y="0" length="short" direction="pas" visible="off" rot="R0" />
              <pin name="2" x="7.62" y="0" length="short" direction="pas" visible="off" rot="R180" />
              <wire x1="-5.08" y1="0" x2="-0.46" y2="0" width="0.254" layer="94" />
              <wire x1="-0.46" y1="-1.65" x2="-0.46" y2="1.65" width="0.254" layer="94" />
              <wire x1="5.08" y1="0" x2="0.46" y2="0" width="0.254" layer="94" />
              <wire x1="0.46" y1="-1.65" x2="0.46" y2="1.65" width="0.254" layer="94" />
              <text x="0" y="2.8448" size="1.8" layer="95" font="proportional" align="bottom-center">&gt;NAME</text>
              <text x="0" y="-2.159" size="1.5" layer="96" font="proportional" align="top-center">&gt;VALUE</text>
            </symbol>
            <symbol name="C_EPD_C1206">
              <pin name="1" x="-7.62" y="0" length="short" direction="pas" visible="off" rot="R0" />
              <pin name="2" x="7.62" y="0" length="short" direction="pas" visible="off" rot="R180" />
              <wire x1="-5.08" y1="0" x2="-0.46" y2="0" width="0.254" layer="94" />
              <wire x1="-0.46" y1="-1.65" x2="-0.46" y2="1.65" width="0.254" layer="94" />
              <wire x1="5.08" y1="0" x2="0.46" y2="0" width="0.254" layer="94" />
              <wire x1="0.46" y1="-1.65" x2="0.46" y2="1.65" width="0.254" layer="94" />
              <text x="0" y="2.8448" size="1.8" layer="95" font="proportional" align="bottom-center">&gt;NAME</text>
              <text x="0" y="-2.159" size="1.5" layer="96" font="proportional" align="top-center">&gt;VALUE</text>
            </symbol>
            <symbol name="TP_TP_4BE49">
              <pin name="EPD_VGH" x="-7.62" y="0" length="short" direction="pas" visible="off" rot="R0" />
              <wire x1="-5.08" y1="0" x2="-0.9" y2="0" width="0.254" layer="94" />
              <circle x="0" y="0" radius=".9" width=".254" layer="94" />
              <text x="0" y="2.8448" size="1.8" layer="95" font="proportional" align="bottom-center">&gt;NAME</text>
              <text x="0" y="-2.159" size="1.5" layer="96" font="proportional" align="top-center">&gt;VALUE</text>
            </symbol>
            <symbol name="TP_TP_CC413">
              <pin name="EPD_VGL" x="-7.62" y="0" length="short" direction="pas" visible="off" rot="R0" />
              <wire x1="-5.08" y1="0" x2="-0.9" y2="0" width="0.254" layer="94" />
              <circle x="0" y="0" radius=".9" width=".254" layer="94" />
              <text x="0" y="2.8448" size="1.8" layer="95" font="proportional" align="bottom-center">&gt;NAME</text>
              <text x="0" y="-2.159" size="1.5" layer="96" font="proportional" align="top-center">&gt;VALUE</text>
            </symbol>
            <symbol name="TPS7A0228PDBVR">
              <pin name="IN" x="-12.7" y="5.08" length="short" direction="pwr" visible="both" rot="R0" />
              <pin name="GND" x="-12.7" y="0" length="short" direction="pwr" visible="both" rot="R0" />
              <pin name="EN" x="-12.7" y="-5.08" length="short" direction="in" visible="both" rot="R0" />
              <pin name="NC" x="12.7" y="5.08" length="short" direction="nc" visible="both" rot="R180" />
              <pin name="OUT" x="12.7" y="0" length="short" direction="out" visible="both" rot="R180" />
              <wire x1="-10.16" y1="-7.62" x2="10.16" y2="-7.62" width="0.254" layer="94" />
              <wire x1="10.16" y1="-7.62" x2="10.16" y2="7.62" width="0.254" layer="94" />
              <wire x1="10.16" y1="7.62" x2="-10.16" y2="7.62" width="0.254" layer="94" />
              <wire x1="-10.16" y1="7.62" x2="-10.16" y2="-7.62" width="0.254" layer="94" />
              <text x="-10.16" y="11.684" size="2.25" layer="95" font="proportional">&gt;NAME</text>
              <text x="-10.16" y="8.1788" size="1.7" layer="96" font="proportional">&gt;VALUE</text>
            </symbol>
            <symbol name="TPL5111DDCR">
              <pin name="VDD" x="-25.4" y="5.08" length="short" direction="pwr" visible="both" rot="R0" />
              <pin name="GND" x="-25.4" y="0" length="short" direction="pwr" visible="both" rot="R0" />
              <pin name="DELAY_MDRV" x="-25.4" y="-5.08" length="short" direction="in" visible="both" rot="R0" />
              <pin name="DONE" x="25.4" y="5.08" length="short" direction="in" visible="both" rot="R180" />
              <pin name="DRVn" x="25.4" y="0" length="short" direction="out" visible="both" rot="R180" />
              <pin name="EN_ONE_SHOT" x="25.4" y="-5.08" length="short" direction="in" visible="both" rot="R180" />
              <wire x1="-22.86" y1="-7.62" x2="22.86" y2="-7.62" width="0.254" layer="94" />
              <wire x1="22.86" y1="-7.62" x2="22.86" y2="7.62" width="0.254" layer="94" />
              <wire x1="22.86" y1="7.62" x2="-22.86" y2="7.62" width="0.254" layer="94" />
              <wire x1="-22.86" y1="7.62" x2="-22.86" y2="-7.62" width="0.254" layer="94" />
              <text x="-22.86" y="11.684" size="2.25" layer="95" font="proportional">&gt;NAME</text>
              <text x="-22.86" y="8.1788" size="1.7" layer="96" font="proportional">&gt;VALUE</text>
            </symbol>
            <symbol name="PCF85063AT/AY">
              <pin name="OSCI" x="-17.78" y="7.62" length="short" direction="in" visible="both" rot="R0" />
              <pin name="OSCO" x="-17.78" y="2.54" length="short" direction="out" visible="both" rot="R0" />
              <pin name="INTn" x="-17.78" y="-2.54" length="short" direction="oc" visible="both" rot="R0" />
              <pin name="VSS" x="-17.78" y="-7.62" length="short" direction="pwr" visible="both" rot="R0" />
              <pin name="SDA" x="17.78" y="7.62" length="short" direction="io" visible="both" rot="R180" />
              <pin name="SCL" x="17.78" y="2.54" length="short" direction="in" visible="both" rot="R180" />
              <pin name="CLKOUT" x="17.78" y="-2.54" length="short" direction="out" visible="both" rot="R180" />
              <pin name="VDD" x="17.78" y="-7.62" length="short" direction="pwr" visible="both" rot="R180" />
              <wire x1="-15.24" y1="-10.16" x2="15.24" y2="-10.16" width="0.254" layer="94" />
              <wire x1="15.24" y1="-10.16" x2="15.24" y2="10.16" width="0.254" layer="94" />
              <wire x1="15.24" y1="10.16" x2="-15.24" y2="10.16" width="0.254" layer="94" />
              <wire x1="-15.24" y1="10.16" x2="-15.24" y2="-10.16" width="0.254" layer="94" />
              <text x="-15.24" y="14.224" size="2.25" layer="95" font="proportional">&gt;NAME</text>
              <text x="-15.24" y="10.7188" size="1.7" layer="96" font="proportional">&gt;VALUE</text>
            </symbol>
            <symbol name="Y_ABRACON_ABS07">
              <pin name="XTAL1" x="-7.62" y="0" length="short" direction="pas" visible="off" rot="R0" />
              <pin name="XTAL2" x="7.62" y="0" length="short" direction="pas" visible="off" rot="R180" />
              <wire x1="-5.08" y1="0" x2="-1.9" y2="0" width="0.254" layer="94" />
              <wire x1="-1.9" y1="-1.6" x2="-1.9" y2="1.6" width="0.254" layer="94" />
              <wire x1="5.08" y1="0" x2="1.9" y2="0" width="0.254" layer="94" />
              <wire x1="1.9" y1="-1.6" x2="1.9" y2="1.6" width="0.254" layer="94" />
              <wire x1="-0.825" y1="-1.8" x2="0.825" y2="-1.8" width="0.254" layer="94" />
              <wire x1="0.825" y1="-1.8" x2="0.825" y2="1.8" width="0.254" layer="94" />
              <wire x1="0.825" y1="1.8" x2="-0.825" y2="1.8" width="0.254" layer="94" />
              <wire x1="-0.825" y1="1.8" x2="-0.825" y2="-1.8" width="0.254" layer="94" />
              <text x="0" y="2.8448" size="1.8" layer="95" font="proportional" align="bottom-center">&gt;NAME</text>
              <text x="0" y="-2.159" size="1.5" layer="96" font="proportional" align="top-center">&gt;VALUE</text>
            </symbol>
            <symbol name="BME280">
              <pin name="GND1" x="-15.24" y="7.62" length="short" direction="pwr" visible="both" rot="R0" />
              <pin name="CSB" x="-15.24" y="2.54" length="short" direction="in" visible="both" rot="R0" />
              <pin name="SDI" x="-15.24" y="-2.54" length="short" direction="io" visible="both" rot="R0" />
              <pin name="SCK" x="-15.24" y="-7.62" length="short" direction="in" visible="both" rot="R0" />
              <pin name="SDO" x="15.24" y="7.62" length="short" direction="io" visible="both" rot="R180" />
              <pin name="VDDIO" x="15.24" y="2.54" length="short" direction="pwr" visible="both" rot="R180" />
              <pin name="GND2" x="15.24" y="-2.54" length="short" direction="pwr" visible="both" rot="R180" />
              <pin name="VDD" x="15.24" y="-7.62" length="short" direction="pwr" visible="both" rot="R180" />
              <wire x1="-12.7" y1="-10.16" x2="12.7" y2="-10.16" width="0.254" layer="94" />
              <wire x1="12.7" y1="-10.16" x2="12.7" y2="10.16" width="0.254" layer="94" />
              <wire x1="12.7" y1="10.16" x2="-12.7" y2="10.16" width="0.254" layer="94" />
              <wire x1="-12.7" y1="10.16" x2="-12.7" y2="-10.16" width="0.254" layer="94" />
              <text x="-12.7" y="14.224" size="2.25" layer="95" font="proportional">&gt;NAME</text>
              <text x="-12.7" y="10.7188" size="1.7" layer="96" font="proportional">&gt;VALUE</text>
            </symbol>
            <symbol name="74HC123PW_118">
              <pin name="1A" x="-17.78" y="17.78" length="short" direction="in" visible="both" rot="R0" />
              <pin name="1B" x="-17.78" y="12.7" length="short" direction="in" visible="both" rot="R0" />
              <pin name="1RDn" x="-17.78" y="7.62" length="short" direction="in" visible="both" rot="R0" />
              <pin name="1Qn" x="-17.78" y="2.54" length="short" direction="out" visible="both" rot="R0" />
              <pin name="2Q" x="-17.78" y="-2.54" length="short" direction="out" visible="both" rot="R0" />
              <pin name="2CEXT" x="-17.78" y="-7.62" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="2RCEXT" x="-17.78" y="-12.7" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="GND" x="-17.78" y="-17.78" length="short" direction="pwr" visible="both" rot="R0" />
              <pin name="2A" x="17.78" y="17.78" length="short" direction="in" visible="both" rot="R180" />
              <pin name="2B" x="17.78" y="12.7" length="short" direction="in" visible="both" rot="R180" />
              <pin name="2RDn" x="17.78" y="7.62" length="short" direction="in" visible="both" rot="R180" />
              <pin name="2Qn" x="17.78" y="2.54" length="short" direction="out" visible="both" rot="R180" />
              <pin name="1Q" x="17.78" y="-2.54" length="short" direction="out" visible="both" rot="R180" />
              <pin name="1CEXT" x="17.78" y="-7.62" length="short" direction="pas" visible="both" rot="R180" />
              <pin name="1RCEXT" x="17.78" y="-12.7" length="short" direction="pas" visible="both" rot="R180" />
              <pin name="VCC" x="17.78" y="-17.78" length="short" direction="pwr" visible="both" rot="R180" />
              <wire x1="-15.24" y1="-20.32" x2="15.24" y2="-20.32" width="0.254" layer="94" />
              <wire x1="15.24" y1="-20.32" x2="15.24" y2="20.32" width="0.254" layer="94" />
              <wire x1="15.24" y1="20.32" x2="-15.24" y2="20.32" width="0.254" layer="94" />
              <wire x1="-15.24" y1="20.32" x2="-15.24" y2="-20.32" width="0.254" layer="94" />
              <text x="-15.24" y="24.384" size="2.25" layer="95" font="proportional">&gt;NAME</text>
              <text x="-15.24" y="20.8788" size="1.7" layer="96" font="proportional">&gt;VALUE</text>
            </symbol>
            <symbol name="BAT54A_215">
              <pin name="K1" x="-15.24" y="2.54" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="K2" x="-15.24" y="-2.54" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="COM_A" x="15.24" y="2.54" length="short" direction="pas" visible="both" rot="R180" />
              <wire x1="-12.7" y1="-5.08" x2="12.7" y2="-5.08" width="0.254" layer="94" />
              <wire x1="12.7" y1="-5.08" x2="12.7" y2="5.08" width="0.254" layer="94" />
              <wire x1="12.7" y1="5.08" x2="-12.7" y2="5.08" width="0.254" layer="94" />
              <wire x1="-12.7" y1="5.08" x2="-12.7" y2="-5.08" width="0.254" layer="94" />
              <text x="-12.7" y="9.144" size="2.25" layer="95" font="proportional">&gt;NAME</text>
              <text x="-12.7" y="5.6388" size="1.7" layer="96" font="proportional">&gt;VALUE</text>
            </symbol>
            <symbol name="AO3401A_8EBFA">
              <pin name="G" x="-12.7" y="2.54" length="short" direction="in" visible="both" rot="R0" />
              <pin name="S" x="-12.7" y="-2.54" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="D" x="12.7" y="2.54" length="short" direction="pas" visible="both" rot="R180" />
              <wire x1="-10.16" y1="-5.08" x2="10.16" y2="-5.08" width="0.254" layer="94" />
              <wire x1="10.16" y1="-5.08" x2="10.16" y2="5.08" width="0.254" layer="94" />
              <wire x1="10.16" y1="5.08" x2="-10.16" y2="5.08" width="0.254" layer="94" />
              <wire x1="-10.16" y1="5.08" x2="-10.16" y2="-5.08" width="0.254" layer="94" />
              <text x="-10.16" y="9.144" size="2.25" layer="95" font="proportional">&gt;NAME</text>
              <text x="-10.16" y="5.6388" size="1.7" layer="96" font="proportional">&gt;VALUE</text>
            </symbol>
            <symbol name="SN74AUP3G14DCUR">
              <pin name="1A" x="-12.7" y="7.62" length="short" direction="in" visible="both" rot="R0" />
              <pin name="3Y" x="-12.7" y="2.54" length="short" direction="out" visible="both" rot="R0" />
              <pin name="2A" x="-12.7" y="-2.54" length="short" direction="in" visible="both" rot="R0" />
              <pin name="GND" x="-12.7" y="-7.62" length="short" direction="pwr" visible="both" rot="R0" />
              <pin name="2Y" x="12.7" y="7.62" length="short" direction="out" visible="both" rot="R180" />
              <pin name="3A" x="12.7" y="2.54" length="short" direction="in" visible="both" rot="R180" />
              <pin name="1Y" x="12.7" y="-2.54" length="short" direction="out" visible="both" rot="R180" />
              <pin name="VCC" x="12.7" y="-7.62" length="short" direction="pwr" visible="both" rot="R180" />
              <wire x1="-10.16" y1="-10.16" x2="10.16" y2="-10.16" width="0.254" layer="94" />
              <wire x1="10.16" y1="-10.16" x2="10.16" y2="10.16" width="0.254" layer="94" />
              <wire x1="10.16" y1="10.16" x2="-10.16" y2="10.16" width="0.254" layer="94" />
              <wire x1="-10.16" y1="10.16" x2="-10.16" y2="-10.16" width="0.254" layer="94" />
              <text x="-10.16" y="14.224" size="2.25" layer="95" font="proportional">&gt;NAME</text>
              <text x="-10.16" y="10.7188" size="1.7" layer="96" font="proportional">&gt;VALUE</text>
            </symbol>
            <symbol name="SKRPABE010">
              <pin name="A1" x="-12.7" y="2.54" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="A2" x="-12.7" y="-2.54" length="short" direction="pas" visible="both" rot="R0" />
              <pin name="B1" x="12.7" y="2.54" length="short" direction="pas" visible="both" rot="R180" />
              <pin name="B2" x="12.7" y="-2.54" length="short" direction="pas" visible="both" rot="R180" />
              <wire x1="-10.16" y1="-5.08" x2="10.16" y2="-5.08" width="0.254" layer="94" />
              <wire x1="10.16" y1="-5.08" x2="10.16" y2="5.08" width="0.254" layer="94" />
              <wire x1="10.16" y1="5.08" x2="-10.16" y2="5.08" width="0.254" layer="94" />
              <wire x1="-10.16" y1="5.08" x2="-10.16" y2="-5.08" width="0.254" layer="94" />
              <text x="-10.16" y="9.144" size="2.25" layer="95" font="proportional">&gt;NAME</text>
              <text x="-10.16" y="5.6388" size="1.7" layer="96" font="proportional">&gt;VALUE</text>
            </symbol>
            <symbol name="TPS22919DCKR">
              <pin name="IN" x="-12.7" y="5.08" length="short" direction="pwr" visible="both" rot="R0" />
              <pin name="GND" x="-12.7" y="0" length="short" direction="pwr" visible="both" rot="R0" />
              <pin name="ON" x="-12.7" y="-5.08" length="short" direction="in" visible="both" rot="R0" />
              <pin name="NC" x="12.7" y="5.08" length="short" direction="nc" visible="both" rot="R180" />
              <pin name="QOD" x="12.7" y="0" length="short" direction="pas" visible="both" rot="R180" />
              <pin name="OUT" x="12.7" y="-5.08" length="short" direction="out" visible="both" rot="R180" />
              <wire x1="-10.16" y1="-7.62" x2="10.16" y2="-7.62" width="0.254" layer="94" />
              <wire x1="10.16" y1="-7.62" x2="10.16" y2="7.62" width="0.254" layer="94" />
              <wire x1="10.16" y1="7.62" x2="-10.16" y2="7.62" width="0.254" layer="94" />
              <wire x1="-10.16" y1="7.62" x2="-10.16" y2="-7.62" width="0.254" layer="94" />
              <text x="-10.16" y="11.684" size="2.25" layer="95" font="proportional">&gt;NAME</text>
              <text x="-10.16" y="8.1788" size="1.7" layer="96" font="proportional">&gt;VALUE</text>
            </symbol>
            <symbol name="SN74AUP1G97DCKR">
              <pin name="B" x="-12.7" y="5.08" length="short" direction="in" visible="both" rot="R0" />
              <pin name="GND" x="-12.7" y="0" length="short" direction="pwr" visible="both" rot="R0" />
              <pin name="A" x="-12.7" y="-5.08" length="short" direction="in" visible="both" rot="R0" />
              <pin name="Y" x="12.7" y="5.08" length="short" direction="out" visible="both" rot="R180" />
              <pin name="VCC" x="12.7" y="0" length="short" direction="pwr" visible="both" rot="R180" />
              <pin name="C" x="12.7" y="-5.08" length="short" direction="in" visible="both" rot="R180" />
              <wire x1="-10.16" y1="-7.62" x2="10.16" y2="-7.62" width="0.254" layer="94" />
              <wire x1="10.16" y1="-7.62" x2="10.16" y2="7.62" width="0.254" layer="94" />
              <wire x1="10.16" y1="7.62" x2="-10.16" y2="7.62" width="0.254" layer="94" />
              <wire x1="-10.16" y1="7.62" x2="-10.16" y2="-7.62" width="0.254" layer="94" />
              <text x="-10.16" y="11.684" size="2.25" layer="95" font="proportional">&gt;NAME</text>
              <text x="-10.16" y="8.1788" size="1.7" layer="96" font="proportional">&gt;VALUE</text>
            </symbol>
          </symbols>
          <devicesets>
            <deviceset name="USB4135-GF-A" prefix="J" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="USB4135-GF-A" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="GCT_USB4135">
                  <connects>
                    <connect gate="G$1" pin="USB_CC1" pad="A5" />
                    <connect gate="G$1" pin="VBUS" pad="A9" />
                    <connect gate="G$1" pin="GND" pad="A12" />
                    <connect gate="G$1" pin="USB_CC2" pad="B5" />
                    <connect gate="G$1" pin="VBUS@B9" pad="B9" />
                    <connect gate="G$1" pin="GND@B12" pad="B12" />
                    <connect gate="G$1" pin="GND@SH1" pad="SH1" />
                    <connect gate="G$1" pin="GND@SH2" pad="SH2" />
                    <connect gate="G$1" pin="GND@SH3" pad="SH3" />
                    <connect gate="G$1" pin="GND@SH4" pad="SH4" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="BM03B-ACHSS-GAN-ETF_LF__SN" prefix="J" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="BM03B-ACHSS-GAN-ETF_LF__SN" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="JST_ACH03P_POWER">
                  <connects>
                    <connect gate="G$1" pin="PACK_NEG" pad="1" />
                    <connect gate="G$1" pin="NTC" pad="2" />
                    <connect gate="G$1" pin="PACK_POS" pad="3" />
                    <connect gate="G$1" pin="MT1" pad="M1" />
                    <connect gate="G$1" pin="MT2" pad="M2" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="PCB-FEATURE" prefix="J" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="PCB-FEATURE" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="PV_WIRE_PAIR">
                  <connects>
                    <connect gate="G$1" pin="PV_POS" pad="1" />
                    <connect gate="G$1" pin="PV_NEG" pad="2" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="SPV1050TTR" prefix="U" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="SPV1050TTR" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="SPV_VFQFPN20">
                  <connects>
                    <connect gate="G$1" pin="MPP" pad="1" />
                    <connect gate="G$1" pin="MPP_SET" pad="2" />
                    <connect gate="G$1" pin="MPP_REF" pad="3" />
                    <connect gate="G$1" pin="GND" pad="4" />
                    <connect gate="G$1" pin="LDO1_EN" pad="5" />
                    <connect gate="G$1" pin="LDO2_EN" pad="6" />
                    <connect gate="G$1" pin="BATT_CHG_N" pad="7" />
                    <connect gate="G$1" pin="BATT_CONN_N" pad="8" />
                    <connect gate="G$1" pin="EOC" pad="9" />
                    <connect gate="G$1" pin="UVP" pad="10" />
                    <connect gate="G$1" pin="LDO1" pad="11" />
                    <connect gate="G$1" pin="LDO2" pad="12" />
                    <connect gate="G$1" pin="CONF" pad="13" />
                    <connect gate="G$1" pin="BATT" pad="14" />
                    <connect gate="G$1" pin="STORE" pad="15" />
                    <connect gate="G$1" pin="IN_LV" pad="16" />
                    <connect gate="G$1" pin="NC" pad="17" />
                    <connect gate="G$1" pin="PGND" pad="18" />
                    <connect gate="G$1" pin="L_HV" pad="19" />
                    <connect gate="G$1" pin="IN_HV" pad="20" />
                    <connect gate="G$1" pin="EP" pad="EP" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="BQ24074RGTR" prefix="U" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="BQ24074RGTR" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="TI_RGT16_BQ74">
                  <connects>
                    <connect gate="G$1" pin="TS" pad="1" />
                    <connect gate="G$1" pin="BAT_1" pad="2" />
                    <connect gate="G$1" pin="BAT_2" pad="3" />
                    <connect gate="G$1" pin="CE_N" pad="4" />
                    <connect gate="G$1" pin="EN2" pad="5" />
                    <connect gate="G$1" pin="EN1" pad="6" />
                    <connect gate="G$1" pin="PGOOD_N" pad="7" />
                    <connect gate="G$1" pin="VSS" pad="8" />
                    <connect gate="G$1" pin="CHG_N" pad="9" />
                    <connect gate="G$1" pin="OUT" pad="10 11" route="all" />
                    <connect gate="G$1" pin="ILIM" pad="12" />
                    <connect gate="G$1" pin="IN" pad="13" />
                    <connect gate="G$1" pin="TMR" pad="14" />
                    <connect gate="G$1" pin="ITERM" pad="15" />
                    <connect gate="G$1" pin="ISET" pad="16" />
                    <connect gate="G$1" pin="EP" pad="EP" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="TPS2116DRLR" prefix="U" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="TPS2116DRLR" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="TI_DRL8_MUX">
                  <connects>
                    <connect gate="G$1" pin="GND" pad="1" />
                    <connect gate="G$1" pin="VOUT" pad="2 7" route="all" />
                    <connect gate="G$1" pin="VIN1" pad="3" />
                    <connect gate="G$1" pin="PR1" pad="4" />
                    <connect gate="G$1" pin="MODE" pad="5" />
                    <connect gate="G$1" pin="VIN2" pad="6" />
                    <connect gate="G$1" pin="ST" pad="8" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="RT6160AWSC" prefix="U" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="RT6160AWSC" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="RT_WLCSP15">
                  <connects>
                    <connect gate="G$1" pin="EN" pad="A1" />
                    <connect gate="G$1" pin="VIN_1" pad="A2" />
                    <connect gate="G$1" pin="VIN_2" pad="A3" />
                    <connect gate="G$1" pin="VSEL" pad="B1" />
                    <connect gate="G$1" pin="SW1_1" pad="B2" />
                    <connect gate="G$1" pin="SW1_2" pad="B3" />
                    <connect gate="G$1" pin="AGND" pad="C1" />
                    <connect gate="G$1" pin="PGND_1" pad="C2" />
                    <connect gate="G$1" pin="PGND_2" pad="C3" />
                    <connect gate="G$1" pin="SCL" pad="D1" />
                    <connect gate="G$1" pin="SW2_1" pad="D2" />
                    <connect gate="G$1" pin="SW2_2" pad="D3" />
                    <connect gate="G$1" pin="SDA" pad="E1" />
                    <connect gate="G$1" pin="VOUT" pad="E2 E3" route="all" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="MCP6542-I/MS" prefix="U" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="MCP6542-I/MS" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="MC_MSOP8_TEMP">
                  <connects>
                    <connect gate="G$1" pin="OUTA" pad="1" />
                    <connect gate="G$1" pin="INA_N" pad="2" />
                    <connect gate="G$1" pin="INA_P" pad="3" />
                    <connect gate="G$1" pin="VSS" pad="4" />
                    <connect gate="G$1" pin="INB_P" pad="5" />
                    <connect gate="G$1" pin="INB_N" pad="6" />
                    <connect gate="G$1" pin="OUTB" pad="7" />
                    <connect gate="G$1" pin="VDD" pad="8" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="USBLC6-2SC6" prefix="D" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="USBLC6-2SC6" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="ST_SOT23_6_ESD">
                  <connects>
                    <connect gate="G$1" pin="IO1A" pad="1" />
                    <connect gate="G$1" pin="GND" pad="2" />
                    <connect gate="G$1" pin="IO2A" pad="3" />
                    <connect gate="G$1" pin="IO2B" pad="4" />
                    <connect gate="G$1" pin="VBUS" pad="5" />
                    <connect gate="G$1" pin="IO1B" pad="6" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="D_NXP_CFP3_DIODE" prefix="D" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="D_NXP_CFP3_DIODE" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="NXP_CFP3_DIODE">
                  <connects>
                    <connect gate="G$1" pin="K" pad="1" />
                    <connect gate="G$1" pin="A" pad="2" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="AO3401A" prefix="Q" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="AO3401A" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="SOT23_AO3401A">
                  <connects>
                    <connect gate="G$1" pin="G" pad="1" />
                    <connect gate="G$1" pin="S" pad="2" />
                    <connect gate="G$1" pin="D" pad="3" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="L_BOURNS_SRN3015" prefix="L" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="L_BOURNS_SRN3015" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="BOURNS_SRN3015">
                  <connects>
                    <connect gate="G$1" pin="1" pad="1" />
                    <connect gate="G$1" pin="2" pad="2" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="L_COIL_XGL4015" prefix="L" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="L_COIL_XGL4015" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="COIL_XGL4015">
                  <connects>
                    <connect gate="G$1" pin="1" pad="1" />
                    <connect gate="G$1" pin="2" pad="2" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="R_R0402" prefix="R" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="R_R0402" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="R0402">
                  <connects>
                    <connect gate="G$1" pin="1" pad="1" />
                    <connect gate="G$1" pin="2" pad="2" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="C_C0402" prefix="C" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="C_C0402" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="C0402">
                  <connects>
                    <connect gate="G$1" pin="1" pad="1" />
                    <connect gate="G$1" pin="2" pad="2" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="C_C0603" prefix="C" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="C_C0603" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="C0603">
                  <connects>
                    <connect gate="G$1" pin="1" pad="1" />
                    <connect gate="G$1" pin="2" pad="2" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="C_C1206P" prefix="C" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="C_C1206P" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="C1206P">
                  <connects>
                    <connect gate="G$1" pin="1" pad="1" />
                    <connect gate="G$1" pin="2" pad="2" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="BAT54C_215" prefix="D" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="BAT54C_215" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="NXP_SOT23_DIODE">
                  <connects>
                    <connect gate="G$1" pin="A1" pad="1" />
                    <connect gate="G$1" pin="A2" pad="2" />
                    <connect gate="G$1" pin="K1_K2" pad="3" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="R_R0603" prefix="R" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="R_R0603" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="R0603">
                  <connects>
                    <connect gate="G$1" pin="1" pad="1" />
                    <connect gate="G$1" pin="2" pad="2" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="TP_TP" prefix="TP" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="TP_TP" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="TP">
                  <connects>
                    <connect gate="G$1" pin="1" pad="1" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="E73-2G4M08S1F" prefix="U" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="E73-2G4M08S1F" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="EBYTE_08S1F_LGA40">
                  <connects>
                    <connect gate="G$1" pin="P1.09" pad="1" />
                    <connect gate="G$1" pin="P1.10" pad="2" />
                    <connect gate="G$1" pin="P1.11" pad="3" />
                    <connect gate="G$1" pin="P1.12" pad="4" />
                    <connect gate="G$1" pin="P1.13" pad="5" />
                    <connect gate="G$1" pin="P1.14" pad="6" />
                    <connect gate="G$1" pin="P1.04_AIN0" pad="7" />
                    <connect gate="G$1" pin="P1.02" pad="8" />
                    <connect gate="G$1" pin="VDD" pad="9" />
                    <connect gate="G$1" pin="GND_10" pad="10" />
                    <connect gate="G$1" pin="SWCLK" pad="11" />
                    <connect gate="G$1" pin="SWDIO" pad="12" />
                    <connect gate="G$1" pin="P1.03" pad="13" />
                    <connect gate="G$1" pin="P1.06" pad="14" />
                    <connect gate="G$1" pin="P1.05" pad="15" />
                    <connect gate="G$1" pin="P1.07" pad="16" />
                    <connect gate="G$1" pin="P1.08" pad="17" />
                    <connect gate="G$1" pin="P2.00" pad="18" />
                    <connect gate="G$1" pin="nRESET" pad="19" />
                    <connect gate="G$1" pin="P2.01" pad="20" />
                    <connect gate="G$1" pin="P2.02" pad="21" />
                    <connect gate="G$1" pin="P2.03" pad="22" />
                    <connect gate="G$1" pin="P2.06" pad="23" />
                    <connect gate="G$1" pin="P2.08" pad="24" />
                    <connect gate="G$1" pin="P2.10" pad="25" />
                    <connect gate="G$1" pin="P0.01" pad="26" />
                    <connect gate="G$1" pin="P2.04" pad="27" />
                    <connect gate="G$1" pin="P2.05" pad="28" />
                    <connect gate="G$1" pin="P0.00" pad="29" />
                    <connect gate="G$1" pin="GND_30" pad="30" />
                    <connect gate="G$1" pin="GND_31" pad="31" />
                    <connect gate="G$1" pin="P0.02" pad="32" />
                    <connect gate="G$1" pin="P0.04" pad="33" />
                    <connect gate="G$1" pin="P0.03" pad="34" />
                    <connect gate="G$1" pin="P2.09" pad="35" />
                    <connect gate="G$1" pin="P2.07" pad="36" />
                    <connect gate="G$1" pin="GND_37" pad="37" />
                    <connect gate="G$1" pin="GND_38" pad="38" />
                    <connect gate="G$1" pin="GND_39" pad="39" />
                    <connect gate="G$1" pin="GND_40" pad="40" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="PCB_pads_only" prefix="J" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="PCB_pads_only" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="SWD_FIXTURE_7">
                  <connects>
                    <connect gate="G$1" pin="GND" pad="1" />
                    <connect gate="G$1" pin="VTREF_SENSE" pad="2" />
                    <connect gate="G$1" pin="SWCLK" pad="3" />
                    <connect gate="G$1" pin="SWDIO" pad="4" />
                    <connect gate="G$1" pin="nRESET" pad="5" />
                    <connect gate="G$1" pin="WAKE_MDRV" pad="6" />
                    <connect gate="G$1" pin="VAON" pad="7" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="FH12-24S-0.5SH_55" prefix="J" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="FH12-24S-0.5SH_55" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="FH12_24S_05SH">
                  <connects>
                    <connect gate="G$1" pin="NC1" pad="1" />
                    <connect gate="G$1" pin="GDR" pad="2" />
                    <connect gate="G$1" pin="RESE" pad="3" />
                    <connect gate="G$1" pin="NC4" pad="4" />
                    <connect gate="G$1" pin="VSH2" pad="5" />
                    <connect gate="G$1" pin="TSCL" pad="6" />
                    <connect gate="G$1" pin="TSDA" pad="7" />
                    <connect gate="G$1" pin="BS1" pad="8" />
                    <connect gate="G$1" pin="BUSY" pad="9" />
                    <connect gate="G$1" pin="nRES" pad="10" />
                    <connect gate="G$1" pin="DC" pad="11" />
                    <connect gate="G$1" pin="nCS" pad="12" />
                    <connect gate="G$1" pin="SCL" pad="13" />
                    <connect gate="G$1" pin="SDA" pad="14" />
                    <connect gate="G$1" pin="VDDIO" pad="15" />
                    <connect gate="G$1" pin="VCI" pad="16" />
                    <connect gate="G$1" pin="VSS" pad="17" />
                    <connect gate="G$1" pin="VDD" pad="18" />
                    <connect gate="G$1" pin="VPP" pad="19" />
                    <connect gate="G$1" pin="VSH1" pad="20" />
                    <connect gate="G$1" pin="VGH" pad="21" />
                    <connect gate="G$1" pin="VSL" pad="22" />
                    <connect gate="G$1" pin="VGL" pad="23" />
                    <connect gate="G$1" pin="VCOM" pad="24" />
                    <connect gate="G$1" pin="SHELL1" pad="MP1" />
                    <connect gate="G$1" pin="SHELL2" pad="MP2" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="BSS138LT1G" prefix="Q" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="BSS138LT1G" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="BSS138_CASE318">
                  <connects>
                    <connect gate="G$1" pin="G" pad="1" />
                    <connect gate="G$1" pin="S" pad="2" />
                    <connect gate="G$1" pin="D" pad="3" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="L_SRN4018" prefix="L" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="L_SRN4018" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="SRN4018">
                  <connects>
                    <connect gate="G$1" pin="1" pad="1" />
                    <connect gate="G$1" pin="2" pad="2" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="D_MBR0530_CASE425" prefix="D" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="D_MBR0530_CASE425" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="MBR0530_CASE425">
                  <connects>
                    <connect gate="G$1" pin="K" pad="1" />
                    <connect gate="G$1" pin="A" pad="2" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="C_EPD_C1210" prefix="C" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="C_EPD_C1210" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="EPD_C1210">
                  <connects>
                    <connect gate="G$1" pin="1" pad="1" />
                    <connect gate="G$1" pin="2" pad="2" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="C_C0805" prefix="C" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="C_C0805" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="C0805">
                  <connects>
                    <connect gate="G$1" pin="1" pad="1" />
                    <connect gate="G$1" pin="2" pad="2" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="C_EPD_C1206" prefix="C" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="C_EPD_C1206" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="EPD_C1206">
                  <connects>
                    <connect gate="G$1" pin="1" pad="1" />
                    <connect gate="G$1" pin="2" pad="2" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="TP_TP_4BE49" prefix="TP" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="TP_TP_4BE49" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="TP">
                  <connects>
                    <connect gate="G$1" pin="EPD_VGH" pad="1" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="TP_TP_CC413" prefix="TP" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="TP_TP_CC413" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="TP">
                  <connects>
                    <connect gate="G$1" pin="EPD_VGL" pad="1" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="TPS7A0228PDBVR" prefix="U" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="TPS7A0228PDBVR" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="TI_DBV5_W">
                  <connects>
                    <connect gate="G$1" pin="IN" pad="1" />
                    <connect gate="G$1" pin="GND" pad="2" />
                    <connect gate="G$1" pin="EN" pad="3" />
                    <connect gate="G$1" pin="NC" pad="4" />
                    <connect gate="G$1" pin="OUT" pad="5" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="TPL5111DDCR" prefix="U" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="TPL5111DDCR" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="TI_DDC6_TPL">
                  <connects>
                    <connect gate="G$1" pin="VDD" pad="1" />
                    <connect gate="G$1" pin="GND" pad="2" />
                    <connect gate="G$1" pin="DELAY_MDRV" pad="3" />
                    <connect gate="G$1" pin="DONE" pad="4" />
                    <connect gate="G$1" pin="DRVn" pad="5" />
                    <connect gate="G$1" pin="EN_ONE_SHOT" pad="6" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="PCF85063AT/AY" prefix="U" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="PCF85063AT/AY" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="NXP_SO8_RTC">
                  <connects>
                    <connect gate="G$1" pin="OSCI" pad="1" />
                    <connect gate="G$1" pin="OSCO" pad="2" />
                    <connect gate="G$1" pin="INTn" pad="3" />
                    <connect gate="G$1" pin="VSS" pad="4" />
                    <connect gate="G$1" pin="SDA" pad="5" />
                    <connect gate="G$1" pin="SCL" pad="6" />
                    <connect gate="G$1" pin="CLKOUT" pad="7" />
                    <connect gate="G$1" pin="VDD" pad="8" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="Y_ABRACON_ABS07" prefix="Y" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="Y_ABRACON_ABS07" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="ABRACON_ABS07">
                  <connects>
                    <connect gate="G$1" pin="XTAL1" pad="1" />
                    <connect gate="G$1" pin="XTAL2" pad="2" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="BME280" prefix="U" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="BME280" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="BOSCH_BME280">
                  <connects>
                    <connect gate="G$1" pin="GND1" pad="1" />
                    <connect gate="G$1" pin="CSB" pad="2" />
                    <connect gate="G$1" pin="SDI" pad="3" />
                    <connect gate="G$1" pin="SCK" pad="4" />
                    <connect gate="G$1" pin="SDO" pad="5" />
                    <connect gate="G$1" pin="VDDIO" pad="6" />
                    <connect gate="G$1" pin="GND2" pad="7" />
                    <connect gate="G$1" pin="VDD" pad="8" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="74HC123PW_118" prefix="U" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="74HC123PW_118" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="NXP_TSSOP16_MONO">
                  <connects>
                    <connect gate="G$1" pin="1A" pad="1" />
                    <connect gate="G$1" pin="1B" pad="2" />
                    <connect gate="G$1" pin="1RDn" pad="3" />
                    <connect gate="G$1" pin="1Qn" pad="4" />
                    <connect gate="G$1" pin="2Q" pad="5" />
                    <connect gate="G$1" pin="2CEXT" pad="6" />
                    <connect gate="G$1" pin="2RCEXT" pad="7" />
                    <connect gate="G$1" pin="GND" pad="8" />
                    <connect gate="G$1" pin="2A" pad="9" />
                    <connect gate="G$1" pin="2B" pad="10" />
                    <connect gate="G$1" pin="2RDn" pad="11" />
                    <connect gate="G$1" pin="2Qn" pad="12" />
                    <connect gate="G$1" pin="1Q" pad="13" />
                    <connect gate="G$1" pin="1CEXT" pad="14" />
                    <connect gate="G$1" pin="1RCEXT" pad="15" />
                    <connect gate="G$1" pin="VCC" pad="16" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="BAT54A_215" prefix="D" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="BAT54A_215" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="SOT23_WAKE">
                  <connects>
                    <connect gate="G$1" pin="K1" pad="1" />
                    <connect gate="G$1" pin="K2" pad="2" />
                    <connect gate="G$1" pin="COM_A" pad="3" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="AO3401A_8EBFA" prefix="Q" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="AO3401A_8EBFA" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="SOT23_WAKE">
                  <connects>
                    <connect gate="G$1" pin="G" pad="1" />
                    <connect gate="G$1" pin="S" pad="2" />
                    <connect gate="G$1" pin="D" pad="3" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="SN74AUP3G14DCUR" prefix="U" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="SN74AUP3G14DCUR" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="TI_DCU8_KEY">
                  <connects>
                    <connect gate="G$1" pin="1A" pad="1" />
                    <connect gate="G$1" pin="3Y" pad="2" />
                    <connect gate="G$1" pin="2A" pad="3" />
                    <connect gate="G$1" pin="GND" pad="4" />
                    <connect gate="G$1" pin="2Y" pad="5" />
                    <connect gate="G$1" pin="3A" pad="6" />
                    <connect gate="G$1" pin="1Y" pad="7" />
                    <connect gate="G$1" pin="VCC" pad="8" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="SKRPABE010" prefix="SW" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="SKRPABE010" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="ALPS_SKRP">
                  <connects>
                    <connect gate="G$1" pin="A1" pad="1" />
                    <connect gate="G$1" pin="A2" pad="2" />
                    <connect gate="G$1" pin="B1" pad="3" />
                    <connect gate="G$1" pin="B2" pad="4" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="TPS22919DCKR" prefix="U" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="TPS22919DCKR" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="TI_DCK6_SENSE">
                  <connects>
                    <connect gate="G$1" pin="IN" pad="1" />
                    <connect gate="G$1" pin="GND" pad="2" />
                    <connect gate="G$1" pin="ON" pad="3" />
                    <connect gate="G$1" pin="NC" pad="4" />
                    <connect gate="G$1" pin="QOD" pad="5" />
                    <connect gate="G$1" pin="OUT" pad="6" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
            <deviceset name="SN74AUP1G97DCKR" prefix="U" uservalue="yes">
              <gates>
                <gate name="G$1" symbol="SN74AUP1G97DCKR" x="0" y="0" />
              </gates>
              <devices>
                <device name="" package="TI_DCK6_SENSE">
                  <connects>
                    <connect gate="G$1" pin="B" pad="1" />
                    <connect gate="G$1" pin="GND" pad="2" />
                    <connect gate="G$1" pin="A" pad="3" />
                    <connect gate="G$1" pin="Y" pad="4" />
                    <connect gate="G$1" pin="VCC" pad="5" />
                    <connect gate="G$1" pin="C" pad="6" />
                  </connects>
                  <technologies>
                    <technology name="" />
                  </technologies>
                </device>
              </devices>
            </deviceset>
          </devicesets>
        </library>
      </libraries>
      <attributes />
      <variantdefs />
      <classes>
        <class number="0" name="default" width="0" drill="0" />
        <class number="1" name="power" width="0.3" drill="0" />
      </classes>
      <parts>
        <part name="J101" library="ASTRA" deviceset="USB4135-GF-A" device="" value="USB-C power input">
          <attribute name="MPN" value="USB4135-GF-A" />
          <attribute name="LCSC" value="C5438410" />
        </part>
        <part name="J102" library="ASTRA" deviceset="BM03B-ACHSS-GAN-ETF_LF__SN" device="" value="LP223439 pack, black / yellow / red">
          <attribute name="MPN" value="BM03B-ACHSS-GAN-ETF(LF)(SN)" />
          <attribute name="LCSC" value="C5118705" />
        </part>
        <part name="J103" library="ASTRA" deviceset="PCB-FEATURE" device="" value="PV+ / PV− wire lands">
          <attribute name="MPN" value="PCB-FEATURE" />
        </part>
        <part name="U101" library="ASTRA" deviceset="SPV1050TTR" device="" value="SPV1050TTR">
          <attribute name="MPN" value="SPV1050TTR" />
          <attribute name="LCSC" value="C5181469" />
        </part>
        <part name="U102" library="ASTRA" deviceset="BQ24074RGTR" device="" value="BQ24074RGTR">
          <attribute name="MPN" value="BQ24074RGTR" />
          <attribute name="LCSC" value="C54313" />
        </part>
        <part name="U103" library="ASTRA" deviceset="TPS2116DRLR" device="" value="TPS2116DRLR">
          <attribute name="MPN" value="TPS2116DRLR" />
          <attribute name="LCSC" value="C3235557" />
        </part>
        <part name="U104" library="ASTRA" deviceset="RT6160AWSC" device="" value="RT6160AWSC">
          <attribute name="MPN" value="RT6160AWSC" />
          <attribute name="LCSC" value="C7065276" />
        </part>
        <part name="U105" library="ASTRA" deviceset="MCP6542-I/MS" device="" value="MCP6542-I/MS">
          <attribute name="MPN" value="MCP6542-I/MS" />
          <attribute name="LCSC" value="C636338" />
        </part>
        <part name="D101" library="ASTRA" deviceset="USBLC6-2SC6" device="" value="USBLC6-2SC6">
          <attribute name="MPN" value="USBLC6-2SC6" />
          <attribute name="LCSC" value="C7519" />
        </part>
        <part name="D102" library="ASTRA" deviceset="D_NXP_CFP3_DIODE" device="" value="PMEG2010ER,115">
          <attribute name="MPN" value="PMEG2010ER,115" />
          <attribute name="LCSC" value="C82288" />
        </part>
        <part name="Q101" library="ASTRA" deviceset="AO3401A" device="" value="AO3401A">
          <attribute name="MPN" value="AO3401A" />
          <attribute name="LCSC" value="C15127" />
        </part>
        <part name="L101" library="ASTRA" deviceset="L_BOURNS_SRN3015" device="" value="22uH 0.58A">
          <attribute name="MPN" value="SRN3015-220M" />
          <attribute name="LCSC" value="C2918094" />
        </part>
        <part name="L102" library="ASTRA" deviceset="L_COIL_XGL4015" device="" value="0.47uH 4.4A at 10% drop">
          <attribute name="MPN" value="XGL4015-471MEC" />
          <attribute name="LCSC" value="C5452431" />
        </part>
        <part name="R101" library="ASTRA" deviceset="R_R0402" device="" value="5.1k 1%">
          <attribute name="MPN" value="0402WGF5101TCE" />
          <attribute name="LCSC" value="C25905" />
        </part>
        <part name="R102" library="ASTRA" deviceset="R_R0402" device="" value="5.1k 1%">
          <attribute name="MPN" value="0402WGF5101TCE" />
          <attribute name="LCSC" value="C25905" />
        </part>
        <part name="R103" library="ASTRA" deviceset="R_R0402" device="" value="301k 1%">
          <attribute name="MPN" value="0402WGF3013TCE" />
          <attribute name="LCSC" value="C25775" />
        </part>
        <part name="R104" library="ASTRA" deviceset="R_R0402" device="" value="100k 1%">
          <attribute name="MPN" value="0402WGF1003TCE" />
          <attribute name="LCSC" value="C25741" />
        </part>
        <part name="C101" library="ASTRA" deviceset="C_C0402" device="" value="1uF 16V X5R">
          <attribute name="MPN" value="CL05A105KO5NNNC" />
          <attribute name="LCSC" value="C29266" />
        </part>
        <part name="C102" library="ASTRA" deviceset="C_C0603" device="" value="4.7uF 16V X5R">
          <attribute name="MPN" value="GRM188R61C475KE11D" />
          <attribute name="LCSC" value="C77045" />
        </part>
        <part name="C103" library="ASTRA" deviceset="C_C0603" device="" value="4.7uF 16V X5R">
          <attribute name="MPN" value="GRM188R61C475KE11D" />
          <attribute name="LCSC" value="C77045" />
        </part>
        <part name="C104" library="ASTRA" deviceset="C_C0402" device="" value="10nF 25V X7R">
          <attribute name="MPN" value="CL05B103KA5NNNC" />
          <attribute name="LCSC" value="C318576" />
        </part>
        <part name="R105" library="ASTRA" deviceset="R_R0402" device="" value="6.8M 1%">
          <attribute name="MPN" value="0402WGF6804TCE" />
          <attribute name="LCSC" value="C620473" />
        </part>
        <part name="R106" library="ASTRA" deviceset="R_R0402" device="" value="360k 1%">
          <attribute name="MPN" value="0402WGF3603TCE" />
          <attribute name="LCSC" value="C45956" />
        </part>
        <part name="R107" library="ASTRA" deviceset="R_R0402" device="" value="1.5M 1%">
          <attribute name="MPN" value="0402WGF1504TCE" />
          <attribute name="LCSC" value="C22276" />
        </part>
        <part name="R108" library="ASTRA" deviceset="R_R0402" device="" value="6.8M 1%">
          <attribute name="MPN" value="0402WGF6804TCE" />
          <attribute name="LCSC" value="C620473" />
        </part>
        <part name="R109" library="ASTRA" deviceset="R_R0402" device="" value="1.5M 1%">
          <attribute name="MPN" value="0402WGF1504TCE" />
          <attribute name="LCSC" value="C22276" />
        </part>
        <part name="R110" library="ASTRA" deviceset="R_R0402" device="" value="2.7M 1%">
          <attribute name="MPN" value="0402WGF2704TCE" />
          <attribute name="LCSC" value="C270621" />
        </part>
        <part name="R111" library="ASTRA" deviceset="R_R0402" device="" value="1M 1%">
          <attribute name="MPN" value="0402WGF1004TCE" />
          <attribute name="LCSC" value="C26083" />
        </part>
        <part name="C105" library="ASTRA" deviceset="C_C0402" device="" value="1uF 16V X5R">
          <attribute name="MPN" value="CL05A105KO5NNNC" />
          <attribute name="LCSC" value="C29266" />
        </part>
        <part name="C106" library="ASTRA" deviceset="C_C1206P" device="" value="47uF 10V X5R">
          <attribute name="MPN" value="GRM31CR61A476KE15L" />
          <attribute name="LCSC" value="C426659" />
        </part>
        <part name="C107" library="ASTRA" deviceset="C_C1206P" device="" value="47uF 10V X5R">
          <attribute name="MPN" value="GRM31CR61A476KE15L" />
          <attribute name="LCSC" value="C426659" />
        </part>
        <part name="C108" library="ASTRA" deviceset="C_C0402" device="" value="1uF 16V X5R">
          <attribute name="MPN" value="CL05A105KO5NNNC" />
          <attribute name="LCSC" value="C29266" />
        </part>
        <part name="R112" library="ASTRA" deviceset="R_R0402" device="" value="10k 1%">
          <attribute name="MPN" value="0402WGF1002TCE" />
          <attribute name="LCSC" value="C25744" />
        </part>
        <part name="R113" library="ASTRA" deviceset="R_R0402" device="" value="2k 1%">
          <attribute name="MPN" value="0402WGF2001TCE" />
          <attribute name="LCSC" value="C4109" />
        </part>
        <part name="R114" library="ASTRA" deviceset="R_R0402" device="" value="68k 1%">
          <attribute name="MPN" value="0402WGF6802TCE" />
          <attribute name="LCSC" value="C36871" />
        </part>
        <part name="R123" library="ASTRA" deviceset="R_R0402" device="" value="4.7k 1%">
          <attribute name="MPN" value="0402WGF4701TCE" />
          <attribute name="LCSC" value="C25900" />
        </part>
        <part name="R115" library="ASTRA" deviceset="R_R0402" device="" value="8.66k 1%">
          <attribute name="MPN" value="0402WGF8661TCE" />
          <attribute name="LCSC" value="C270576" />
        </part>
        <part name="C109" library="ASTRA" deviceset="C_C0603" device="" value="22uF 16V X5R">
          <attribute name="MPN" value="GRM188R61C226ME01D" />
          <attribute name="LCSC" value="C5116073" />
        </part>
        <part name="C110" library="ASTRA" deviceset="C_C0603" device="" value="22uF 16V X5R">
          <attribute name="MPN" value="GRM188R61C226ME01D" />
          <attribute name="LCSC" value="C5116073" />
        </part>
        <part name="C111" library="ASTRA" deviceset="C_C0402" device="" value="1uF 16V X5R">
          <attribute name="MPN" value="CL05A105KO5NNNC" />
          <attribute name="LCSC" value="C29266" />
        </part>
        <part name="R116" library="ASTRA" deviceset="R_R0402" device="" value="22k 1%">
          <attribute name="MPN" value="0402WGF2202TCE" />
          <attribute name="LCSC" value="C25768" />
        </part>
        <part name="R117" library="ASTRA" deviceset="R_R0402" device="" value="62k 1%">
          <attribute name="MPN" value="0402WGF6202TCE" />
          <attribute name="LCSC" value="C37825" />
        </part>
        <part name="R118" library="ASTRA" deviceset="R_R0402" device="" value="22k 1%">
          <attribute name="MPN" value="0402WGF2202TCE" />
          <attribute name="LCSC" value="C25768" />
        </part>
        <part name="R119" library="ASTRA" deviceset="R_R0402" device="" value="22k 1%">
          <attribute name="MPN" value="0402WGF2202TCE" />
          <attribute name="LCSC" value="C25768" />
        </part>
        <part name="R120" library="ASTRA" deviceset="R_R0402" device="" value="22k 1%">
          <attribute name="MPN" value="0402WGF2202TCE" />
          <attribute name="LCSC" value="C25768" />
        </part>
        <part name="D103" library="ASTRA" deviceset="BAT54C_215" device="" value="BAT54C,215">
          <attribute name="MPN" value="BAT54C,215" />
          <attribute name="LCSC" value="C37704" />
        </part>
        <part name="C112" library="ASTRA" deviceset="C_C0402" device="" value="100nF 16V X7R">
          <attribute name="MPN" value="CL05B104KO5NNNC" />
          <attribute name="LCSC" value="C1525" />
        </part>
        <part name="R122" library="ASTRA" deviceset="R_R0402" device="" value="1M 1%">
          <attribute name="MPN" value="0402WGF1004TCE" />
          <attribute name="LCSC" value="C26083" />
        </part>
        <part name="C113" library="ASTRA" deviceset="C_C0603" device="" value="22uF 16V X5R">
          <attribute name="MPN" value="GRM188R61C226ME01D" />
          <attribute name="LCSC" value="C5116073" />
        </part>
        <part name="C114" library="ASTRA" deviceset="C_C0402" device="" value="100nF 16V X7R">
          <attribute name="MPN" value="CL05B104KO5NNNC" />
          <attribute name="LCSC" value="C1525" />
        </part>
        <part name="C115" library="ASTRA" deviceset="C_C0603" device="" value="22uF 10V X5R">
          <attribute name="MPN" value="GRM188R61A226ME15D" />
          <attribute name="LCSC" value="C84419" />
        </part>
        <part name="C116" library="ASTRA" deviceset="C_C0603" device="" value="22uF 10V X5R">
          <attribute name="MPN" value="GRM188R61A226ME15D" />
          <attribute name="LCSC" value="C84419" />
        </part>
        <part name="R124" library="ASTRA" deviceset="R_R0603" device="" value="0R 1A DFT input">
          <attribute name="MPN" value="ERJ3GEY0R00V" />
          <attribute name="LCSC" value="C122704" />
        </part>
        <part name="R125" library="ASTRA" deviceset="R_R0603" device="" value="0R 1A DFT output">
          <attribute name="MPN" value="ERJ3GEY0R00V" />
          <attribute name="LCSC" value="C122704" />
        </part>
        <part name="R126" library="ASTRA" deviceset="R_R0603" device="" value="0R 1A DFT solar">
          <attribute name="MPN" value="ERJ3GEY0R00V" />
          <attribute name="LCSC" value="C122704" />
        </part>
        <part name="TP101" library="ASTRA" deviceset="TP_TP" device="" value="PV_STORE">
          <attribute name="MPN" value="PCB-FEATURE" />
        </part>
        <part name="TP102" library="ASTRA" deviceset="TP_TP" device="" value="CHG_IN">
          <attribute name="MPN" value="PCB-FEATURE" />
        </part>
        <part name="TP103" library="ASTRA" deviceset="TP_TP" device="" value="VBAT">
          <attribute name="MPN" value="PCB-FEATURE" />
        </part>
        <part name="TP104" library="ASTRA" deviceset="TP_TP" device="" value="SYS_AON">
          <attribute name="MPN" value="PCB-FEATURE" />
        </part>
        <part name="TP105" library="ASTRA" deviceset="TP_TP" device="" value="GND">
          <attribute name="MPN" value="PCB-FEATURE" />
        </part>
        <part name="TP106" library="ASTRA" deviceset="TP_TP" device="" value="VMAIN">
          <attribute name="MPN" value="PCB-FEATURE" />
        </part>
        <part name="U201" library="ASTRA" deviceset="E73-2G4M08S1F" device="" value="nRF54L15-QFAA + 2.4 GHz PCB antenna">
          <attribute name="MPN" value="E73-2G4M08S1F" />
          <attribute name="LCSC" value="C54337734" />
        </part>
        <part name="C201" library="ASTRA" deviceset="C_C0402" device="" value="100 nF">
          <attribute name="MPN" value="CL05B104KO5NNNC" />
          <attribute name="LCSC" value="C1525" />
        </part>
        <part name="C202" library="ASTRA" deviceset="C_C0402" device="" value="1 µF">
          <attribute name="MPN" value="CL05A105KA5NQNC" />
          <attribute name="LCSC" value="C52923" />
        </part>
        <part name="R201" library="ASTRA" deviceset="R_R0402" device="" value="10 kΩ">
          <attribute name="MPN" value="0402WGF1002TCE" />
          <attribute name="LCSC" value="C25744" />
        </part>
        <part name="C203" library="ASTRA" deviceset="C_C0402" device="" value="33 pF">
          <attribute name="MPN" value="0402CG330J500NT" />
          <attribute name="LCSC" value="C1562" />
        </part>
        <part name="J201" library="ASTRA" deviceset="PCB_pads_only" device="" value="7-pad SWD fixture">
          <attribute name="MPN" value="PCB pads only" />
        </part>
        <part name="J301" library="ASTRA" deviceset="FH12-24S-0.5SH_55" device="" value="EPD FPC 24 bottom-contact">
          <attribute name="MPN" value="FH12-24S-0.5SH(55)" />
          <attribute name="LCSC" value="C202112" />
        </part>
        <part name="Q301" library="ASTRA" deviceset="BSS138LT1G" device="" value="BSS138L 50V NMOS">
          <attribute name="MPN" value="BSS138LT1G" />
          <attribute name="LCSC" value="C82045" />
        </part>
        <part name="L301" library="ASTRA" deviceset="L_SRN4018" device="" value="10uH 1.4A Isat">
          <attribute name="MPN" value="SRN4018-100M" />
          <attribute name="LCSC" value="C503307" />
        </part>
        <part name="D301" library="ASTRA" deviceset="D_MBR0530_CASE425" device="" value="MBR0530 30V Schottky">
          <attribute name="MPN" value="MBR0530T1G" />
          <attribute name="LCSC" value="C82046" />
        </part>
        <part name="D302" library="ASTRA" deviceset="D_MBR0530_CASE425" device="" value="MBR0530 30V Schottky">
          <attribute name="MPN" value="MBR0530T1G" />
          <attribute name="LCSC" value="C82046" />
        </part>
        <part name="D303" library="ASTRA" deviceset="D_MBR0530_CASE425" device="" value="MBR0530 30V Schottky">
          <attribute name="MPN" value="MBR0530T1G" />
          <attribute name="LCSC" value="C82046" />
        </part>
        <part name="R301" library="ASTRA" deviceset="R_R0402" device="" value="10k 1%">
          <attribute name="MPN" value="0402WGF1002TCE" />
          <attribute name="LCSC" value="C25744" />
        </part>
        <part name="R302" library="ASTRA" deviceset="R_R0603" device="" value="3R 1% 100mW">
          <attribute name="MPN" value="RC0603FR-073RL" />
          <attribute name="LCSC" value="C137724" />
        </part>
        <part name="C301" library="ASTRA" deviceset="C_EPD_C1210" device="" value="4.7uF 50V X7R">
          <attribute name="MPN" value="CL32B475KBJNNNE" />
          <attribute name="LCSC" value="C47783" />
        </part>
        <part name="C302" library="ASTRA" deviceset="C_C0805" device="" value="4.7uF 25V X5R">
          <attribute name="MPN" value="CL21A475KAQNNNE" />
          <attribute name="LCSC" value="C1779" />
        </part>
        <part name="C303" library="ASTRA" deviceset="C_C0805" device="" value="1uF 50V X7R">
          <attribute name="MPN" value="CL21B105KBFNNNE" />
          <attribute name="LCSC" value="C28323" />
        </part>
        <part name="C304" library="ASTRA" deviceset="C_C0402" device="" value="100nF 16V X7R">
          <attribute name="MPN" value="CL05B104KO5NNNC" />
          <attribute name="LCSC" value="C1525" />
        </part>
        <part name="C305" library="ASTRA" deviceset="C_C0402" device="" value="1uF 25V X5R">
          <attribute name="MPN" value="CL05A105KA5NQNC" />
          <attribute name="LCSC" value="C52923" />
        </part>
        <part name="C306" library="ASTRA" deviceset="C_C0805" device="" value="1uF 50V X7R">
          <attribute name="MPN" value="CL21B105KBFNNNE" />
          <attribute name="LCSC" value="C28323" />
        </part>
        <part name="C307" library="ASTRA" deviceset="C_C0805" device="" value="1uF 50V X7R">
          <attribute name="MPN" value="CL21B105KBFNNNE" />
          <attribute name="LCSC" value="C28323" />
        </part>
        <part name="C308" library="ASTRA" deviceset="C_EPD_C1206" device="" value="1uF 100V X7R">
          <attribute name="MPN" value="CL31B105KCHNNNE" />
          <attribute name="LCSC" value="C13832" />
        </part>
        <part name="C309" library="ASTRA" deviceset="C_C0805" device="" value="1uF 50V X7R">
          <attribute name="MPN" value="CL21B105KBFNNNE" />
          <attribute name="LCSC" value="C28323" />
        </part>
        <part name="C310" library="ASTRA" deviceset="C_EPD_C1206" device="" value="1uF 100V X7R">
          <attribute name="MPN" value="CL31B105KCHNNNE" />
          <attribute name="LCSC" value="C13832" />
        </part>
        <part name="C311" library="ASTRA" deviceset="C_C0805" device="" value="1uF 50V X7R">
          <attribute name="MPN" value="CL21B105KBFNNNE" />
          <attribute name="LCSC" value="C28323" />
        </part>
        <part name="R303" library="ASTRA" deviceset="R_R0402" device="" value="100k 1%">
          <attribute name="MPN" value="0402WGF1003TCE" />
          <attribute name="LCSC" value="C25741" />
        </part>
        <part name="R304" library="ASTRA" deviceset="R_R0402" device="" value="100k 1%">
          <attribute name="MPN" value="0402WGF1003TCE" />
          <attribute name="LCSC" value="C25741" />
        </part>
        <part name="R305" library="ASTRA" deviceset="R_R0402" device="" value="100k 1%">
          <attribute name="MPN" value="0402WGF1003TCE" />
          <attribute name="LCSC" value="C25741" />
        </part>
        <part name="TP301" library="ASTRA" deviceset="TP_TP_4BE49" device="" value="EPD_VGH">
          <attribute name="MPN" value="PCB test land" />
        </part>
        <part name="TP302" library="ASTRA" deviceset="TP_TP_CC413" device="" value="EPD_VGL">
          <attribute name="MPN" value="PCB test land" />
        </part>
        <part name="U401" library="ASTRA" deviceset="TPS7A0228PDBVR" device="" value="2.8V always-on">
          <attribute name="MPN" value="TPS7A0228PDBVR" />
          <attribute name="LCSC" value="C5220176" />
        </part>
        <part name="C401" library="ASTRA" deviceset="C_C0805" device="" value="4.7u 16V">
          <attribute name="MPN" value="CL21B475KOFNNNE" />
          <attribute name="LCSC" value="C107365" />
        </part>
        <part name="C402" library="ASTRA" deviceset="C_C0805" device="" value="4.7u 16V">
          <attribute name="MPN" value="CL21B475KOFNNNE" />
          <attribute name="LCSC" value="C107365" />
        </part>
        <part name="U402" library="ASTRA" deviceset="TPL5111DDCR" device="" value="One-shot watchdog">
          <attribute name="MPN" value="TPL5111DDCR" />
          <attribute name="LCSC" value="C2870554" />
        </part>
        <part name="C403" library="ASTRA" deviceset="C_C0402" device="" value="100n 16V">
          <attribute name="MPN" value="CL05B104KO5NNNC" />
          <attribute name="LCSC" value="C1525" />
        </part>
        <part name="R401" library="ASTRA" deviceset="R_R0402" device="" value="30k 1%">
          <attribute name="MPN" value="0402WGF3002TCE" />
          <attribute name="LCSC" value="C25776" />
        </part>
        <part name="R402" library="ASTRA" deviceset="R_R0402" device="" value="33k 1%">
          <attribute name="MPN" value="0402WGF3302TCE" />
          <attribute name="LCSC" value="C25779" />
        </part>
        <part name="R403" library="ASTRA" deviceset="R_R0402" device="" value="100k 1%">
          <attribute name="MPN" value="0402WGF1003TCE" />
          <attribute name="LCSC" value="C25741" />
        </part>
        <part name="C404" library="ASTRA" deviceset="C_C0402" device="" value="10n 50V">
          <attribute name="MPN" value="CL05B103KB5NNNC" />
          <attribute name="LCSC" value="C15195" />
        </part>
        <part name="U403" library="ASTRA" deviceset="PCF85063AT/AY" device="" value="RTC 0x51">
          <attribute name="MPN" value="PCF85063AT/AY" />
          <attribute name="LCSC" value="C5151540" />
        </part>
        <part name="Y401" library="ASTRA" deviceset="Y_ABRACON_ABS07" device="" value="32.768 kHz 7pF">
          <attribute name="MPN" value="ABS07-32.768KHZ-7-1-T" />
          <attribute name="LCSC" value="C1985277" />
        </part>
        <part name="C407" library="ASTRA" deviceset="C_C0402" device="" value="100n 16V">
          <attribute name="MPN" value="CL05B104KO5NNNC" />
          <attribute name="LCSC" value="C1525" />
        </part>
        <part name="R404" library="ASTRA" deviceset="R_R0402" device="" value="47k 1%">
          <attribute name="MPN" value="0402WGF4702TCE" />
          <attribute name="LCSC" value="C25792" />
        </part>
        <part name="R405" library="ASTRA" deviceset="R_R0402" device="" value="4.7k 1%">
          <attribute name="MPN" value="0402WGF4701TCE" />
          <attribute name="LCSC" value="C25900" />
        </part>
        <part name="R406" library="ASTRA" deviceset="R_R0402" device="" value="4.7k 1%">
          <attribute name="MPN" value="0402WGF4701TCE" />
          <attribute name="LCSC" value="C25900" />
        </part>
        <part name="U404" library="ASTRA" deviceset="BME280" device="" value="BME280 0x76">
          <attribute name="MPN" value="BME280" />
          <attribute name="LCSC" value="C92489" />
        </part>
        <part name="C405" library="ASTRA" deviceset="C_C0402" device="" value="100n 16V">
          <attribute name="MPN" value="CL05B104KO5NNNC" />
          <attribute name="LCSC" value="C1525" />
        </part>
        <part name="C406" library="ASTRA" deviceset="C_C0402" device="" value="100n 16V">
          <attribute name="MPN" value="CL05B104KO5NNNC" />
          <attribute name="LCSC" value="C1525" />
        </part>
        <part name="U405" library="ASTRA" deviceset="74HC123PW_118" device="" value="Dual event monostable">
          <attribute name="MPN" value="74HC123PW,118" />
          <attribute name="LCSC" value="C426698" />
        </part>
        <part name="C408" library="ASTRA" deviceset="C_C0402" device="" value="100n 16V">
          <attribute name="MPN" value="CL05B104KO5NNNC" />
          <attribute name="LCSC" value="C1525" />
        </part>
        <part name="R407" library="ASTRA" deviceset="R_R0402" device="" value="47k 1%">
          <attribute name="MPN" value="0402WGF4702TCE" />
          <attribute name="LCSC" value="C25792" />
        </part>
        <part name="C409" library="ASTRA" deviceset="C_C0805" device="" value="4.7u 16V">
          <attribute name="MPN" value="CL21B475KOFNNNE" />
          <attribute name="LCSC" value="C107365" />
        </part>
        <part name="R408" library="ASTRA" deviceset="R_R0402" device="" value="47k 1%">
          <attribute name="MPN" value="0402WGF4702TCE" />
          <attribute name="LCSC" value="C25792" />
        </part>
        <part name="C410" library="ASTRA" deviceset="C_C0805" device="" value="4.7u 16V">
          <attribute name="MPN" value="CL21B475KOFNNNE" />
          <attribute name="LCSC" value="C107365" />
        </part>
        <part name="D401" library="ASTRA" deviceset="BAT54A_215" device="" value="Dual Schottky common anode">
          <attribute name="MPN" value="BAT54A,215" />
          <attribute name="LCSC" value="C130910" />
        </part>
        <part name="R409" library="ASTRA" deviceset="R_R0402" device="" value="100k 1%">
          <attribute name="MPN" value="0402WGF1003TCE" />
          <attribute name="LCSC" value="C25741" />
        </part>
        <part name="Q401" library="ASTRA" deviceset="AO3401A_8EBFA" device="" value="P-channel wake drive">
          <attribute name="MPN" value="AO3401A" />
          <attribute name="LCSC" value="C15127" />
        </part>
        <part name="U406" library="ASTRA" deviceset="SN74AUP3G14DCUR" device="" value="Key isolation / Schmitt">
          <attribute name="MPN" value="SN74AUP3G14DCUR" />
          <attribute name="LCSC" value="C2863927" />
        </part>
        <part name="C411" library="ASTRA" deviceset="C_C0402" device="" value="100n 16V">
          <attribute name="MPN" value="CL05B104KO5NNNC" />
          <attribute name="LCSC" value="C1525" />
        </part>
        <part name="R410" library="ASTRA" deviceset="R_R0402" device="" value="47k 1%">
          <attribute name="MPN" value="0402WGF4702TCE" />
          <attribute name="LCSC" value="C25792" />
        </part>
        <part name="D402" library="ASTRA" deviceset="BAT54A_215" device="" value="Dual Schottky common anode">
          <attribute name="MPN" value="BAT54A,215" />
          <attribute name="LCSC" value="C130910" />
        </part>
        <part name="D403" library="ASTRA" deviceset="BAT54A_215" device="" value="Dual Schottky common anode">
          <attribute name="MPN" value="BAT54A,215" />
          <attribute name="LCSC" value="C130910" />
        </part>
        <part name="SW401" library="ASTRA" deviceset="SKRPABE010" device="" value="Key 1">
          <attribute name="MPN" value="SKRPABE010" />
          <attribute name="LCSC" value="C115360" />
        </part>
        <part name="R411" library="ASTRA" deviceset="R_R0402" device="" value="100k 1%">
          <attribute name="MPN" value="0402WGF1003TCE" />
          <attribute name="LCSC" value="C25741" />
        </part>
        <part name="C412" library="ASTRA" deviceset="C_C0805" device="" value="4.7u 16V">
          <attribute name="MPN" value="CL21B475KOFNNNE" />
          <attribute name="LCSC" value="C107365" />
        </part>
        <part name="R414" library="ASTRA" deviceset="R_R0402" device="" value="330R 1%">
          <attribute name="MPN" value="0402WGF3300TCE" />
          <attribute name="LCSC" value="C25104" />
        </part>
        <part name="R417" library="ASTRA" deviceset="R_R0402" device="" value="3.3k 1%">
          <attribute name="MPN" value="0402WGF3301TCE" />
          <attribute name="LCSC" value="C25890" />
        </part>
        <part name="SW402" library="ASTRA" deviceset="SKRPABE010" device="" value="Key 2">
          <attribute name="MPN" value="SKRPABE010" />
          <attribute name="LCSC" value="C115360" />
        </part>
        <part name="R412" library="ASTRA" deviceset="R_R0402" device="" value="100k 1%">
          <attribute name="MPN" value="0402WGF1003TCE" />
          <attribute name="LCSC" value="C25741" />
        </part>
        <part name="C413" library="ASTRA" deviceset="C_C0805" device="" value="4.7u 16V">
          <attribute name="MPN" value="CL21B475KOFNNNE" />
          <attribute name="LCSC" value="C107365" />
        </part>
        <part name="R415" library="ASTRA" deviceset="R_R0402" device="" value="330R 1%">
          <attribute name="MPN" value="0402WGF3300TCE" />
          <attribute name="LCSC" value="C25104" />
        </part>
        <part name="R418" library="ASTRA" deviceset="R_R0402" device="" value="3.3k 1%">
          <attribute name="MPN" value="0402WGF3301TCE" />
          <attribute name="LCSC" value="C25890" />
        </part>
        <part name="SW403" library="ASTRA" deviceset="SKRPABE010" device="" value="Key 3">
          <attribute name="MPN" value="SKRPABE010" />
          <attribute name="LCSC" value="C115360" />
        </part>
        <part name="R413" library="ASTRA" deviceset="R_R0402" device="" value="100k 1%">
          <attribute name="MPN" value="0402WGF1003TCE" />
          <attribute name="LCSC" value="C25741" />
        </part>
        <part name="C414" library="ASTRA" deviceset="C_C0805" device="" value="4.7u 16V">
          <attribute name="MPN" value="CL21B475KOFNNNE" />
          <attribute name="LCSC" value="C107365" />
        </part>
        <part name="R416" library="ASTRA" deviceset="R_R0402" device="" value="330R 1%">
          <attribute name="MPN" value="0402WGF3300TCE" />
          <attribute name="LCSC" value="C25104" />
        </part>
        <part name="R419" library="ASTRA" deviceset="R_R0402" device="" value="3.3k 1%">
          <attribute name="MPN" value="0402WGF3301TCE" />
          <attribute name="LCSC" value="C25890" />
        </part>
        <part name="U407" library="ASTRA" deviceset="TPS22919DCKR" device="" value="Gated battery sample">
          <attribute name="MPN" value="TPS22919DCKR" />
          <attribute name="LCSC" value="C2149796" />
        </part>
        <part name="C415" library="ASTRA" deviceset="C_C0402" device="" value="1u 25V">
          <attribute name="MPN" value="CL05A105KA5NQNC" />
          <attribute name="LCSC" value="C52923" />
        </part>
        <part name="R420" library="ASTRA" deviceset="R_R0402" device="" value="10k 1%">
          <attribute name="MPN" value="0402WGF1002TCE" />
          <attribute name="LCSC" value="C25744" />
        </part>
        <part name="R421" library="ASTRA" deviceset="R_R0402" device="" value="10k 1%">
          <attribute name="MPN" value="0402WGF1002TCE" />
          <attribute name="LCSC" value="C25744" />
        </part>
        <part name="C416" library="ASTRA" deviceset="C_C0402" device="" value="1n 50V">
          <attribute name="MPN" value="0402B102K500NT" />
          <attribute name="LCSC" value="C1523" />
        </part>
        <part name="U408" library="ASTRA" deviceset="SN74AUP1G97DCKR" device="" value="Schmitt ADC interlock">
          <attribute name="MPN" value="SN74AUP1G97DCKR" />
          <attribute name="LCSC" value="C2682139" />
        </part>
        <part name="C417" library="ASTRA" deviceset="C_C0402" device="" value="100n 16V">
          <attribute name="MPN" value="CL05B104KO5NNNC" />
          <attribute name="LCSC" value="C1525" />
        </part>
        <part name="R422" library="ASTRA" deviceset="R_R0402" device="" value="10k 1%">
          <attribute name="MPN" value="0402WGF1002TCE" />
          <attribute name="LCSC" value="C25744" />
        </part>
        <part name="R423" library="ASTRA" deviceset="R_R0402" device="" value="100k 1%">
          <attribute name="MPN" value="0402WGF1003TCE" />
          <attribute name="LCSC" value="C25741" />
        </part>
        <part name="R424" library="ASTRA" deviceset="R_R0402" device="" value="10k 1%">
          <attribute name="MPN" value="0402WGF1002TCE" />
          <attribute name="LCSC" value="C25744" />
        </part>
        <part name="C418" library="ASTRA" deviceset="C_C0402" device="" value="10n 50V">
          <attribute name="MPN" value="CL05B103KB5NNNC" />
          <attribute name="LCSC" value="C15195" />
        </part>
      </parts>
      <sheets>
        <sheet>
          <description>System architecture and design index</description>
          <plain>
            <wire x1="0" y1="0" x2="406.4" y2="0" width="0.25" layer="97" />
            <wire x1="406.4" y1="0" x2="406.4" y2="274.32" width="0.25" layer="97" />
            <wire x1="406.4" y1="274.32" x2="0" y2="274.32" width="0.25" layer="97" />
            <wire x1="0" y1="274.32" x2="0" y2="0" width="0.25" layer="97" />
            <text x="8" y="264" size="1.9" layer="97" font="proportional">ASTRA   /   ENGINEERING SCHEMATIC</text>
            <text x="8" y="251" size="5.1" layer="97" font="proportional">Solar e-ink weather station</text>
            <text x="8" y="241" size="2.7" layer="97" font="proportional">System architecture</text>
            <text x="350" y="264" size="1.9" layer="97" font="proportional">PROTOTYPE  A</text>
            <wire x1="8" y1="236" x2="398.4" y2="236" width="0.2" layer="97" />
            <wire x1="9" y1="198" x2="69" y2="198" width="0.25" layer="97" />
            <wire x1="69" y1="198" x2="69" y2="224" width="0.25" layer="97" />
            <wire x1="69" y1="224" x2="9" y2="224" width="0.25" layer="97" />
            <wire x1="9" y1="224" x2="9" y2="198" width="0.25" layer="97" />
            <text x="12" y="218" size="2.2" layer="97" font="proportional">Solar input</text>
            <text x="12" y="212" size="1.72" layer="97" font="proportional">5 V / 230 mA at MPP</text>
            <text x="12" y="207.8" size="1.72" layer="97" font="proportional">J103 wire lands</text>
            <wire x1="9" y1="156" x2="69" y2="156" width="0.25" layer="97" />
            <wire x1="69" y1="156" x2="69" y2="182" width="0.25" layer="97" />
            <wire x1="69" y1="182" x2="9" y2="182" width="0.25" layer="97" />
            <wire x1="9" y1="182" x2="9" y2="156" width="0.25" layer="97" />
            <text x="12" y="176" size="2.2" layer="97" font="proportional">USB-C input</text>
            <text x="12" y="170" size="1.72" layer="97" font="proportional">5 V sink, two Rd resistors</text>
            <text x="12" y="165.8" size="1.72" layer="97" font="proportional">J101 charge input</text>
            <wire x1="86" y1="198" x2="153" y2="198" width="0.25" layer="97" />
            <wire x1="153" y1="198" x2="153" y2="224" width="0.25" layer="97" />
            <wire x1="153" y1="224" x2="86" y2="224" width="0.25" layer="97" />
            <wire x1="86" y1="224" x2="86" y2="198" width="0.25" layer="97" />
            <text x="89" y="218" size="2.2" layer="97" font="proportional">SPV1050</text>
            <text x="89" y="212" size="1.72" layer="97" font="proportional">PV tracking and storage</text>
            <text x="89" y="207.8" size="1.72" layer="97" font="proportional">PV_VALID to source switch</text>
            <wire x1="171" y1="171" x2="235" y2="171" width="0.25" layer="97" />
            <wire x1="235" y1="171" x2="235" y2="198" width="0.25" layer="97" />
            <wire x1="235" y1="198" x2="171" y2="198" width="0.25" layer="97" />
            <wire x1="171" y1="198" x2="171" y2="171" width="0.25" layer="97" />
            <text x="174" y="192" size="2.2" layer="97" font="proportional">TPS2116</text>
            <text x="174" y="186" size="1.72" layer="97" font="proportional">Priority source selection</text>
            <text x="174" y="181.8" size="1.72" layer="97" font="proportional">USB priority</text>
            <wire x1="250" y1="171" x2="315" y2="171" width="0.25" layer="97" />
            <wire x1="315" y1="171" x2="315" y2="198" width="0.25" layer="97" />
            <wire x1="315" y1="198" x2="250" y2="198" width="0.25" layer="97" />
            <wire x1="250" y1="198" x2="250" y2="171" width="0.25" layer="97" />
            <text x="253" y="192" size="2.2" layer="97" font="proportional">BQ24074</text>
            <text x="253" y="186" size="1.72" layer="97" font="proportional">Power path and charging</text>
            <text x="253" y="181.8" size="1.72" layer="97" font="proportional">Pack NTC window</text>
            <wire x1="330" y1="171" x2="396" y2="171" width="0.25" layer="97" />
            <wire x1="396" y1="171" x2="396" y2="198" width="0.25" layer="97" />
            <wire x1="396" y1="198" x2="330" y2="198" width="0.25" layer="97" />
            <wire x1="330" y1="198" x2="330" y2="171" width="0.25" layer="97" />
            <text x="333" y="192" size="2.2" layer="97" font="proportional">Protected LiPo</text>
            <text x="333" y="186" size="1.72" layer="97" font="proportional">250 mAh / 1S</text>
            <text x="333" y="181.8" size="1.72" layer="97" font="proportional">J102 keyed 3-wire pack</text>
            <wire x1="69" y1="211" x2="86" y2="211" width="0.32" layer="97" />
            <wire x1="86" y1="211" x2="83.6" y2="210" width="0.32" layer="97" />
            <wire x1="86" y1="211" x2="83.6" y2="212" width="0.32" layer="97" />
            <wire x1="153" y1="211" x2="162" y2="211" width="0.32" layer="97" />
            <wire x1="162" y1="211" x2="162" y2="191" width="0.32" layer="97" />
            <wire x1="162" y1="191" x2="171" y2="191" width="0.32" layer="97" />
            <wire x1="171" y1="191" x2="168.6" y2="190" width="0.32" layer="97" />
            <wire x1="171" y1="191" x2="168.6" y2="192" width="0.32" layer="97" />
            <wire x1="69" y1="168" x2="161" y2="168" width="0.32" layer="97" />
            <wire x1="161" y1="168" x2="161" y2="179" width="0.32" layer="97" />
            <wire x1="161" y1="179" x2="171" y2="179" width="0.32" layer="97" />
            <wire x1="171" y1="179" x2="168.6" y2="178" width="0.32" layer="97" />
            <wire x1="171" y1="179" x2="168.6" y2="180" width="0.32" layer="97" />
            <wire x1="235" y1="184" x2="250" y2="184" width="0.32" layer="97" />
            <wire x1="250" y1="184" x2="247.6" y2="183" width="0.32" layer="97" />
            <wire x1="250" y1="184" x2="247.6" y2="185" width="0.32" layer="97" />
            <wire x1="315" y1="187" x2="330" y2="187" width="0.32" layer="97" />
            <wire x1="330" y1="187" x2="327.6" y2="186" width="0.32" layer="97" />
            <wire x1="330" y1="187" x2="327.6" y2="188" width="0.32" layer="97" />
            <wire x1="330" y1="178" x2="315" y2="178" width="0.32" layer="97" />
            <wire x1="315" y1="178" x2="317.4" y2="179" width="0.32" layer="97" />
            <wire x1="315" y1="178" x2="317.4" y2="177" width="0.32" layer="97" />
            <wire x1="246" y1="118" x2="316" y2="118" width="0.25" layer="97" />
            <wire x1="316" y1="118" x2="316" y2="146" width="0.25" layer="97" />
            <wire x1="316" y1="146" x2="246" y2="146" width="0.25" layer="97" />
            <wire x1="246" y1="146" x2="246" y2="118" width="0.25" layer="97" />
            <text x="249" y="140" size="2.2" layer="97" font="proportional">RT6160A</text>
            <text x="249" y="134" size="1.72" layer="97" font="proportional">Switched 3.3 V VMAIN</text>
            <text x="249" y="129.8" size="1.72" layer="97" font="proportional">Enable = MAIN_EN</text>
            <wire x1="121" y1="118" x2="200" y2="118" width="0.25" layer="97" />
            <wire x1="200" y1="118" x2="200" y2="146" width="0.25" layer="97" />
            <wire x1="200" y1="146" x2="121" y2="146" width="0.25" layer="97" />
            <wire x1="121" y1="146" x2="121" y2="118" width="0.25" layer="97" />
            <text x="124" y="140" size="2.2" layer="97" font="proportional">Always-on domain</text>
            <text x="124" y="134" size="1.72" layer="97" font="proportional">TPS7A02, PCF85063A, TPL5111</text>
            <text x="124" y="129.8" size="1.72" layer="97" font="proportional">Alarm or pushbutton starts VMAIN</text>
            <wire x1="282" y1="171" x2="282" y2="146" width="0.32" layer="97" />
            <wire x1="282" y1="146" x2="281" y2="148.4" width="0.32" layer="97" />
            <wire x1="282" y1="146" x2="283" y2="148.4" width="0.32" layer="97" />
            <wire x1="282" y1="157" x2="160" y2="157" width="0.32" layer="97" />
            <wire x1="160" y1="157" x2="160" y2="146" width="0.32" layer="97" />
            <wire x1="160" y1="146" x2="159" y2="148.4" width="0.32" layer="97" />
            <wire x1="160" y1="146" x2="161" y2="148.4" width="0.32" layer="97" />
            <wire x1="200" y1="129" x2="246" y2="129" width="0.32" layer="97" />
            <wire x1="246" y1="129" x2="243.6" y2="128" width="0.32" layer="97" />
            <wire x1="246" y1="129" x2="243.6" y2="130" width="0.32" layer="97" />
            <text x="201" y="158" size="1.8" layer="97" font="proportional">SYS_AON</text>
            <text x="211" y="131" size="1.8" layer="97" font="proportional">MAIN_EN</text>
            <wire x1="80" y1="66" x2="156" y2="66" width="0.25" layer="97" />
            <wire x1="156" y1="66" x2="156" y2="95" width="0.25" layer="97" />
            <wire x1="156" y1="95" x2="80" y2="95" width="0.25" layer="97" />
            <wire x1="80" y1="95" x2="80" y2="66" width="0.25" layer="97" />
            <text x="83" y="89" size="2.2" layer="97" font="proportional">BME280 and controls</text>
            <text x="83" y="83" size="1.72" layer="97" font="proportional">I2C 0x76, three button inputs</text>
            <text x="83" y="78.8" size="1.72" layer="97" font="proportional">Switched battery measurement</text>
            <wire x1="203" y1="66" x2="285" y2="66" width="0.25" layer="97" />
            <wire x1="285" y1="66" x2="285" y2="95" width="0.25" layer="97" />
            <wire x1="285" y1="95" x2="203" y2="95" width="0.25" layer="97" />
            <wire x1="203" y1="95" x2="203" y2="66" width="0.25" layer="97" />
            <text x="206" y="89" size="2.2" layer="97" font="proportional">Ebyte E73 module</text>
            <text x="206" y="83" size="1.72" layer="97" font="proportional">nRF54L15-QFAA, 2.4 GHz</text>
            <text x="206" y="78.8" size="1.72" layer="97" font="proportional">Retained RRAM journal and SWD</text>
            <wire x1="323" y1="66" x2="396" y2="66" width="0.25" layer="97" />
            <wire x1="396" y1="66" x2="396" y2="95" width="0.25" layer="97" />
            <wire x1="396" y1="95" x2="323" y2="95" width="0.25" layer="97" />
            <wire x1="323" y1="95" x2="323" y2="66" width="0.25" layer="97" />
            <text x="326" y="89" size="2.2" layer="97" font="proportional">Waveshare 4.2 V2</text>
            <text x="326" y="83" size="1.72" layer="97" font="proportional">SSD1683, 400 x 300, FPC24</text>
            <text x="326" y="78.8" size="1.72" layer="97" font="proportional">Switched bias pump and SPI</text>
            <wire x1="256" y1="118" x2="256" y2="95" width="0.32" layer="97" />
            <wire x1="256" y1="95" x2="255" y2="97.4" width="0.32" layer="97" />
            <wire x1="256" y1="95" x2="257" y2="97.4" width="0.32" layer="97" />
            <wire x1="156" y1="82" x2="203" y2="82" width="0.32" layer="97" />
            <wire x1="203" y1="82" x2="200.6" y2="81" width="0.32" layer="97" />
            <wire x1="203" y1="82" x2="200.6" y2="83" width="0.32" layer="97" />
            <wire x1="285" y1="82" x2="323" y2="82" width="0.32" layer="97" />
            <wire x1="323" y1="82" x2="320.6" y2="81" width="0.32" layer="97" />
            <wire x1="323" y1="82" x2="320.6" y2="83" width="0.32" layer="97" />
            <text x="164" y="84" size="1.7" layer="97" font="proportional">SDA / SCL</text>
            <text x="291" y="84" size="1.7" layer="97" font="proportional">4-wire SPI</text>
            <text x="9" y="48" size="2.8" layer="97" font="proportional">Wake sequence</text>
            <text x="9" y="40" size="1.9" layer="97" font="proportional">Read RTC, keys and BME280. Restore both controller image planes for a valid differential update.</text>
            <text x="9" y="34" size="1.9" layer="97" font="proportional">A failed or interrupted optical update requires a full refresh. Commit the new state before asserting TIMER_DONE.</text>
            <text x="9" y="21" size="2.3" layer="97" font="proportional">Sheet index</text>
            <text x="9" y="13" size="1.75" layer="97" font="proportional">2-3  Energy harvesting and power path     |     4  Radio and programming     |     5  Electrophoretic display     |     6-7  Timekeeping, sensing and controls</text>
          </plain>
          <instances />
          <busses />
          <nets />
        </sheet>
        <sheet>
          <description>USB-C, battery charging and system rail</description>
          <plain>
            <wire x1="0" y1="0" x2="406.4" y2="0" width="0.25" layer="97" />
            <wire x1="406.4" y1="0" x2="406.4" y2="274.32" width="0.25" layer="97" />
            <wire x1="406.4" y1="274.32" x2="0" y2="274.32" width="0.25" layer="97" />
            <wire x1="0" y1="274.32" x2="0" y2="0" width="0.25" layer="97" />
            <text x="7.62" y="264.16" size="1.65" layer="97" font="proportional">ASTRA   /   SOLAR WEATHER STATION</text>
            <text x="7.62" y="252.73" size="4.1" layer="97" font="proportional">USB-C, battery charging and system rail</text>
            <text x="7.62" y="247.396" size="1.6" layer="97" font="proportional">USB priority, protected LiPo power path and switched 3.3 V</text>
            <text x="398.78" y="264.16" size="1.65" layer="97" font="proportional" align="bottom-right">PROTOTYPE  A  /  SHEET  02  OF  07</text>
            <wire x1="7.62" y1="244.602" x2="398.78" y2="244.602" width="0.2" layer="97" />
            <text x="7.62" y="4.445" size="1.55" layer="97" font="proportional">Identical net labels connect across sheets.   |   Pin numbers refer to the top-side package.</text>
            <text x="7.62" y="238.76" size="1.9" layer="97" font="proportional">USB-C AND INPUT SELECTION</text>
            <text x="142.24" y="238.76" size="1.9" layer="97" font="proportional">USB-C AND INPUT SELECTION</text>
            <text x="276.86" y="238.76" size="1.9" layer="97" font="proportional">PROTECTED CELL CHARGER</text>
            <text x="142.24" y="207.772" size="1.9" layer="97" font="proportional">SWITCHED 3.3 V</text>
          </plain>
          <instances>
            <instance part="J101" gate="G$1" x="68.58" y="208.28" rot="R0" smashed="yes">
              <attribute name="NAME" x="53.34" y="225.044" size="2.25" layer="95" font="proportional" rot="R0" />
              <attribute name="VALUE" x="53.34" y="221.5388" size="1.7" layer="96" font="proportional" rot="R0" />
            </instance>
            <instance part="U103" gate="G$1" x="68.58" y="167.64" rot="R0" smashed="yes">
              <attribute name="NAME" x="58.42" y="181.864" size="2.25" layer="95" font="proportional" rot="R0" />
              <attribute name="VALUE" x="58.42" y="178.3588" size="1.7" layer="96" font="proportional" rot="R0" />
            </instance>
            <instance part="D101" gate="G$1" x="68.58" y="132.08" rot="R0" smashed="yes">
              <attribute name="NAME" x="58.42" y="143.764" size="2.25" layer="95" font="proportional" rot="R0" />
              <attribute name="VALUE" x="58.42" y="140.2588" size="1.7" layer="96" font="proportional" rot="R0" />
            </instance>
            <instance part="C102" gate="G$1" x="68.58" y="109.22" rot="R0" smashed="yes">
              <attribute name="NAME" x="68.58" y="112.0648" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="68.58" y="107.061" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="R101" gate="G$1" x="68.58" y="93.98" rot="R0" smashed="yes">
              <attribute name="NAME" x="68.58" y="96.8248" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="68.58" y="91.821" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="R102" gate="G$1" x="68.58" y="78.74" rot="R0" smashed="yes">
              <attribute name="NAME" x="68.58" y="81.5848" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="68.58" y="76.581" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="R104" gate="G$1" x="68.58" y="63.5" rot="R0" smashed="yes">
              <attribute name="NAME" x="68.58" y="66.3448" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="68.58" y="61.341" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="C101" gate="G$1" x="68.58" y="48.26" rot="R0" smashed="yes">
              <attribute name="NAME" x="68.58" y="51.1048" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="68.58" y="46.101" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="R103" gate="G$1" x="68.58" y="33.02" rot="R0" smashed="yes">
              <attribute name="NAME" x="68.58" y="35.8648" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="68.58" y="30.861" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="TP102" gate="G$1" x="203.2" y="223.52" rot="R0" smashed="yes">
              <attribute name="NAME" x="203.2" y="226.3648" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="203.2" y="221.361" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="U102" gate="G$1" x="337.82" y="124.46" rot="R0" smashed="yes">
              <attribute name="NAME" x="322.58" y="152.4" size="2.25" layer="95" font="proportional" rot="R0" align="bottom-left" />
              <attribute name="VALUE" x="322.58" y="147.32" size="1.7" layer="96" font="proportional" rot="R0" align="bottom-left" />
            </instance>
            <instance part="J102" gate="G$1" x="314.96" y="198.12" rot="R0" smashed="yes">
              <attribute name="NAME" x="299.72" y="213.36" size="2.25" layer="95" font="proportional" rot="R0" align="bottom-left" />
              <attribute name="VALUE" x="299.72" y="208.28" size="1.7" layer="96" font="proportional" rot="R0" align="bottom-left" />
            </instance>
            <instance part="R112" gate="G$1" x="307.34" y="160.02" rot="R90" smashed="yes">
              <attribute name="NAME" x="309.88" y="162.56" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="309.88" y="157.48" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="R113" gate="G$1" x="294.64" y="66.04" rot="R270" smashed="yes">
              <attribute name="NAME" x="297.18" y="68.58" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="297.18" y="63.5" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="R114" gate="G$1" x="320.04" y="66.04" rot="R270" smashed="yes">
              <attribute name="NAME" x="322.58" y="68.58" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="322.58" y="63.5" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="R123" gate="G$1" x="345.44" y="66.04" rot="R270" smashed="yes">
              <attribute name="NAME" x="347.98" y="68.58" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="347.98" y="63.5" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="R115" gate="G$1" x="370.84" y="66.04" rot="R270" smashed="yes">
              <attribute name="NAME" x="373.38" y="68.58" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="373.38" y="63.5" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="C109" gate="G$1" x="289.56" y="119.38" rot="R270" smashed="yes">
              <attribute name="NAME" x="292.1" y="121.92" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="292.1" y="116.84" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="C110" gate="G$1" x="373.38" y="154.94" rot="R90" smashed="yes">
              <attribute name="NAME" x="375.92" y="157.48" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="375.92" y="152.4" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="C111" gate="G$1" x="393.7" y="104.14" rot="R270" smashed="yes">
              <attribute name="NAME" x="380.238" y="106.172" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="380.238" y="101.854" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="TP103" gate="G$1" x="297.18" y="167.64" rot="R0" smashed="yes">
              <attribute name="NAME" x="289.56" y="173.99" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="289.56" y="162.56" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="TP104" gate="G$1" x="391.16" y="137.16" rot="R0" smashed="yes">
              <attribute name="NAME" x="386.08" y="142.24" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="386.08" y="133.096" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="TP105" gate="G$1" x="386.08" y="48.26" rot="R0" smashed="yes">
              <attribute name="NAME" x="381" y="53.34" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="381" y="43.18" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="U104" gate="G$1" x="203.2" y="152.4" rot="R0" smashed="yes">
              <attribute name="NAME" x="187.96" y="177.8" size="2.25" layer="95" font="proportional" rot="R0" align="bottom-left" />
              <attribute name="VALUE" x="187.96" y="172.72" size="1.7" layer="96" font="proportional" rot="R0" align="bottom-left" />
            </instance>
            <instance part="L102" gate="G$1" x="203.2" y="104.14" rot="R0" smashed="yes">
              <attribute name="NAME" x="198.12" y="109.22" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="193.04" y="96.52" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="R122" gate="G$1" x="203.2" y="190.5" rot="R0" smashed="yes">
              <attribute name="NAME" x="198.12" y="195.58" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="198.12" y="185.42" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="R124" gate="G$1" x="162.56" y="175.26" rot="R180" smashed="yes">
              <attribute name="NAME" x="157.48" y="180.34" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="149.86" y="171.45" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="R125" gate="G$1" x="241.3" y="137.16" rot="R0" smashed="yes">
              <attribute name="NAME" x="236.982" y="139.192" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="232.41" y="133.858" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="C113" gate="G$1" x="149.86" y="152.4" rot="R270" smashed="yes">
              <attribute name="NAME" x="152.4" y="153.67" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="152.4" y="149.86" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="C114" gate="G$1" x="165.1" y="152.4" rot="R270" smashed="yes">
              <attribute name="NAME" x="167.64" y="153.67" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="167.64" y="149.86" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="C115" gate="G$1" x="231.14" y="124.46" rot="R270" smashed="yes">
              <attribute name="NAME" x="233.68" y="127" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="233.68" y="121.92" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="C116" gate="G$1" x="246.38" y="124.46" rot="R270" smashed="yes">
              <attribute name="NAME" x="248.92" y="125.984" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="248.92" y="120.904" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="TP106" gate="G$1" x="259.08" y="137.16" rot="R0" smashed="yes">
              <attribute name="NAME" x="251.46" y="133.858" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="251.46" y="130.302" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
          </instances>
          <busses />
          <nets>
            <net name="CHG_IN" class="0">
              <segment>
                <pinref part="U103" gate="G$1" pin="VOUT" />
                <wire x1="55.88" y1="170.18" x2="7.62" y2="170.18" width="0.1524" layer="91" />
                <label x="7.62" y="170.18" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C102" gate="G$1" pin="1" />
                <wire x1="60.96" y1="109.22" x2="7.62" y2="109.22" width="0.1524" layer="91" />
                <label x="7.62" y="109.22" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="TP102" gate="G$1" pin="1" />
                <wire x1="195.58" y1="223.52" x2="142.24" y2="223.52" width="0.1524" layer="91" />
                <label x="142.24" y="223.52" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U102" gate="G$1" pin="IN" />
                <wire x1="355.6" y1="127" x2="373.38" y2="127" width="0.1524" layer="91" />
                <wire x1="373.38" y1="127" x2="393.7" y2="127" width="0.1524" layer="91" />
                <pinref part="C111" gate="G$1" pin="1" />
                <wire x1="393.7" y1="111.76" x2="393.7" y2="127" width="0.1524" layer="91" />
                <label x="373.38" y="127" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="GND" class="0">
              <segment>
                <pinref part="J101" gate="G$1" pin="GND" />
                <wire x1="50.8" y1="208.28" x2="7.62" y2="208.28" width="0.1524" layer="91" />
                <label x="7.62" y="208.28" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="J101" gate="G$1" pin="GND@B12" />
                <wire x1="86.36" y1="218.44" x2="127" y2="218.44" width="0.1524" layer="91" />
                <label x="88.9" y="218.44" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="J101" gate="G$1" pin="GND@SH1" />
                <wire x1="86.36" y1="213.36" x2="127" y2="213.36" width="0.1524" layer="91" />
                <label x="88.9" y="213.36" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="J101" gate="G$1" pin="GND@SH2" />
                <wire x1="86.36" y1="208.28" x2="127" y2="208.28" width="0.1524" layer="91" />
                <label x="88.9" y="208.28" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="J101" gate="G$1" pin="GND@SH3" />
                <wire x1="86.36" y1="203.2" x2="127" y2="203.2" width="0.1524" layer="91" />
                <label x="88.9" y="203.2" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="J101" gate="G$1" pin="GND@SH4" />
                <wire x1="86.36" y1="198.12" x2="127" y2="198.12" width="0.1524" layer="91" />
                <label x="88.9" y="198.12" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U103" gate="G$1" pin="GND" />
                <wire x1="55.88" y1="175.26" x2="7.62" y2="175.26" width="0.1524" layer="91" />
                <label x="7.62" y="175.26" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="D101" gate="G$1" pin="GND" />
                <wire x1="55.88" y1="132.08" x2="7.62" y2="132.08" width="0.1524" layer="91" />
                <label x="7.62" y="132.08" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C102" gate="G$1" pin="2" />
                <wire x1="76.2" y1="109.22" x2="127" y2="109.22" width="0.1524" layer="91" />
                <wire x1="127" y1="109.22" x2="127" y2="93.98" width="0.1524" layer="91" />
                <pinref part="R101" gate="G$1" pin="2" />
                <wire x1="76.2" y1="93.98" x2="127" y2="93.98" width="0.1524" layer="91" />
                <wire x1="127" y1="93.98" x2="127" y2="78.74" width="0.1524" layer="91" />
                <junction x="127" y="93.98" />
                <pinref part="R102" gate="G$1" pin="2" />
                <wire x1="76.2" y1="78.74" x2="127" y2="78.74" width="0.1524" layer="91" />
                <wire x1="127" y1="78.74" x2="127" y2="63.5" width="0.1524" layer="91" />
                <junction x="127" y="78.74" />
                <pinref part="R104" gate="G$1" pin="2" />
                <wire x1="76.2" y1="63.5" x2="127" y2="63.5" width="0.1524" layer="91" />
                <wire x1="127" y1="63.5" x2="127" y2="48.26" width="0.1524" layer="91" />
                <junction x="127" y="63.5" />
                <pinref part="C101" gate="G$1" pin="2" />
                <wire x1="76.2" y1="48.26" x2="127" y2="48.26" width="0.1524" layer="91" />
                <label x="78.74" y="109.22" size="1.55" layer="95" />
              </segment>
              <segment>
                <wire x1="284.48" y1="203.2" x2="284.48" y2="223.52" width="0.1524" layer="91" />
                <wire x1="284.48" y1="203.2" x2="294.64" y2="203.2" width="0.1524" layer="91" />
                <wire x1="284.48" y1="223.52" x2="327.66" y2="223.52" width="0.1524" layer="91" />
                <pinref part="J102" gate="G$1" pin="PACK_NEG" />
                <wire x1="327.66" y1="223.52" x2="340.36" y2="223.52" width="0.1524" layer="91" />
                <pinref part="J102" gate="G$1" pin="MT2" />
                <wire x1="335.28" y1="198.12" x2="340.36" y2="198.12" width="0.1524" layer="91" />
                <pinref part="J102" gate="G$1" pin="MT1" />
                <wire x1="335.28" y1="203.2" x2="340.36" y2="203.2" width="0.1524" layer="91" />
                <wire x1="340.36" y1="198.12" x2="340.36" y2="203.2" width="0.1524" layer="91" />
                <wire x1="340.36" y1="203.2" x2="340.36" y2="223.52" width="0.1524" layer="91" />
                <junction x="340.36" y="203.2" />
                <label x="327.66" y="223.52" size="1.55" layer="95" />
              </segment>
              <segment>
                <wire x1="289.56" y1="48.26" x2="289.56" y2="104.14" width="0.1524" layer="91" />
                <wire x1="289.56" y1="48.26" x2="294.64" y2="48.26" width="0.1524" layer="91" />
                <wire x1="289.56" y1="104.14" x2="289.56" y2="111.76" width="0.1524" layer="91" />
                <wire x1="289.56" y1="104.14" x2="309.88" y2="104.14" width="0.1524" layer="91" />
                <junction x="289.56" y="104.14" />
                <pinref part="C109" gate="G$1" pin="2" />
                <wire x1="294.64" y1="48.26" x2="294.64" y2="58.42" width="0.1524" layer="91" />
                <wire x1="294.64" y1="48.26" x2="320.04" y2="48.26" width="0.1524" layer="91" />
                <junction x="294.64" y="48.26" />
                <pinref part="R113" gate="G$1" pin="2" />
                <wire x1="309.88" y1="104.14" x2="309.88" y2="106.68" width="0.1524" layer="91" />
                <wire x1="309.88" y1="106.68" x2="309.88" y2="116.84" width="0.1524" layer="91" />
                <wire x1="309.88" y1="106.68" x2="320.04" y2="106.68" width="0.1524" layer="91" />
                <junction x="309.88" y="106.68" />
                <wire x1="309.88" y1="116.84" x2="309.88" y2="121.92" width="0.1524" layer="91" />
                <wire x1="309.88" y1="116.84" x2="320.04" y2="116.84" width="0.1524" layer="91" />
                <junction x="309.88" y="116.84" />
                <wire x1="309.88" y1="121.92" x2="320.04" y2="121.92" width="0.1524" layer="91" />
                <wire x1="320.04" y1="48.26" x2="320.04" y2="58.42" width="0.1524" layer="91" />
                <wire x1="320.04" y1="48.26" x2="345.44" y2="48.26" width="0.1524" layer="91" />
                <junction x="320.04" y="48.26" />
                <pinref part="R114" gate="G$1" pin="2" />
                <pinref part="U102" gate="G$1" pin="VSS" />
                <pinref part="U102" gate="G$1" pin="EN1" />
                <pinref part="U102" gate="G$1" pin="EN2" />
                <wire x1="345.44" y1="48.26" x2="345.44" y2="58.42" width="0.1524" layer="91" />
                <wire x1="345.44" y1="48.26" x2="370.84" y2="48.26" width="0.1524" layer="91" />
                <junction x="345.44" y="48.26" />
                <pinref part="R123" gate="G$1" pin="2" />
                <wire x1="370.84" y1="48.26" x2="370.84" y2="58.42" width="0.1524" layer="91" />
                <wire x1="370.84" y1="48.26" x2="378.46" y2="48.26" width="0.1524" layer="91" />
                <junction x="370.84" y="48.26" />
                <pinref part="R115" gate="G$1" pin="2" />
                <pinref part="TP105" gate="G$1" pin="1" />
                <label x="309.88" y="104.14" size="1.55" layer="95" />
                <label x="345.44" y="48.26" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R112" gate="G$1" pin="2" />
                <wire x1="307.34" y1="167.64" x2="307.34" y2="172.72" width="0.1524" layer="91" />
                <wire x1="307.34" y1="172.72" x2="312.42" y2="172.72" width="0.1524" layer="91" />
                <label x="312.42" y="172.72" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U102" gate="G$1" pin="EP" />
                <wire x1="355.6" y1="106.68" x2="363.22" y2="106.68" width="0.1524" layer="91" />
                <wire x1="363.22" y1="96.52" x2="363.22" y2="106.68" width="0.1524" layer="91" />
                <label x="363.22" y="96.52" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C110" gate="G$1" pin="2" />
                <wire x1="373.38" y1="162.56" x2="373.38" y2="172.72" width="0.1524" layer="91" />
                <wire x1="373.38" y1="172.72" x2="381" y2="172.72" width="0.1524" layer="91" />
                <label x="381" y="172.72" size="1.55" layer="95" />
              </segment>
              <segment>
                <wire x1="386.08" y1="88.9" x2="393.7" y2="88.9" width="0.1524" layer="91" />
                <wire x1="393.7" y1="88.9" x2="393.7" y2="96.52" width="0.1524" layer="91" />
                <pinref part="C111" gate="G$1" pin="2" />
                <label x="386.08" y="88.9" size="1.55" layer="95" />
              </segment>
              <segment>
                <wire x1="149.86" y1="137.16" x2="149.86" y2="144.78" width="0.1524" layer="91" />
                <wire x1="149.86" y1="137.16" x2="157.48" y2="137.16" width="0.1524" layer="91" />
                <pinref part="C113" gate="G$1" pin="2" />
                <wire x1="157.48" y1="137.16" x2="165.1" y2="137.16" width="0.1524" layer="91" />
                <wire x1="165.1" y1="137.16" x2="165.1" y2="144.78" width="0.1524" layer="91" />
                <pinref part="C114" gate="G$1" pin="2" />
                <label x="157.48" y="137.16" size="1.55" layer="95" />
              </segment>
              <segment>
                <wire x1="175.26" y1="152.4" x2="185.42" y2="152.4" width="0.1524" layer="91" />
                <pinref part="U104" gate="G$1" pin="VSEL" />
                <label x="175.26" y="152.4" size="1.55" layer="95" />
              </segment>
              <segment>
                <wire x1="182.88" y1="121.92" x2="182.88" y2="137.16" width="0.1524" layer="91" />
                <wire x1="182.88" y1="137.16" x2="185.42" y2="137.16" width="0.1524" layer="91" />
                <pinref part="U104" gate="G$1" pin="AGND" />
                <label x="182.88" y="121.92" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R122" gate="G$1" pin="2" />
                <wire x1="210.82" y1="190.5" x2="223.52" y2="190.5" width="0.1524" layer="91" />
                <label x="223.52" y="190.5" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U104" gate="G$1" pin="PGND_2" />
                <wire x1="220.98" y1="162.56" x2="233.68" y2="162.56" width="0.1524" layer="91" />
                <pinref part="U104" gate="G$1" pin="PGND_1" />
                <wire x1="220.98" y1="167.64" x2="233.68" y2="167.64" width="0.1524" layer="91" />
                <wire x1="233.68" y1="162.56" x2="233.68" y2="167.64" width="0.1524" layer="91" />
                <wire x1="233.68" y1="167.64" x2="241.3" y2="167.64" width="0.1524" layer="91" />
                <junction x="233.68" y="167.64" />
                <wire x1="241.3" y1="167.64" x2="251.46" y2="167.64" width="0.1524" layer="91" />
                <label x="241.3" y="167.64" size="1.55" layer="95" />
              </segment>
              <segment>
                <wire x1="231.14" y1="111.76" x2="231.14" y2="116.84" width="0.1524" layer="91" />
                <wire x1="231.14" y1="111.76" x2="236.22" y2="111.76" width="0.1524" layer="91" />
                <pinref part="C115" gate="G$1" pin="2" />
                <wire x1="236.22" y1="111.76" x2="246.38" y2="111.76" width="0.1524" layer="91" />
                <wire x1="246.38" y1="111.76" x2="246.38" y2="116.84" width="0.1524" layer="91" />
                <pinref part="C116" gate="G$1" pin="2" />
                <label x="236.22" y="111.76" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="PV_VALID" class="0">
              <segment>
                <pinref part="U103" gate="G$1" pin="VIN2" />
                <wire x1="81.28" y1="170.18" x2="127" y2="170.18" width="0.1524" layer="91" />
                <label x="83.82" y="170.18" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="USB_CC1" class="0">
              <segment>
                <pinref part="J101" gate="G$1" pin="USB_CC1" />
                <wire x1="50.8" y1="218.44" x2="7.62" y2="218.44" width="0.1524" layer="91" />
                <label x="7.62" y="218.44" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="D101" gate="G$1" pin="IO1A" />
                <wire x1="55.88" y1="137.16" x2="7.62" y2="137.16" width="0.1524" layer="91" />
                <label x="7.62" y="137.16" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="D101" gate="G$1" pin="IO1B" />
                <wire x1="81.28" y1="127" x2="127" y2="127" width="0.1524" layer="91" />
                <label x="83.82" y="127" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R101" gate="G$1" pin="1" />
                <wire x1="60.96" y1="93.98" x2="7.62" y2="93.98" width="0.1524" layer="91" />
                <label x="7.62" y="93.98" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="USB_CC2" class="0">
              <segment>
                <pinref part="J101" gate="G$1" pin="USB_CC2" />
                <wire x1="50.8" y1="203.2" x2="7.62" y2="203.2" width="0.1524" layer="91" />
                <label x="7.62" y="203.2" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="D101" gate="G$1" pin="IO2A" />
                <wire x1="55.88" y1="127" x2="7.62" y2="127" width="0.1524" layer="91" />
                <label x="7.62" y="127" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="D101" gate="G$1" pin="IO2B" />
                <wire x1="81.28" y1="137.16" x2="127" y2="137.16" width="0.1524" layer="91" />
                <label x="83.82" y="137.16" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R102" gate="G$1" pin="1" />
                <wire x1="60.96" y1="78.74" x2="7.62" y2="78.74" width="0.1524" layer="91" />
                <label x="7.62" y="78.74" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="USB_PR" class="0">
              <segment>
                <pinref part="U103" gate="G$1" pin="PR1" />
                <wire x1="55.88" y1="160.02" x2="7.62" y2="160.02" width="0.1524" layer="91" />
                <label x="7.62" y="160.02" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R104" gate="G$1" pin="1" />
                <wire x1="60.96" y1="63.5" x2="7.62" y2="63.5" width="0.1524" layer="91" />
                <label x="7.62" y="63.5" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R103" gate="G$1" pin="2" />
                <wire x1="76.2" y1="33.02" x2="127" y2="33.02" width="0.1524" layer="91" />
                <label x="78.74" y="33.02" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="VBUS" class="1">
              <segment>
                <pinref part="J101" gate="G$1" pin="VBUS" />
                <wire x1="50.8" y1="213.36" x2="7.62" y2="213.36" width="0.1524" layer="91" />
                <label x="7.62" y="213.36" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="J101" gate="G$1" pin="VBUS@B9" />
                <wire x1="50.8" y1="198.12" x2="7.62" y2="198.12" width="0.1524" layer="91" />
                <label x="7.62" y="198.12" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U103" gate="G$1" pin="VIN1" />
                <wire x1="55.88" y1="165.1" x2="7.62" y2="165.1" width="0.1524" layer="91" />
                <label x="7.62" y="165.1" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U103" gate="G$1" pin="MODE" />
                <wire x1="81.28" y1="175.26" x2="127" y2="175.26" width="0.1524" layer="91" />
                <label x="83.82" y="175.26" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="D101" gate="G$1" pin="VBUS" />
                <wire x1="81.28" y1="132.08" x2="127" y2="132.08" width="0.1524" layer="91" />
                <label x="83.82" y="132.08" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C101" gate="G$1" pin="1" />
                <wire x1="60.96" y1="48.26" x2="7.62" y2="48.26" width="0.1524" layer="91" />
                <wire x1="7.62" y1="48.26" x2="7.62" y2="33.02" width="0.1524" layer="91" />
                <pinref part="R103" gate="G$1" pin="1" />
                <wire x1="60.96" y1="33.02" x2="7.62" y2="33.02" width="0.1524" layer="91" />
                <label x="7.62" y="48.26" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="VBAT" class="1">
              <segment>
                <wire x1="284.48" y1="137.16" x2="284.48" y2="167.64" width="0.1524" layer="91" />
                <wire x1="284.48" y1="137.16" x2="289.56" y2="137.16" width="0.1524" layer="91" />
                <wire x1="284.48" y1="167.64" x2="284.48" y2="193.04" width="0.1524" layer="91" />
                <wire x1="284.48" y1="167.64" x2="289.56" y2="167.64" width="0.1524" layer="91" />
                <junction x="284.48" y="167.64" />
                <wire x1="284.48" y1="193.04" x2="294.64" y2="193.04" width="0.1524" layer="91" />
                <pinref part="C109" gate="G$1" pin="1" />
                <wire x1="289.56" y1="127" x2="289.56" y2="137.16" width="0.1524" layer="91" />
                <wire x1="289.56" y1="137.16" x2="302.26" y2="137.16" width="0.1524" layer="91" />
                <junction x="289.56" y="137.16" />
                <pinref part="TP103" gate="G$1" pin="1" />
                <pinref part="J102" gate="G$1" pin="PACK_POS" />
                <wire x1="302.26" y1="132.08" x2="302.26" y2="137.16" width="0.1524" layer="91" />
                <wire x1="302.26" y1="132.08" x2="320.04" y2="132.08" width="0.1524" layer="91" />
                <wire x1="302.26" y1="137.16" x2="320.04" y2="137.16" width="0.1524" layer="91" />
                <junction x="302.26" y="137.16" />
                <pinref part="U102" gate="G$1" pin="BAT_2" />
                <pinref part="U102" gate="G$1" pin="BAT_1" />
                <label x="289.56" y="137.16" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="BAT_NTC" class="0">
              <segment>
                <wire x1="279.4" y1="198.12" x2="294.64" y2="198.12" width="0.1524" layer="91" />
                <pinref part="J102" gate="G$1" pin="NTC" />
                <label x="279.4" y="198.12" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="BQ_TS" class="0">
              <segment>
                <wire x1="307.34" y1="142.24" x2="307.34" y2="147.32" width="0.1524" layer="91" />
                <wire x1="307.34" y1="142.24" x2="320.04" y2="142.24" width="0.1524" layer="91" />
                <wire x1="307.34" y1="147.32" x2="307.34" y2="152.4" width="0.1524" layer="91" />
                <pinref part="R112" gate="G$1" pin="1" />
                <pinref part="U102" gate="G$1" pin="TS" />
                <label x="307.34" y="147.32" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="CHG_DISABLE" class="0">
              <segment>
                <wire x1="302.26" y1="127" x2="320.04" y2="127" width="0.1524" layer="91" />
                <pinref part="U102" gate="G$1" pin="CE_N" />
                <label x="302.26" y="127" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="SYS_AON" class="1">
              <segment>
                <pinref part="U102" gate="G$1" pin="OUT" />
                <wire x1="355.6" y1="137.16" x2="358.14" y2="137.16" width="0.1524" layer="91" />
                <wire x1="358.14" y1="137.16" x2="373.38" y2="137.16" width="0.1524" layer="91" />
                <wire x1="373.38" y1="137.16" x2="373.38" y2="147.32" width="0.1524" layer="91" />
                <wire x1="373.38" y1="137.16" x2="383.54" y2="137.16" width="0.1524" layer="91" />
                <junction x="373.38" y="137.16" />
                <pinref part="C110" gate="G$1" pin="1" />
                <pinref part="TP104" gate="G$1" pin="1" />
                <label x="358.14" y="137.16" size="1.55" layer="95" />
              </segment>
              <segment>
                <wire x1="144.78" y1="175.26" x2="154.94" y2="175.26" width="0.1524" layer="91" />
                <pinref part="R124" gate="G$1" pin="2" />
                <label x="144.78" y="175.26" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="BQ_ILIM" class="0">
              <segment>
                <pinref part="R113" gate="G$1" pin="1" />
                <wire x1="294.64" y1="73.66" x2="294.64" y2="83.82" width="0.1524" layer="91" />
                <label x="294.64" y="83.82" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U102" gate="G$1" pin="ILIM" />
                <wire x1="355.6" y1="132.08" x2="363.22" y2="132.08" width="0.1524" layer="91" />
                <wire x1="363.22" y1="132.08" x2="375.92" y2="132.08" width="0.1524" layer="91" />
                <label x="363.22" y="132.08" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="BQ_TMR" class="0">
              <segment>
                <pinref part="R114" gate="G$1" pin="1" />
                <wire x1="320.04" y1="73.66" x2="320.04" y2="83.82" width="0.1524" layer="91" />
                <label x="320.04" y="83.82" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U102" gate="G$1" pin="TMR" />
                <wire x1="355.6" y1="121.92" x2="363.22" y2="121.92" width="0.1524" layer="91" />
                <wire x1="363.22" y1="121.92" x2="375.92" y2="121.92" width="0.1524" layer="91" />
                <label x="363.22" y="121.92" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="BQ_ITERM" class="0">
              <segment>
                <pinref part="R123" gate="G$1" pin="1" />
                <wire x1="345.44" y1="73.66" x2="345.44" y2="83.82" width="0.1524" layer="91" />
                <label x="345.44" y="83.82" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U102" gate="G$1" pin="ITERM" />
                <wire x1="355.6" y1="116.84" x2="363.22" y2="116.84" width="0.1524" layer="91" />
                <wire x1="363.22" y1="116.84" x2="375.92" y2="116.84" width="0.1524" layer="91" />
                <label x="363.22" y="116.84" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="BQ_ISET" class="0">
              <segment>
                <pinref part="U102" gate="G$1" pin="ISET" />
                <wire x1="355.6" y1="111.76" x2="363.22" y2="111.76" width="0.1524" layer="91" />
                <wire x1="363.22" y1="111.76" x2="375.92" y2="111.76" width="0.1524" layer="91" />
                <label x="363.22" y="111.76" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R115" gate="G$1" pin="1" />
                <wire x1="370.84" y1="73.66" x2="370.84" y2="83.82" width="0.1524" layer="91" />
                <label x="370.84" y="83.82" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="MAIN_EN" class="0">
              <segment>
                <wire x1="154.94" y1="190.5" x2="172.72" y2="190.5" width="0.1524" layer="91" />
                <wire x1="172.72" y1="167.64" x2="172.72" y2="190.5" width="0.1524" layer="91" />
                <wire x1="172.72" y1="167.64" x2="185.42" y2="167.64" width="0.1524" layer="91" />
                <wire x1="172.72" y1="190.5" x2="195.58" y2="190.5" width="0.1524" layer="91" />
                <junction x="172.72" y="190.5" />
                <pinref part="U104" gate="G$1" pin="EN" />
                <pinref part="R122" gate="G$1" pin="1" />
                <label x="154.94" y="190.5" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="RT_VIN_LOCAL" class="0">
              <segment>
                <pinref part="C113" gate="G$1" pin="1" />
                <wire x1="149.86" y1="160.02" x2="149.86" y2="162.56" width="0.1524" layer="91" />
                <wire x1="149.86" y1="162.56" x2="165.1" y2="162.56" width="0.1524" layer="91" />
                <pinref part="C114" gate="G$1" pin="1" />
                <wire x1="165.1" y1="160.02" x2="165.1" y2="162.56" width="0.1524" layer="91" />
                <wire x1="165.1" y1="162.56" x2="170.18" y2="162.56" width="0.1524" layer="91" />
                <junction x="165.1" y="162.56" />
                <wire x1="170.18" y1="162.56" x2="170.18" y2="175.26" width="0.1524" layer="91" />
                <wire x1="170.18" y1="162.56" x2="175.26" y2="162.56" width="0.1524" layer="91" />
                <junction x="170.18" y="162.56" />
                <pinref part="R124" gate="G$1" pin="1" />
                <wire x1="175.26" y1="157.48" x2="175.26" y2="162.56" width="0.1524" layer="91" />
                <wire x1="175.26" y1="157.48" x2="185.42" y2="157.48" width="0.1524" layer="91" />
                <wire x1="175.26" y1="162.56" x2="185.42" y2="162.56" width="0.1524" layer="91" />
                <junction x="175.26" y="162.56" />
                <pinref part="U104" gate="G$1" pin="VIN_2" />
                <pinref part="U104" gate="G$1" pin="VIN_1" />
                <label x="149.86" y="162.56" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="RT_SW1" class="0">
              <segment>
                <wire x1="170.18" y1="104.14" x2="170.18" y2="142.24" width="0.1524" layer="91" />
                <wire x1="170.18" y1="104.14" x2="175.26" y2="104.14" width="0.1524" layer="91" />
                <wire x1="170.18" y1="142.24" x2="177.8" y2="142.24" width="0.1524" layer="91" />
                <wire x1="175.26" y1="104.14" x2="195.58" y2="104.14" width="0.1524" layer="91" />
                <wire x1="177.8" y1="142.24" x2="177.8" y2="147.32" width="0.1524" layer="91" />
                <wire x1="177.8" y1="142.24" x2="185.42" y2="142.24" width="0.1524" layer="91" />
                <junction x="177.8" y="142.24" />
                <wire x1="177.8" y1="147.32" x2="185.42" y2="147.32" width="0.1524" layer="91" />
                <pinref part="U104" gate="G$1" pin="SW1_2" />
                <pinref part="U104" gate="G$1" pin="SW1_1" />
                <pinref part="L102" gate="G$1" pin="1" />
                <label x="175.26" y="104.14" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="RT_SW2" class="0">
              <segment>
                <pinref part="L102" gate="G$1" pin="2" />
                <wire x1="210.82" y1="104.14" x2="238.76" y2="104.14" width="0.1524" layer="91" />
                <pinref part="U104" gate="G$1" pin="SW2_2" />
                <wire x1="220.98" y1="147.32" x2="226.06" y2="147.32" width="0.1524" layer="91" />
                <pinref part="U104" gate="G$1" pin="SW2_1" />
                <wire x1="220.98" y1="152.4" x2="226.06" y2="152.4" width="0.1524" layer="91" />
                <wire x1="226.06" y1="147.32" x2="226.06" y2="152.4" width="0.1524" layer="91" />
                <wire x1="226.06" y1="147.32" x2="264.16" y2="147.32" width="0.1524" layer="91" />
                <junction x="226.06" y="147.32" />
                <wire x1="238.76" y1="104.14" x2="264.16" y2="104.14" width="0.1524" layer="91" />
                <wire x1="264.16" y1="104.14" x2="264.16" y2="147.32" width="0.1524" layer="91" />
                <label x="238.76" y="104.14" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="SCL" class="0">
              <segment>
                <pinref part="U104" gate="G$1" pin="SCL" />
                <wire x1="220.98" y1="157.48" x2="238.76" y2="157.48" width="0.1524" layer="91" />
                <wire x1="238.76" y1="157.48" x2="254" y2="157.48" width="0.1524" layer="91" />
                <label x="238.76" y="157.48" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="SDA" class="0">
              <segment>
                <pinref part="U104" gate="G$1" pin="SDA" />
                <wire x1="220.98" y1="142.24" x2="236.22" y2="142.24" width="0.1524" layer="91" />
                <wire x1="236.22" y1="142.24" x2="251.46" y2="142.24" width="0.1524" layer="91" />
                <label x="236.22" y="142.24" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="RT_VOUT_LOCAL" class="0">
              <segment>
                <pinref part="U104" gate="G$1" pin="VOUT" />
                <wire x1="220.98" y1="137.16" x2="223.52" y2="137.16" width="0.1524" layer="91" />
                <wire x1="223.52" y1="137.16" x2="231.14" y2="137.16" width="0.1524" layer="91" />
                <pinref part="C115" gate="G$1" pin="1" />
                <wire x1="231.14" y1="132.08" x2="231.14" y2="137.16" width="0.1524" layer="91" />
                <wire x1="231.14" y1="132.08" x2="246.38" y2="132.08" width="0.1524" layer="91" />
                <junction x="231.14" y="132.08" />
                <wire x1="231.14" y1="137.16" x2="233.68" y2="137.16" width="0.1524" layer="91" />
                <junction x="231.14" y="137.16" />
                <pinref part="R125" gate="G$1" pin="1" />
                <pinref part="C116" gate="G$1" pin="1" />
                <label x="223.52" y="137.16" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="VMAIN" class="1">
              <segment>
                <pinref part="R125" gate="G$1" pin="2" />
                <wire x1="248.92" y1="137.16" x2="251.46" y2="137.16" width="0.1524" layer="91" />
                <pinref part="TP106" gate="G$1" pin="1" />
                <label x="248.92" y="137.16" size="1.55" layer="95" />
              </segment>
            </net>
          </nets>
        </sheet>
        <sheet>
          <description>Solar harvesting and pack temperature</description>
          <plain>
            <wire x1="0" y1="0" x2="406.4" y2="0" width="0.25" layer="97" />
            <wire x1="406.4" y1="0" x2="406.4" y2="274.32" width="0.25" layer="97" />
            <wire x1="406.4" y1="274.32" x2="0" y2="274.32" width="0.25" layer="97" />
            <wire x1="0" y1="274.32" x2="0" y2="0" width="0.25" layer="97" />
            <text x="7.62" y="264.16" size="1.65" layer="97" font="proportional">ASTRA   /   SOLAR WEATHER STATION</text>
            <text x="7.62" y="252.73" size="4.1" layer="97" font="proportional">Solar harvesting and pack temperature</text>
            <text x="7.62" y="247.396" size="1.6" layer="97" font="proportional">SPV1050 reservoir, maximum-power-point setting and pack temperature window</text>
            <text x="398.78" y="264.16" size="1.65" layer="97" font="proportional" align="bottom-right">PROTOTYPE  A  /  SHEET  03  OF  07</text>
            <wire x1="7.62" y1="244.602" x2="398.78" y2="244.602" width="0.2" layer="97" />
            <text x="7.62" y="4.445" size="1.55" layer="97" font="proportional">Identical net labels connect across sheets.   |   Pin numbers refer to the top-side package.</text>
            <text x="7.62" y="238.76" size="1.9" layer="97" font="proportional">SOLAR MPPT</text>
            <text x="142.24" y="238.76" size="1.9" layer="97" font="proportional">PACK TEMPERATURE WINDOW</text>
          </plain>
          <instances>
            <instance part="U105" gate="G$1" x="203.2" y="210.82" rot="R0" smashed="yes">
              <attribute name="NAME" x="190.5" y="225.044" size="2.25" layer="95" font="proportional" rot="R0" />
              <attribute name="VALUE" x="190.5" y="221.5388" size="1.7" layer="96" font="proportional" rot="R0" />
            </instance>
            <instance part="D103" gate="G$1" x="203.2" y="177.8" rot="R0" smashed="yes">
              <attribute name="NAME" x="190.5" y="186.944" size="2.25" layer="95" font="proportional" rot="R0" />
              <attribute name="VALUE" x="190.5" y="183.4388" size="1.7" layer="96" font="proportional" rot="R0" />
            </instance>
            <instance part="R120" gate="G$1" x="203.2" y="157.48" rot="R0" smashed="yes">
              <attribute name="NAME" x="203.2" y="160.3248" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="203.2" y="155.321" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="R116" gate="G$1" x="203.2" y="142.24" rot="R0" smashed="yes">
              <attribute name="NAME" x="203.2" y="145.0848" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="203.2" y="140.081" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="C112" gate="G$1" x="203.2" y="127" rot="R0" smashed="yes">
              <attribute name="NAME" x="203.2" y="129.8448" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="203.2" y="124.841" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="R117" gate="G$1" x="203.2" y="111.76" rot="R0" smashed="yes">
              <attribute name="NAME" x="203.2" y="114.6048" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="203.2" y="109.601" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="R118" gate="G$1" x="203.2" y="96.52" rot="R0" smashed="yes">
              <attribute name="NAME" x="203.2" y="99.3648" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="203.2" y="94.361" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="R119" gate="G$1" x="203.2" y="81.28" rot="R0" smashed="yes">
              <attribute name="NAME" x="203.2" y="84.1248" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="203.2" y="79.121" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="U101" gate="G$1" x="63.5" y="129.54" rot="R0" smashed="yes">
              <attribute name="NAME" x="40.64" y="165.1" size="2.25" layer="95" font="proportional" rot="R0" align="bottom-left" />
              <attribute name="VALUE" x="40.64" y="160.02" size="1.7" layer="96" font="proportional" rot="R0" align="bottom-left" />
            </instance>
            <instance part="J103" gate="G$1" x="63.5" y="218.44" rot="R0" smashed="yes">
              <attribute name="NAME" x="48.26" y="231.14" size="2.25" layer="95" font="proportional" rot="R0" align="bottom-left" />
              <attribute name="VALUE" x="48.26" y="226.06" size="1.7" layer="96" font="proportional" rot="R0" align="bottom-left" />
            </instance>
            <instance part="D102" gate="G$1" x="45.72" y="203.2" rot="R90" smashed="yes">
              <attribute name="NAME" x="50.8" y="205.74" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="50.8" y="200.66" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="R126" gate="G$1" x="33.02" y="193.04" rot="R0" smashed="yes">
              <attribute name="NAME" x="27.94" y="198.12" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="27.94" y="188.468" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="R105" gate="G$1" x="20.32" y="180.34" rot="R270" smashed="yes">
              <attribute name="NAME" x="22.86" y="182.88" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="22.86" y="177.8" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="R106" gate="G$1" x="20.32" y="160.02" rot="R270" smashed="yes">
              <attribute name="NAME" x="10.16" y="162.56" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="10.16" y="157.48" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="R107" gate="G$1" x="20.32" y="139.7" rot="R270" smashed="yes">
              <attribute name="NAME" x="10.16" y="142.24" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="10.16" y="137.16" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="C104" gate="G$1" x="27.94" y="129.54" rot="R270" smashed="yes">
              <attribute name="NAME" x="22.225" y="132.588" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="16.129" y="126.111" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="C105" gate="G$1" x="104.14" y="154.94" rot="R90" smashed="yes">
              <attribute name="NAME" x="106.68" y="157.48" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="106.68" y="152.4" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="C106" gate="G$1" x="88.9" y="182.88" rot="R90" smashed="yes">
              <attribute name="NAME" x="91.44" y="185.42" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="91.44" y="180.34" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="C107" gate="G$1" x="106.68" y="182.88" rot="R90" smashed="yes">
              <attribute name="NAME" x="109.22" y="185.42" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="109.22" y="180.34" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="TP101" gate="G$1" x="71.12" y="172.72" rot="R180" smashed="yes">
              <attribute name="NAME" x="63.5" y="177.8" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="63.5" y="167.64" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="L101" gate="G$1" x="104.14" y="127" rot="R90" smashed="yes">
              <attribute name="NAME" x="106.68" y="129.54" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="106.68" y="124.46" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="C103" gate="G$1" x="111.76" y="101.6" rot="R270" smashed="yes">
              <attribute name="NAME" x="114.3" y="104.14" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="114.3" y="99.06" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="R108" gate="G$1" x="20.32" y="93.98" rot="R270" smashed="yes">
              <attribute name="NAME" x="22.86" y="96.52" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="22.86" y="91.44" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="R109" gate="G$1" x="20.32" y="73.66" rot="R270" smashed="yes">
              <attribute name="NAME" x="22.86" y="76.2" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="22.86" y="71.12" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="R110" gate="G$1" x="20.32" y="53.34" rot="R270" smashed="yes">
              <attribute name="NAME" x="22.86" y="55.88" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="22.86" y="50.8" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="Q101" gate="G$1" x="73.66" y="68.58" rot="R0" smashed="yes">
              <attribute name="NAME" x="63.5" y="78.74" size="2.25" layer="95" font="proportional" rot="R0" align="bottom-left" />
              <attribute name="VALUE" x="63.5" y="75.438" size="1.7" layer="96" font="proportional" rot="R0" align="bottom-left" />
            </instance>
            <instance part="R111" gate="G$1" x="48.26" y="58.42" rot="R270" smashed="yes">
              <attribute name="NAME" x="40.64" y="60.96" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="40.64" y="55.88" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="C108" gate="G$1" x="109.22" y="55.88" rot="R270" smashed="yes">
              <attribute name="NAME" x="111.76" y="58.42" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="111.76" y="53.34" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
          </instances>
          <busses />
          <nets>
            <net name="BAT_NTC" class="0">
              <segment>
                <pinref part="U105" gate="G$1" pin="INA_P" />
                <wire x1="187.96" y1="208.28" x2="142.24" y2="208.28" width="0.1524" layer="91" />
                <label x="142.24" y="208.28" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U105" gate="G$1" pin="INB_N" />
                <wire x1="218.44" y1="213.36" x2="261.62" y2="213.36" width="0.1524" layer="91" />
                <label x="220.98" y="213.36" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R116" gate="G$1" pin="2" />
                <wire x1="210.82" y1="142.24" x2="261.62" y2="142.24" width="0.1524" layer="91" />
                <label x="213.36" y="142.24" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="CHG_DISABLE" class="0">
              <segment>
                <pinref part="D103" gate="G$1" pin="K1_K2" />
                <wire x1="218.44" y1="180.34" x2="261.62" y2="180.34" width="0.1524" layer="91" />
                <label x="220.98" y="180.34" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R120" gate="G$1" pin="1" />
                <wire x1="195.58" y1="157.48" x2="142.24" y2="157.48" width="0.1524" layer="91" />
                <label x="142.24" y="157.48" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="CHG_IN" class="0">
              <segment>
                <pinref part="U105" gate="G$1" pin="VDD" />
                <wire x1="218.44" y1="203.2" x2="261.62" y2="203.2" width="0.1524" layer="91" />
                <label x="220.98" y="203.2" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R116" gate="G$1" pin="1" />
                <wire x1="195.58" y1="142.24" x2="142.24" y2="142.24" width="0.1524" layer="91" />
                <wire x1="142.24" y1="142.24" x2="142.24" y2="127" width="0.1524" layer="91" />
                <pinref part="C112" gate="G$1" pin="1" />
                <wire x1="195.58" y1="127" x2="142.24" y2="127" width="0.1524" layer="91" />
                <wire x1="142.24" y1="127" x2="142.24" y2="111.76" width="0.1524" layer="91" />
                <junction x="142.24" y="127" />
                <pinref part="R117" gate="G$1" pin="1" />
                <wire x1="195.58" y1="111.76" x2="142.24" y2="111.76" width="0.1524" layer="91" />
                <label x="142.24" y="142.24" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="GND" class="0">
              <segment>
                <pinref part="U105" gate="G$1" pin="VSS" />
                <wire x1="187.96" y1="203.2" x2="142.24" y2="203.2" width="0.1524" layer="91" />
                <label x="142.24" y="203.2" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R120" gate="G$1" pin="2" />
                <wire x1="210.82" y1="157.48" x2="261.62" y2="157.48" width="0.1524" layer="91" />
                <label x="213.36" y="157.48" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C112" gate="G$1" pin="2" />
                <wire x1="210.82" y1="127" x2="261.62" y2="127" width="0.1524" layer="91" />
                <label x="213.36" y="127" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R119" gate="G$1" pin="2" />
                <wire x1="210.82" y1="81.28" x2="261.62" y2="81.28" width="0.1524" layer="91" />
                <label x="213.36" y="81.28" size="1.55" layer="95" />
              </segment>
              <segment>
                <wire x1="15.24" y1="121.92" x2="15.24" y2="132.08" width="0.1524" layer="91" />
                <wire x1="15.24" y1="121.92" x2="22.86" y2="121.92" width="0.1524" layer="91" />
                <wire x1="15.24" y1="132.08" x2="20.32" y2="132.08" width="0.1524" layer="91" />
                <pinref part="R107" gate="G$1" pin="2" />
                <wire x1="22.86" y1="121.92" x2="27.94" y2="121.92" width="0.1524" layer="91" />
                <pinref part="C104" gate="G$1" pin="2" />
                <wire x1="27.94" y1="121.92" x2="33.02" y2="121.92" width="0.1524" layer="91" />
                <junction x="27.94" y="121.92" />
                <wire x1="33.02" y1="121.92" x2="33.02" y2="129.54" width="0.1524" layer="91" />
                <wire x1="33.02" y1="129.54" x2="33.02" y2="134.62" width="0.1524" layer="91" />
                <wire x1="33.02" y1="129.54" x2="38.1" y2="129.54" width="0.1524" layer="91" />
                <junction x="33.02" y="129.54" />
                <wire x1="33.02" y1="134.62" x2="33.02" y2="139.7" width="0.1524" layer="91" />
                <wire x1="33.02" y1="134.62" x2="38.1" y2="134.62" width="0.1524" layer="91" />
                <junction x="33.02" y="134.62" />
                <wire x1="33.02" y1="139.7" x2="38.1" y2="139.7" width="0.1524" layer="91" />
                <pinref part="U101" gate="G$1" pin="LDO2_EN" />
                <pinref part="U101" gate="G$1" pin="LDO1_EN" />
                <pinref part="U101" gate="G$1" pin="GND" />
                <label x="22.86" y="121.92" size="1.55" layer="95" />
              </segment>
              <segment>
                <wire x1="20.32" y1="38.1" x2="20.32" y2="45.72" width="0.1524" layer="91" />
                <wire x1="20.32" y1="38.1" x2="73.66" y2="38.1" width="0.1524" layer="91" />
                <pinref part="R110" gate="G$1" pin="2" />
                <wire x1="73.66" y1="38.1" x2="109.22" y2="38.1" width="0.1524" layer="91" />
                <wire x1="109.22" y1="38.1" x2="109.22" y2="48.26" width="0.1524" layer="91" />
                <pinref part="C108" gate="G$1" pin="2" />
                <label x="73.66" y="38.1" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="J103" gate="G$1" pin="PV_NEG" />
                <wire x1="81.28" y1="218.44" x2="83.82" y2="218.44" width="0.1524" layer="91" />
                <wire x1="83.82" y1="218.44" x2="96.52" y2="218.44" width="0.1524" layer="91" />
                <label x="83.82" y="218.44" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U101" gate="G$1" pin="EP" />
                <wire x1="88.9" y1="109.22" x2="93.98" y2="109.22" width="0.1524" layer="91" />
                <wire x1="93.98" y1="91.44" x2="93.98" y2="109.22" width="0.1524" layer="91" />
                <wire x1="93.98" y1="91.44" x2="101.6" y2="91.44" width="0.1524" layer="91" />
                <wire x1="101.6" y1="91.44" x2="111.76" y2="91.44" width="0.1524" layer="91" />
                <wire x1="111.76" y1="91.44" x2="111.76" y2="93.98" width="0.1524" layer="91" />
                <pinref part="C103" gate="G$1" pin="2" />
                <label x="101.6" y="91.44" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U101" gate="G$1" pin="PGND" />
                <wire x1="88.9" y1="124.46" x2="93.98" y2="124.46" width="0.1524" layer="91" />
                <label x="93.98" y="124.46" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U101" gate="G$1" pin="CONF" />
                <wire x1="88.9" y1="149.86" x2="96.52" y2="149.86" width="0.1524" layer="91" />
                <wire x1="96.52" y1="149.86" x2="96.52" y2="160.02" width="0.1524" layer="91" />
                <label x="96.52" y="160.02" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C106" gate="G$1" pin="2" />
                <wire x1="88.9" y1="190.5" x2="88.9" y2="195.58" width="0.1524" layer="91" />
                <wire x1="88.9" y1="195.58" x2="93.98" y2="195.58" width="0.1524" layer="91" />
                <wire x1="93.98" y1="195.58" x2="106.68" y2="195.58" width="0.1524" layer="91" />
                <pinref part="C107" gate="G$1" pin="2" />
                <wire x1="106.68" y1="190.5" x2="106.68" y2="195.58" width="0.1524" layer="91" />
                <label x="93.98" y="195.58" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C105" gate="G$1" pin="2" />
                <wire x1="104.14" y1="162.56" x2="104.14" y2="167.64" width="0.1524" layer="91" />
                <label x="104.14" y="167.64" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="NTC_COLD_REF" class="0">
              <segment>
                <pinref part="U105" gate="G$1" pin="INA_N" />
                <wire x1="187.96" y1="213.36" x2="142.24" y2="213.36" width="0.1524" layer="91" />
                <label x="142.24" y="213.36" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R117" gate="G$1" pin="2" />
                <wire x1="210.82" y1="111.76" x2="261.62" y2="111.76" width="0.1524" layer="91" />
                <label x="213.36" y="111.76" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R118" gate="G$1" pin="1" />
                <wire x1="195.58" y1="96.52" x2="142.24" y2="96.52" width="0.1524" layer="91" />
                <label x="142.24" y="96.52" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="NTC_HOT_REF" class="0">
              <segment>
                <pinref part="U105" gate="G$1" pin="INB_P" />
                <wire x1="218.44" y1="218.44" x2="261.62" y2="218.44" width="0.1524" layer="91" />
                <label x="220.98" y="218.44" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R118" gate="G$1" pin="2" />
                <wire x1="210.82" y1="96.52" x2="261.62" y2="96.52" width="0.1524" layer="91" />
                <label x="213.36" y="96.52" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R119" gate="G$1" pin="1" />
                <wire x1="195.58" y1="81.28" x2="142.24" y2="81.28" width="0.1524" layer="91" />
                <label x="142.24" y="81.28" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="TEMP_COLD" class="0">
              <segment>
                <pinref part="U105" gate="G$1" pin="OUTA" />
                <wire x1="187.96" y1="218.44" x2="142.24" y2="218.44" width="0.1524" layer="91" />
                <label x="142.24" y="218.44" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="D103" gate="G$1" pin="A2" />
                <wire x1="187.96" y1="175.26" x2="142.24" y2="175.26" width="0.1524" layer="91" />
                <label x="142.24" y="175.26" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="TEMP_HOT" class="0">
              <segment>
                <pinref part="U105" gate="G$1" pin="OUTB" />
                <wire x1="218.44" y1="208.28" x2="261.62" y2="208.28" width="0.1524" layer="91" />
                <label x="220.98" y="208.28" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="D103" gate="G$1" pin="A1" />
                <wire x1="187.96" y1="180.34" x2="142.24" y2="180.34" width="0.1524" layer="91" />
                <label x="142.24" y="180.34" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="PV_RAW" class="0">
              <segment>
                <pinref part="D102" gate="G$1" pin="A" />
                <wire x1="45.72" y1="210.82" x2="45.72" y2="218.44" width="0.1524" layer="91" />
                <pinref part="J103" gate="G$1" pin="PV_POS" />
                <label x="45.72" y="210.82" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="PV_IN" class="1">
              <segment>
                <pinref part="R126" gate="G$1" pin="2" />
                <wire x1="40.64" y1="193.04" x2="45.72" y2="193.04" width="0.1524" layer="91" />
                <wire x1="45.72" y1="193.04" x2="45.72" y2="195.58" width="0.1524" layer="91" />
                <pinref part="D102" gate="G$1" pin="K" />
                <label x="45.72" y="193.04" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="PV_IC_IN" class="0">
              <segment>
                <wire x1="15.24" y1="187.96" x2="15.24" y2="193.04" width="0.1524" layer="91" />
                <wire x1="15.24" y1="187.96" x2="20.32" y2="187.96" width="0.1524" layer="91" />
                <wire x1="15.24" y1="193.04" x2="25.4" y2="193.04" width="0.1524" layer="91" />
                <pinref part="R105" gate="G$1" pin="1" />
                <pinref part="R126" gate="G$1" pin="1" />
                <label x="15.24" y="187.96" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U101" gate="G$1" pin="IN_HV" />
                <wire x1="88.9" y1="114.3" x2="93.98" y2="114.3" width="0.1524" layer="91" />
                <wire x1="93.98" y1="114.3" x2="111.76" y2="114.3" width="0.1524" layer="91" />
                <pinref part="C103" gate="G$1" pin="1" />
                <wire x1="111.76" y1="109.22" x2="111.76" y2="114.3" width="0.1524" layer="91" />
                <label x="93.98" y="114.3" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="PV_MPP" class="0">
              <segment>
                <pinref part="R106" gate="G$1" pin="1" />
                <wire x1="20.32" y1="167.64" x2="20.32" y2="170.18" width="0.1524" layer="91" />
                <wire x1="20.32" y1="170.18" x2="20.32" y2="172.72" width="0.1524" layer="91" />
                <wire x1="20.32" y1="170.18" x2="30.48" y2="170.18" width="0.1524" layer="91" />
                <junction x="20.32" y="170.18" />
                <pinref part="R105" gate="G$1" pin="2" />
                <wire x1="30.48" y1="154.94" x2="30.48" y2="170.18" width="0.1524" layer="91" />
                <wire x1="30.48" y1="154.94" x2="38.1" y2="154.94" width="0.1524" layer="91" />
                <pinref part="U101" gate="G$1" pin="MPP" />
                <label x="30.48" y="170.18" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="PV_MPP_SET" class="0">
              <segment>
                <pinref part="R107" gate="G$1" pin="1" />
                <wire x1="20.32" y1="147.32" x2="20.32" y2="149.86" width="0.1524" layer="91" />
                <wire x1="20.32" y1="149.86" x2="20.32" y2="152.4" width="0.1524" layer="91" />
                <wire x1="20.32" y1="149.86" x2="38.1" y2="149.86" width="0.1524" layer="91" />
                <junction x="20.32" y="149.86" />
                <pinref part="R106" gate="G$1" pin="2" />
                <pinref part="U101" gate="G$1" pin="MPP_SET" />
                <label x="20.32" y="149.86" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="PV_MPP_REF" class="0">
              <segment>
                <pinref part="C104" gate="G$1" pin="1" />
                <wire x1="27.94" y1="137.16" x2="27.94" y2="144.78" width="0.1524" layer="91" />
                <wire x1="27.94" y1="144.78" x2="38.1" y2="144.78" width="0.1524" layer="91" />
                <pinref part="U101" gate="G$1" pin="MPP_REF" />
                <label x="27.94" y="144.78" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="PV_READY_N" class="0">
              <segment>
                <wire x1="10.16" y1="119.38" x2="38.1" y2="119.38" width="0.1524" layer="91" />
                <pinref part="U101" gate="G$1" pin="BATT_CONN_N" />
                <label x="10.16" y="119.38" size="1.55" layer="95" />
              </segment>
              <segment>
                <wire x1="38.1" y1="71.12" x2="48.26" y2="71.12" width="0.1524" layer="91" />
                <pinref part="R111" gate="G$1" pin="1" />
                <wire x1="48.26" y1="66.04" x2="48.26" y2="71.12" width="0.1524" layer="91" />
                <wire x1="48.26" y1="71.12" x2="60.96" y2="71.12" width="0.1524" layer="91" />
                <junction x="48.26" y="71.12" />
                <pinref part="Q101" gate="G$1" pin="G" />
                <label x="38.1" y="71.12" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="PV_STORE" class="0">
              <segment>
                <pinref part="R108" gate="G$1" pin="1" />
                <wire x1="20.32" y1="101.6" x2="20.32" y2="106.68" width="0.1524" layer="91" />
                <label x="20.32" y="106.68" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R111" gate="G$1" pin="2" />
                <wire x1="48.26" y1="50.8" x2="55.88" y2="50.8" width="0.1524" layer="91" />
                <wire x1="55.88" y1="50.8" x2="55.88" y2="66.04" width="0.1524" layer="91" />
                <wire x1="55.88" y1="50.8" x2="60.96" y2="50.8" width="0.1524" layer="91" />
                <junction x="55.88" y="50.8" />
                <wire x1="55.88" y1="66.04" x2="60.96" y2="66.04" width="0.1524" layer="91" />
                <wire x1="60.96" y1="50.8" x2="68.58" y2="50.8" width="0.1524" layer="91" />
                <pinref part="Q101" gate="G$1" pin="S" />
                <label x="60.96" y="50.8" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="TP101" gate="G$1" pin="1" />
                <wire x1="78.74" y1="172.72" x2="88.9" y2="172.72" width="0.1524" layer="91" />
                <pinref part="U101" gate="G$1" pin="STORE" />
                <wire x1="88.9" y1="139.7" x2="91.44" y2="139.7" width="0.1524" layer="91" />
                <wire x1="88.9" y1="172.72" x2="88.9" y2="175.26" width="0.1524" layer="91" />
                <wire x1="88.9" y1="172.72" x2="106.68" y2="172.72" width="0.1524" layer="91" />
                <junction x="88.9" y="172.72" />
                <pinref part="C106" gate="G$1" pin="1" />
                <wire x1="91.44" y1="139.7" x2="127" y2="139.7" width="0.1524" layer="91" />
                <wire x1="106.68" y1="172.72" x2="106.68" y2="175.26" width="0.1524" layer="91" />
                <wire x1="106.68" y1="172.72" x2="127" y2="172.72" width="0.1524" layer="91" />
                <junction x="106.68" y="172.72" />
                <pinref part="C107" gate="G$1" pin="1" />
                <wire x1="127" y1="139.7" x2="127" y2="172.72" width="0.1524" layer="91" />
                <label x="91.44" y="139.7" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="PV_UVP" class="0">
              <segment>
                <pinref part="R109" gate="G$1" pin="1" />
                <wire x1="20.32" y1="81.28" x2="20.32" y2="83.82" width="0.1524" layer="91" />
                <wire x1="20.32" y1="83.82" x2="20.32" y2="86.36" width="0.1524" layer="91" />
                <wire x1="20.32" y1="83.82" x2="35.56" y2="83.82" width="0.1524" layer="91" />
                <junction x="20.32" y="83.82" />
                <pinref part="R108" gate="G$1" pin="2" />
                <wire x1="35.56" y1="83.82" x2="35.56" y2="109.22" width="0.1524" layer="91" />
                <wire x1="35.56" y1="109.22" x2="38.1" y2="109.22" width="0.1524" layer="91" />
                <pinref part="U101" gate="G$1" pin="UVP" />
                <label x="20.32" y="83.82" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="PV_EOC" class="0">
              <segment>
                <wire x1="12.7" y1="63.5" x2="12.7" y2="114.3" width="0.1524" layer="91" />
                <wire x1="12.7" y1="63.5" x2="20.32" y2="63.5" width="0.1524" layer="91" />
                <wire x1="12.7" y1="114.3" x2="22.86" y2="114.3" width="0.1524" layer="91" />
                <pinref part="R110" gate="G$1" pin="1" />
                <wire x1="20.32" y1="60.96" x2="20.32" y2="63.5" width="0.1524" layer="91" />
                <wire x1="20.32" y1="63.5" x2="20.32" y2="66.04" width="0.1524" layer="91" />
                <junction x="20.32" y="63.5" />
                <pinref part="R109" gate="G$1" pin="2" />
                <wire x1="22.86" y1="114.3" x2="38.1" y2="114.3" width="0.1524" layer="91" />
                <pinref part="U101" gate="G$1" pin="EOC" />
                <label x="22.86" y="114.3" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="PV_BUFFER" class="0">
              <segment>
                <pinref part="U101" gate="G$1" pin="BATT" />
                <wire x1="88.9" y1="144.78" x2="93.98" y2="144.78" width="0.1524" layer="91" />
                <wire x1="93.98" y1="144.78" x2="104.14" y2="144.78" width="0.1524" layer="91" />
                <wire x1="104.14" y1="144.78" x2="104.14" y2="147.32" width="0.1524" layer="91" />
                <pinref part="C105" gate="G$1" pin="1" />
                <label x="93.98" y="144.78" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="PV_LVSW" class="0">
              <segment>
                <pinref part="U101" gate="G$1" pin="IN_LV" />
                <wire x1="88.9" y1="134.62" x2="91.44" y2="134.62" width="0.1524" layer="91" />
                <wire x1="91.44" y1="134.62" x2="104.14" y2="134.62" width="0.1524" layer="91" />
                <pinref part="L101" gate="G$1" pin="2" />
                <label x="91.44" y="134.62" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="PV_HVSW" class="0">
              <segment>
                <pinref part="U101" gate="G$1" pin="L_HV" />
                <wire x1="88.9" y1="119.38" x2="91.44" y2="119.38" width="0.1524" layer="91" />
                <wire x1="91.44" y1="119.38" x2="104.14" y2="119.38" width="0.1524" layer="91" />
                <pinref part="L101" gate="G$1" pin="1" />
                <label x="91.44" y="119.38" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="PV_VALID" class="0">
              <segment>
                <pinref part="Q101" gate="G$1" pin="D" />
                <wire x1="86.36" y1="71.12" x2="109.22" y2="71.12" width="0.1524" layer="91" />
                <pinref part="C108" gate="G$1" pin="1" />
                <wire x1="109.22" y1="63.5" x2="109.22" y2="71.12" width="0.1524" layer="91" />
                <wire x1="109.22" y1="71.12" x2="111.76" y2="71.12" width="0.1524" layer="91" />
                <junction x="109.22" y="71.12" />
                <wire x1="111.76" y1="71.12" x2="127" y2="71.12" width="0.1524" layer="91" />
                <label x="111.76" y="71.12" size="1.55" layer="95" />
              </segment>
            </net>
          </nets>
        </sheet>
        <sheet>
          <description>Radio and programming</description>
          <plain>
            <wire x1="0" y1="0" x2="406.4" y2="0" width="0.25" layer="97" />
            <wire x1="406.4" y1="0" x2="406.4" y2="274.32" width="0.25" layer="97" />
            <wire x1="406.4" y1="274.32" x2="0" y2="274.32" width="0.25" layer="97" />
            <wire x1="0" y1="274.32" x2="0" y2="0" width="0.25" layer="97" />
            <text x="7.62" y="264.16" size="1.65" layer="97" font="proportional">ASTRA   /   SOLAR WEATHER STATION</text>
            <text x="7.62" y="252.73" size="4.1" layer="97" font="proportional">Radio and programming</text>
            <text x="7.62" y="247.396" size="1.6" layer="97" font="proportional">2.4 GHz radio, host connections and SWD access</text>
            <text x="398.78" y="264.16" size="1.65" layer="97" font="proportional" align="bottom-right">PROTOTYPE  A  /  SHEET  04  OF  07</text>
            <wire x1="7.62" y1="244.602" x2="398.78" y2="244.602" width="0.2" layer="97" />
            <text x="7.62" y="4.445" size="1.55" layer="97" font="proportional">Identical net labels connect across sheets.   |   Pin numbers refer to the top-side package.</text>
            <text x="7.62" y="238.76" size="1.9" layer="97" font="proportional">2.4 GHZ RADIO AND PROCESSOR</text>
            <text x="7.62" y="104.14" size="1.9" layer="97" font="proportional">RADIO SUPPLY BYPASS</text>
            <text x="7.62" y="57.912" size="1.9" layer="97" font="proportional">RADIO RESET FILTER</text>
            <text x="142.24" y="238.76" size="1.9" layer="97" font="proportional">POGO PROGRAMMING AND TIMER OVERRIDE</text>
          </plain>
          <instances>
            <instance part="U201" gate="G$1" x="68.58" y="170.18" rot="R0" smashed="yes">
              <attribute name="NAME" x="48.26" y="225.044" size="2.25" layer="95" font="proportional" rot="R0" />
              <attribute name="VALUE" x="48.26" y="221.5388" size="1.7" layer="96" font="proportional" rot="R0" />
            </instance>
            <instance part="C201" gate="G$1" x="68.58" y="88.9" rot="R0" smashed="yes">
              <attribute name="NAME" x="68.58" y="91.7448" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="68.58" y="86.741" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="C202" gate="G$1" x="68.58" y="73.66" rot="R0" smashed="yes">
              <attribute name="NAME" x="68.58" y="76.5048" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="68.58" y="71.501" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="C203" gate="G$1" x="68.58" y="43.18" rot="R0" smashed="yes">
              <attribute name="NAME" x="68.58" y="46.0248" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="68.58" y="41.021" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="R201" gate="G$1" x="68.58" y="27.94" rot="R0" smashed="yes">
              <attribute name="NAME" x="68.58" y="30.7848" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="68.58" y="25.781" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="J201" gate="G$1" x="203.2" y="210.82" rot="R0" smashed="yes">
              <attribute name="NAME" x="180.34" y="225.044" size="2.25" layer="95" font="proportional" rot="R0" />
              <attribute name="VALUE" x="180.34" y="221.5388" size="1.7" layer="96" font="proportional" rot="R0" />
            </instance>
          </instances>
          <busses />
          <nets>
            <net name="BTN1" class="0">
              <segment>
                <pinref part="U201" gate="G$1" pin="P1.05" />
                <wire x1="45.72" y1="147.32" x2="7.62" y2="147.32" width="0.1524" layer="91" />
                <label x="7.62" y="147.32" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="BTN2" class="0">
              <segment>
                <pinref part="U201" gate="G$1" pin="P1.06" />
                <wire x1="45.72" y1="152.4" x2="7.62" y2="152.4" width="0.1524" layer="91" />
                <label x="7.62" y="152.4" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="BTN3" class="0">
              <segment>
                <pinref part="U201" gate="G$1" pin="P1.07" />
                <wire x1="45.72" y1="142.24" x2="7.62" y2="142.24" width="0.1524" layer="91" />
                <label x="7.62" y="142.24" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="EPD_BUSY" class="0">
              <segment>
                <pinref part="U201" gate="G$1" pin="P2.04" />
                <wire x1="91.44" y1="187.96" x2="127" y2="187.96" width="0.1524" layer="91" />
                <label x="93.98" y="187.96" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="EPD_CS" class="0">
              <segment>
                <pinref part="U201" gate="G$1" pin="P2.05" />
                <wire x1="91.44" y1="182.88" x2="127" y2="182.88" width="0.1524" layer="91" />
                <label x="93.98" y="182.88" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="EPD_DC" class="0">
              <segment>
                <pinref part="U201" gate="G$1" pin="P2.00" />
                <wire x1="45.72" y1="132.08" x2="7.62" y2="132.08" width="0.1524" layer="91" />
                <label x="7.62" y="132.08" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="EPD_MOSI" class="0">
              <segment>
                <pinref part="U201" gate="G$1" pin="P2.02" />
                <wire x1="91.44" y1="218.44" x2="127" y2="218.44" width="0.1524" layer="91" />
                <label x="93.98" y="218.44" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="EPD_RST" class="0">
              <segment>
                <pinref part="U201" gate="G$1" pin="P2.03" />
                <wire x1="91.44" y1="213.36" x2="127" y2="213.36" width="0.1524" layer="91" />
                <label x="93.98" y="213.36" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="EPD_SCK" class="0">
              <segment>
                <pinref part="U201" gate="G$1" pin="P2.01" />
                <wire x1="45.72" y1="121.92" x2="7.62" y2="121.92" width="0.1524" layer="91" />
                <label x="7.62" y="121.92" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="GND" class="0">
              <segment>
                <pinref part="U201" gate="G$1" pin="GND_10" />
                <wire x1="45.72" y1="172.72" x2="7.62" y2="172.72" width="0.1524" layer="91" />
                <label x="7.62" y="172.72" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U201" gate="G$1" pin="GND_30" />
                <wire x1="91.44" y1="172.72" x2="127" y2="172.72" width="0.1524" layer="91" />
                <label x="93.98" y="172.72" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U201" gate="G$1" pin="GND_31" />
                <wire x1="91.44" y1="167.64" x2="127" y2="167.64" width="0.1524" layer="91" />
                <label x="93.98" y="167.64" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U201" gate="G$1" pin="GND_37" />
                <wire x1="91.44" y1="137.16" x2="127" y2="137.16" width="0.1524" layer="91" />
                <label x="93.98" y="137.16" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U201" gate="G$1" pin="GND_38" />
                <wire x1="91.44" y1="132.08" x2="127" y2="132.08" width="0.1524" layer="91" />
                <label x="93.98" y="132.08" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U201" gate="G$1" pin="GND_39" />
                <wire x1="91.44" y1="127" x2="127" y2="127" width="0.1524" layer="91" />
                <label x="93.98" y="127" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U201" gate="G$1" pin="GND_40" />
                <wire x1="91.44" y1="121.92" x2="127" y2="121.92" width="0.1524" layer="91" />
                <label x="93.98" y="121.92" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C201" gate="G$1" pin="2" />
                <wire x1="76.2" y1="88.9" x2="127" y2="88.9" width="0.1524" layer="91" />
                <wire x1="127" y1="88.9" x2="127" y2="73.66" width="0.1524" layer="91" />
                <pinref part="C202" gate="G$1" pin="2" />
                <wire x1="76.2" y1="73.66" x2="127" y2="73.66" width="0.1524" layer="91" />
                <label x="78.74" y="88.9" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C203" gate="G$1" pin="2" />
                <wire x1="76.2" y1="43.18" x2="127" y2="43.18" width="0.1524" layer="91" />
                <label x="78.74" y="43.18" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="J201" gate="G$1" pin="GND" />
                <wire x1="177.8" y1="218.44" x2="142.24" y2="218.44" width="0.1524" layer="91" />
                <label x="142.24" y="218.44" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="NRST" class="0">
              <segment>
                <pinref part="U201" gate="G$1" pin="nRESET" />
                <wire x1="45.72" y1="127" x2="7.62" y2="127" width="0.1524" layer="91" />
                <label x="7.62" y="127" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C203" gate="G$1" pin="1" />
                <wire x1="60.96" y1="43.18" x2="7.62" y2="43.18" width="0.1524" layer="91" />
                <label x="7.62" y="43.18" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R201" gate="G$1" pin="2" />
                <wire x1="76.2" y1="27.94" x2="127" y2="27.94" width="0.1524" layer="91" />
                <label x="78.74" y="27.94" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="J201" gate="G$1" pin="nRESET" />
                <wire x1="228.6" y1="218.44" x2="261.62" y2="218.44" width="0.1524" layer="91" />
                <label x="231.14" y="218.44" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="SCL" class="0">
              <segment>
                <pinref part="U201" gate="G$1" pin="P1.11" />
                <wire x1="45.72" y1="208.28" x2="7.62" y2="208.28" width="0.1524" layer="91" />
                <label x="7.62" y="208.28" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="SDA" class="0">
              <segment>
                <pinref part="U201" gate="G$1" pin="P1.12" />
                <wire x1="45.72" y1="203.2" x2="7.62" y2="203.2" width="0.1524" layer="91" />
                <label x="7.62" y="203.2" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="SWCLK" class="0">
              <segment>
                <pinref part="U201" gate="G$1" pin="SWCLK" />
                <wire x1="45.72" y1="167.64" x2="7.62" y2="167.64" width="0.1524" layer="91" />
                <label x="7.62" y="167.64" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="J201" gate="G$1" pin="SWCLK" />
                <wire x1="177.8" y1="208.28" x2="142.24" y2="208.28" width="0.1524" layer="91" />
                <label x="142.24" y="208.28" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="SWDIO" class="0">
              <segment>
                <pinref part="U201" gate="G$1" pin="SWDIO" />
                <wire x1="45.72" y1="162.56" x2="7.62" y2="162.56" width="0.1524" layer="91" />
                <label x="7.62" y="162.56" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="J201" gate="G$1" pin="SWDIO" />
                <wire x1="177.8" y1="203.2" x2="142.24" y2="203.2" width="0.1524" layer="91" />
                <label x="142.24" y="203.2" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="TIMER_DONE" class="0">
              <segment>
                <pinref part="U201" gate="G$1" pin="P0.00" />
                <wire x1="91.44" y1="177.8" x2="127" y2="177.8" width="0.1524" layer="91" />
                <label x="93.98" y="177.8" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="VAON" class="0">
              <segment>
                <pinref part="J201" gate="G$1" pin="VAON" />
                <wire x1="228.6" y1="208.28" x2="261.62" y2="208.28" width="0.1524" layer="91" />
                <label x="231.14" y="208.28" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="VBAT_MEAS_EN" class="0">
              <segment>
                <pinref part="U201" gate="G$1" pin="P1.09" />
                <wire x1="45.72" y1="218.44" x2="7.62" y2="218.44" width="0.1524" layer="91" />
                <label x="7.62" y="218.44" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="VBAT_SENSE" class="0">
              <segment>
                <pinref part="U201" gate="G$1" pin="P1.04_AIN0" />
                <wire x1="45.72" y1="187.96" x2="7.62" y2="187.96" width="0.1524" layer="91" />
                <label x="7.62" y="187.96" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="VMAIN" class="1">
              <segment>
                <pinref part="U201" gate="G$1" pin="VDD" />
                <wire x1="45.72" y1="177.8" x2="7.62" y2="177.8" width="0.1524" layer="91" />
                <label x="7.62" y="177.8" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C201" gate="G$1" pin="1" />
                <wire x1="60.96" y1="88.9" x2="7.62" y2="88.9" width="0.1524" layer="91" />
                <wire x1="7.62" y1="88.9" x2="7.62" y2="73.66" width="0.1524" layer="91" />
                <pinref part="C202" gate="G$1" pin="1" />
                <wire x1="60.96" y1="73.66" x2="7.62" y2="73.66" width="0.1524" layer="91" />
                <label x="7.62" y="88.9" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R201" gate="G$1" pin="1" />
                <wire x1="60.96" y1="27.94" x2="7.62" y2="27.94" width="0.1524" layer="91" />
                <label x="7.62" y="27.94" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="J201" gate="G$1" pin="VTREF_SENSE" />
                <wire x1="177.8" y1="213.36" x2="142.24" y2="213.36" width="0.1524" layer="91" />
                <label x="142.24" y="213.36" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="WAKE_MDRV" class="0">
              <segment>
                <pinref part="J201" gate="G$1" pin="WAKE_MDRV" />
                <wire x1="228.6" y1="213.36" x2="261.62" y2="213.36" width="0.1524" layer="91" />
                <label x="231.14" y="213.36" size="1.55" layer="95" />
              </segment>
            </net>
          </nets>
        </sheet>
        <sheet>
          <description>Electrophoretic display</description>
          <plain>
            <wire x1="0" y1="0" x2="406.4" y2="0" width="0.25" layer="97" />
            <wire x1="406.4" y1="0" x2="406.4" y2="274.32" width="0.25" layer="97" />
            <wire x1="406.4" y1="274.32" x2="0" y2="274.32" width="0.25" layer="97" />
            <wire x1="0" y1="274.32" x2="0" y2="0" width="0.25" layer="97" />
            <text x="7.62" y="264.16" size="1.65" layer="97" font="proportional">ASTRA   /   SOLAR WEATHER STATION</text>
            <text x="7.62" y="252.73" size="4.1" layer="97" font="proportional">Electrophoretic display</text>
            <text x="7.62" y="247.396" size="1.6" layer="97" font="proportional">24-contact panel interface, switched boost loop and panel bias supplies</text>
            <text x="398.78" y="264.16" size="1.65" layer="97" font="proportional" align="bottom-right">PROTOTYPE  A  /  SHEET  05  OF  07</text>
            <wire x1="7.62" y1="244.602" x2="398.78" y2="244.602" width="0.2" layer="97" />
            <text x="7.62" y="4.445" size="1.55" layer="97" font="proportional">Identical net labels connect across sheets.   |   Pin numbers refer to the top-side package.</text>
            <text x="7.62" y="238.76" size="1.9" layer="97" font="proportional">PANEL CONNECTOR</text>
            <text x="7.62" y="139.7" size="1.9" layer="97" font="proportional">BIPOLAR BOOST</text>
            <text x="142.24" y="238.76" size="1.9" layer="97" font="proportional">PANEL CAPACITORS</text>
            <text x="142.24" y="85.852" size="1.9" layer="97" font="proportional">DIGITAL INTERFACE</text>
            <text x="276.86" y="238.76" size="1.9" layer="97" font="proportional">TEST ACCESS</text>
          </plain>
          <instances>
            <instance part="J301" gate="G$1" x="68.58" y="187.96" rot="R0" smashed="yes">
              <attribute name="NAME" x="53.34" y="225.044" size="2.25" layer="95" font="proportional" rot="R0" />
              <attribute name="VALUE" x="53.34" y="221.5388" size="1.7" layer="96" font="proportional" rot="R0" />
            </instance>
            <instance part="C311" gate="G$1" x="203.2" y="223.52" rot="R0" smashed="yes">
              <attribute name="NAME" x="203.2" y="226.3648" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="203.2" y="221.361" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="C305" gate="G$1" x="203.2" y="208.28" rot="R0" smashed="yes">
              <attribute name="NAME" x="203.2" y="211.1248" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="203.2" y="206.121" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="C308" gate="G$1" x="203.2" y="193.04" rot="R0" smashed="yes">
              <attribute name="NAME" x="203.2" y="195.8848" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="203.2" y="190.881" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="C310" gate="G$1" x="203.2" y="177.8" rot="R0" smashed="yes">
              <attribute name="NAME" x="203.2" y="180.6448" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="203.2" y="175.641" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="C306" gate="G$1" x="203.2" y="162.56" rot="R0" smashed="yes">
              <attribute name="NAME" x="203.2" y="165.4048" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="203.2" y="160.401" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="C307" gate="G$1" x="203.2" y="147.32" rot="R0" smashed="yes">
              <attribute name="NAME" x="203.2" y="150.1648" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="203.2" y="145.161" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="C303" gate="G$1" x="203.2" y="132.08" rot="R0" smashed="yes">
              <attribute name="NAME" x="203.2" y="134.9248" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="203.2" y="129.921" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="C309" gate="G$1" x="203.2" y="116.84" rot="R0" smashed="yes">
              <attribute name="NAME" x="203.2" y="119.6848" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="203.2" y="114.681" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="C304" gate="G$1" x="203.2" y="101.6" rot="R0" smashed="yes">
              <attribute name="NAME" x="203.2" y="104.4448" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="203.2" y="99.441" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="R305" gate="G$1" x="203.2" y="71.12" rot="R0" smashed="yes">
              <attribute name="NAME" x="203.2" y="73.9648" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="203.2" y="68.961" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="R303" gate="G$1" x="203.2" y="55.88" rot="R0" smashed="yes">
              <attribute name="NAME" x="203.2" y="58.7248" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="203.2" y="53.721" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="R304" gate="G$1" x="203.2" y="40.64" rot="R0" smashed="yes">
              <attribute name="NAME" x="203.2" y="43.4848" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="203.2" y="38.481" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="TP301" gate="G$1" x="337.82" y="223.52" rot="R0" smashed="yes">
              <attribute name="NAME" x="337.82" y="226.3648" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="337.82" y="221.361" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="TP302" gate="G$1" x="337.82" y="208.28" rot="R0" smashed="yes">
              <attribute name="NAME" x="337.82" y="211.1248" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="337.82" y="206.121" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="C302" gate="G$1" x="15.24" y="101.6" rot="R270" smashed="yes">
              <attribute name="NAME" x="17.78" y="104.14" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="17.78" y="99.06" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="L301" gate="G$1" x="55.88" y="119.38" rot="R0" smashed="yes">
              <attribute name="NAME" x="55.88" y="122.2248" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="55.88" y="117.221" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="Q301" gate="G$1" x="55.88" y="83.82" rot="R0" smashed="yes">
              <attribute name="NAME" x="45.72" y="92.964" size="2.25" layer="95" font="proportional" rot="R0" />
              <attribute name="VALUE" x="45.72" y="89.4588" size="1.7" layer="96" font="proportional" rot="R0" />
            </instance>
            <instance part="R301" gate="G$1" x="25.4" y="60.96" rot="R90" smashed="yes">
              <attribute name="NAME" x="17.78" y="50.8" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="17.78" y="45.72" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="R302" gate="G$1" x="43.18" y="60.96" rot="R90" smashed="yes">
              <attribute name="NAME" x="45.72" y="63.5" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="45.72" y="58.42" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="D303" gate="G$1" x="93.98" y="119.38" rot="R180" smashed="yes">
              <attribute name="NAME" x="86.36" y="129.54" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="86.36" y="124.46" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="C301" gate="G$1" x="86.36" y="93.98" rot="R0" smashed="yes">
              <attribute name="NAME" x="86.36" y="96.8248" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="86.36" y="91.821" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="D301" gate="G$1" x="104.14" y="66.04" rot="R90" smashed="yes">
              <attribute name="NAME" x="106.68" y="68.58" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="106.68" y="63.5" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="D302" gate="G$1" x="116.84" y="93.98" rot="R0" smashed="yes">
              <attribute name="NAME" x="116.84" y="96.8248" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="116.84" y="91.821" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
          </instances>
          <busses />
          <nets>
            <net name="EPD_BUSY" class="0">
              <segment>
                <pinref part="J301" gate="G$1" pin="BUSY" />
                <wire x1="50.8" y1="177.8" x2="7.62" y2="177.8" width="0.1524" layer="91" />
                <label x="7.62" y="177.8" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R305" gate="G$1" pin="1" />
                <wire x1="195.58" y1="71.12" x2="142.24" y2="71.12" width="0.1524" layer="91" />
                <label x="142.24" y="71.12" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="EPD_CS" class="0">
              <segment>
                <pinref part="J301" gate="G$1" pin="nCS" />
                <wire x1="50.8" y1="162.56" x2="7.62" y2="162.56" width="0.1524" layer="91" />
                <label x="7.62" y="162.56" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R303" gate="G$1" pin="1" />
                <wire x1="195.58" y1="55.88" x2="142.24" y2="55.88" width="0.1524" layer="91" />
                <label x="142.24" y="55.88" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="EPD_DC" class="0">
              <segment>
                <pinref part="J301" gate="G$1" pin="DC" />
                <wire x1="50.8" y1="167.64" x2="7.62" y2="167.64" width="0.1524" layer="91" />
                <label x="7.62" y="167.64" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="EPD_GDR" class="0">
              <segment>
                <pinref part="J301" gate="G$1" pin="GDR" />
                <wire x1="50.8" y1="213.36" x2="7.62" y2="213.36" width="0.1524" layer="91" />
                <label x="7.62" y="213.36" size="1.55" layer="95" />
              </segment>
              <segment>
                <wire x1="20.32" y1="86.36" x2="25.4" y2="86.36" width="0.1524" layer="91" />
                <pinref part="R301" gate="G$1" pin="2" />
                <wire x1="25.4" y1="68.58" x2="25.4" y2="86.36" width="0.1524" layer="91" />
                <wire x1="25.4" y1="86.36" x2="43.18" y2="86.36" width="0.1524" layer="91" />
                <junction x="25.4" y="86.36" />
                <pinref part="Q301" gate="G$1" pin="G" />
                <label x="20.32" y="86.36" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="EPD_MOSI" class="0">
              <segment>
                <pinref part="J301" gate="G$1" pin="SDA" />
                <wire x1="86.36" y1="218.44" x2="127" y2="218.44" width="0.1524" layer="91" />
                <label x="88.9" y="218.44" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="EPD_RESE" class="0">
              <segment>
                <pinref part="J301" gate="G$1" pin="RESE" />
                <wire x1="50.8" y1="208.28" x2="7.62" y2="208.28" width="0.1524" layer="91" />
                <label x="7.62" y="208.28" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R302" gate="G$1" pin="2" />
                <wire x1="43.18" y1="68.58" x2="43.18" y2="73.66" width="0.1524" layer="91" />
                <wire x1="43.18" y1="73.66" x2="43.18" y2="81.28" width="0.1524" layer="91" />
                <pinref part="Q301" gate="G$1" pin="S" />
                <label x="43.18" y="73.66" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="EPD_RST" class="0">
              <segment>
                <pinref part="J301" gate="G$1" pin="nRES" />
                <wire x1="50.8" y1="172.72" x2="7.62" y2="172.72" width="0.1524" layer="91" />
                <label x="7.62" y="172.72" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R304" gate="G$1" pin="1" />
                <wire x1="195.58" y1="40.64" x2="142.24" y2="40.64" width="0.1524" layer="91" />
                <label x="142.24" y="40.64" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="EPD_SCK" class="0">
              <segment>
                <pinref part="J301" gate="G$1" pin="SCL" />
                <wire x1="50.8" y1="157.48" x2="7.62" y2="157.48" width="0.1524" layer="91" />
                <label x="7.62" y="157.48" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="EPD_VCOM" class="0">
              <segment>
                <pinref part="J301" gate="G$1" pin="VCOM" />
                <wire x1="86.36" y1="167.64" x2="127" y2="167.64" width="0.1524" layer="91" />
                <label x="88.9" y="167.64" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C311" gate="G$1" pin="1" />
                <wire x1="195.58" y1="223.52" x2="142.24" y2="223.52" width="0.1524" layer="91" />
                <label x="142.24" y="223.52" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="EPD_VCORE" class="0">
              <segment>
                <pinref part="J301" gate="G$1" pin="VDD" />
                <wire x1="86.36" y1="198.12" x2="127" y2="198.12" width="0.1524" layer="91" />
                <label x="88.9" y="198.12" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C305" gate="G$1" pin="1" />
                <wire x1="195.58" y1="208.28" x2="142.24" y2="208.28" width="0.1524" layer="91" />
                <label x="142.24" y="208.28" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="EPD_VGH" class="0">
              <segment>
                <pinref part="J301" gate="G$1" pin="VGH" />
                <wire x1="86.36" y1="182.88" x2="127" y2="182.88" width="0.1524" layer="91" />
                <label x="88.9" y="182.88" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C308" gate="G$1" pin="1" />
                <wire x1="195.58" y1="193.04" x2="142.24" y2="193.04" width="0.1524" layer="91" />
                <label x="142.24" y="193.04" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="TP301" gate="G$1" pin="EPD_VGH" />
                <wire x1="330.2" y1="223.52" x2="276.86" y2="223.52" width="0.1524" layer="91" />
                <label x="276.86" y="223.52" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="D303" gate="G$1" pin="K" />
                <wire x1="101.6" y1="119.38" x2="109.22" y2="119.38" width="0.1524" layer="91" />
                <wire x1="109.22" y1="119.38" x2="129.54" y2="119.38" width="0.1524" layer="91" />
                <label x="109.22" y="119.38" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="EPD_VGL" class="0">
              <segment>
                <pinref part="J301" gate="G$1" pin="VGL" />
                <wire x1="86.36" y1="172.72" x2="127" y2="172.72" width="0.1524" layer="91" />
                <label x="88.9" y="172.72" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C310" gate="G$1" pin="1" />
                <wire x1="195.58" y1="177.8" x2="142.24" y2="177.8" width="0.1524" layer="91" />
                <label x="142.24" y="177.8" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="TP302" gate="G$1" pin="EPD_VGL" />
                <wire x1="330.2" y1="208.28" x2="276.86" y2="208.28" width="0.1524" layer="91" />
                <label x="276.86" y="208.28" size="1.55" layer="95" />
              </segment>
              <segment>
                <wire x1="109.22" y1="106.68" x2="129.54" y2="106.68" width="0.1524" layer="91" />
                <pinref part="D302" gate="G$1" pin="A" />
                <wire x1="124.46" y1="93.98" x2="129.54" y2="93.98" width="0.1524" layer="91" />
                <wire x1="129.54" y1="93.98" x2="129.54" y2="106.68" width="0.1524" layer="91" />
                <label x="109.22" y="106.68" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="EPD_VPP" class="0">
              <segment>
                <pinref part="J301" gate="G$1" pin="VPP" />
                <wire x1="86.36" y1="193.04" x2="127" y2="193.04" width="0.1524" layer="91" />
                <label x="88.9" y="193.04" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C306" gate="G$1" pin="1" />
                <wire x1="195.58" y1="162.56" x2="142.24" y2="162.56" width="0.1524" layer="91" />
                <label x="142.24" y="162.56" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="EPD_VSH1" class="0">
              <segment>
                <pinref part="J301" gate="G$1" pin="VSH1" />
                <wire x1="86.36" y1="187.96" x2="127" y2="187.96" width="0.1524" layer="91" />
                <label x="88.9" y="187.96" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C307" gate="G$1" pin="1" />
                <wire x1="195.58" y1="147.32" x2="142.24" y2="147.32" width="0.1524" layer="91" />
                <label x="142.24" y="147.32" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="EPD_VSH2" class="0">
              <segment>
                <pinref part="J301" gate="G$1" pin="VSH2" />
                <wire x1="50.8" y1="198.12" x2="7.62" y2="198.12" width="0.1524" layer="91" />
                <label x="7.62" y="198.12" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C303" gate="G$1" pin="1" />
                <wire x1="195.58" y1="132.08" x2="142.24" y2="132.08" width="0.1524" layer="91" />
                <label x="142.24" y="132.08" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="EPD_VSL" class="0">
              <segment>
                <pinref part="J301" gate="G$1" pin="VSL" />
                <wire x1="86.36" y1="177.8" x2="127" y2="177.8" width="0.1524" layer="91" />
                <label x="88.9" y="177.8" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C309" gate="G$1" pin="1" />
                <wire x1="195.58" y1="116.84" x2="142.24" y2="116.84" width="0.1524" layer="91" />
                <label x="142.24" y="116.84" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="GND" class="0">
              <segment>
                <pinref part="J301" gate="G$1" pin="BS1" />
                <wire x1="50.8" y1="182.88" x2="7.62" y2="182.88" width="0.1524" layer="91" />
                <label x="7.62" y="182.88" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="J301" gate="G$1" pin="VSS" />
                <wire x1="86.36" y1="203.2" x2="127" y2="203.2" width="0.1524" layer="91" />
                <label x="88.9" y="203.2" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="J301" gate="G$1" pin="SHELL1" />
                <wire x1="86.36" y1="162.56" x2="127" y2="162.56" width="0.1524" layer="91" />
                <label x="88.9" y="162.56" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="J301" gate="G$1" pin="SHELL2" />
                <wire x1="86.36" y1="157.48" x2="127" y2="157.48" width="0.1524" layer="91" />
                <label x="88.9" y="157.48" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C311" gate="G$1" pin="2" />
                <wire x1="210.82" y1="223.52" x2="261.62" y2="223.52" width="0.1524" layer="91" />
                <wire x1="261.62" y1="223.52" x2="261.62" y2="208.28" width="0.1524" layer="91" />
                <pinref part="C305" gate="G$1" pin="2" />
                <wire x1="210.82" y1="208.28" x2="261.62" y2="208.28" width="0.1524" layer="91" />
                <wire x1="261.62" y1="208.28" x2="261.62" y2="193.04" width="0.1524" layer="91" />
                <junction x="261.62" y="208.28" />
                <pinref part="C308" gate="G$1" pin="2" />
                <wire x1="210.82" y1="193.04" x2="261.62" y2="193.04" width="0.1524" layer="91" />
                <wire x1="261.62" y1="193.04" x2="261.62" y2="177.8" width="0.1524" layer="91" />
                <junction x="261.62" y="193.04" />
                <pinref part="C310" gate="G$1" pin="2" />
                <wire x1="210.82" y1="177.8" x2="261.62" y2="177.8" width="0.1524" layer="91" />
                <wire x1="261.62" y1="177.8" x2="261.62" y2="162.56" width="0.1524" layer="91" />
                <junction x="261.62" y="177.8" />
                <pinref part="C306" gate="G$1" pin="2" />
                <wire x1="210.82" y1="162.56" x2="261.62" y2="162.56" width="0.1524" layer="91" />
                <wire x1="261.62" y1="162.56" x2="261.62" y2="147.32" width="0.1524" layer="91" />
                <junction x="261.62" y="162.56" />
                <pinref part="C307" gate="G$1" pin="2" />
                <wire x1="210.82" y1="147.32" x2="261.62" y2="147.32" width="0.1524" layer="91" />
                <wire x1="261.62" y1="147.32" x2="261.62" y2="132.08" width="0.1524" layer="91" />
                <junction x="261.62" y="147.32" />
                <pinref part="C303" gate="G$1" pin="2" />
                <wire x1="210.82" y1="132.08" x2="261.62" y2="132.08" width="0.1524" layer="91" />
                <wire x1="261.62" y1="132.08" x2="261.62" y2="116.84" width="0.1524" layer="91" />
                <junction x="261.62" y="132.08" />
                <pinref part="C309" gate="G$1" pin="2" />
                <wire x1="210.82" y1="116.84" x2="261.62" y2="116.84" width="0.1524" layer="91" />
                <wire x1="261.62" y1="116.84" x2="261.62" y2="101.6" width="0.1524" layer="91" />
                <junction x="261.62" y="116.84" />
                <pinref part="C304" gate="G$1" pin="2" />
                <wire x1="210.82" y1="101.6" x2="261.62" y2="101.6" width="0.1524" layer="91" />
                <label x="213.36" y="223.52" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R305" gate="G$1" pin="2" />
                <wire x1="210.82" y1="71.12" x2="261.62" y2="71.12" width="0.1524" layer="91" />
                <label x="213.36" y="71.12" size="1.55" layer="95" />
              </segment>
              <segment>
                <wire x1="15.24" y1="35.56" x2="15.24" y2="93.98" width="0.1524" layer="91" />
                <wire x1="15.24" y1="35.56" x2="25.4" y2="35.56" width="0.1524" layer="91" />
                <pinref part="C302" gate="G$1" pin="2" />
                <wire x1="25.4" y1="35.56" x2="25.4" y2="53.34" width="0.1524" layer="91" />
                <wire x1="25.4" y1="35.56" x2="43.18" y2="35.56" width="0.1524" layer="91" />
                <junction x="25.4" y="35.56" />
                <pinref part="R301" gate="G$1" pin="1" />
                <wire x1="43.18" y1="35.56" x2="43.18" y2="53.34" width="0.1524" layer="91" />
                <wire x1="43.18" y1="35.56" x2="71.12" y2="35.56" width="0.1524" layer="91" />
                <junction x="43.18" y="35.56" />
                <pinref part="R302" gate="G$1" pin="1" />
                <wire x1="71.12" y1="35.56" x2="104.14" y2="35.56" width="0.1524" layer="91" />
                <wire x1="104.14" y1="35.56" x2="104.14" y2="58.42" width="0.1524" layer="91" />
                <pinref part="D301" gate="G$1" pin="K" />
                <label x="71.12" y="35.56" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="VMAIN" class="1">
              <segment>
                <pinref part="J301" gate="G$1" pin="VDDIO" />
                <wire x1="86.36" y1="213.36" x2="127" y2="213.36" width="0.1524" layer="91" />
                <label x="88.9" y="213.36" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="J301" gate="G$1" pin="VCI" />
                <wire x1="86.36" y1="208.28" x2="127" y2="208.28" width="0.1524" layer="91" />
                <label x="88.9" y="208.28" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C304" gate="G$1" pin="1" />
                <wire x1="195.58" y1="101.6" x2="142.24" y2="101.6" width="0.1524" layer="91" />
                <label x="142.24" y="101.6" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R303" gate="G$1" pin="2" />
                <wire x1="210.82" y1="55.88" x2="261.62" y2="55.88" width="0.1524" layer="91" />
                <wire x1="261.62" y1="55.88" x2="261.62" y2="40.64" width="0.1524" layer="91" />
                <pinref part="R304" gate="G$1" pin="2" />
                <wire x1="210.82" y1="40.64" x2="261.62" y2="40.64" width="0.1524" layer="91" />
                <label x="213.36" y="55.88" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C302" gate="G$1" pin="1" />
                <wire x1="15.24" y1="109.22" x2="15.24" y2="119.38" width="0.1524" layer="91" />
                <wire x1="15.24" y1="119.38" x2="30.48" y2="119.38" width="0.1524" layer="91" />
                <wire x1="30.48" y1="119.38" x2="48.26" y2="119.38" width="0.1524" layer="91" />
                <pinref part="L301" gate="G$1" pin="1" />
                <label x="30.48" y="119.38" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="EPD_SW" class="0">
              <segment>
                <pinref part="L301" gate="G$1" pin="2" />
                <wire x1="63.5" y1="119.38" x2="73.66" y2="119.38" width="0.1524" layer="91" />
                <pinref part="Q301" gate="G$1" pin="D" />
                <wire x1="68.58" y1="86.36" x2="73.66" y2="86.36" width="0.1524" layer="91" />
                <wire x1="73.66" y1="86.36" x2="73.66" y2="93.98" width="0.1524" layer="91" />
                <wire x1="73.66" y1="93.98" x2="73.66" y2="106.68" width="0.1524" layer="91" />
                <wire x1="73.66" y1="93.98" x2="78.74" y2="93.98" width="0.1524" layer="91" />
                <junction x="73.66" y="93.98" />
                <wire x1="73.66" y1="106.68" x2="73.66" y2="119.38" width="0.1524" layer="91" />
                <wire x1="73.66" y1="119.38" x2="86.36" y2="119.38" width="0.1524" layer="91" />
                <junction x="73.66" y="119.38" />
                <pinref part="C301" gate="G$1" pin="1" />
                <pinref part="D303" gate="G$1" pin="A" />
                <label x="73.66" y="106.68" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="EPD_PUMP" class="0">
              <segment>
                <pinref part="C301" gate="G$1" pin="2" />
                <wire x1="93.98" y1="93.98" x2="104.14" y2="93.98" width="0.1524" layer="91" />
                <pinref part="D301" gate="G$1" pin="A" />
                <wire x1="104.14" y1="73.66" x2="104.14" y2="83.82" width="0.1524" layer="91" />
                <wire x1="104.14" y1="83.82" x2="104.14" y2="93.98" width="0.1524" layer="91" />
                <wire x1="104.14" y1="93.98" x2="109.22" y2="93.98" width="0.1524" layer="91" />
                <junction x="104.14" y="93.98" />
                <pinref part="D302" gate="G$1" pin="K" />
                <label x="104.14" y="83.82" size="1.55" layer="95" />
              </segment>
            </net>
          </nets>
        </sheet>
        <sheet>
          <description>Wake timing, clock and ambient sensor</description>
          <plain>
            <wire x1="0" y1="0" x2="406.4" y2="0" width="0.25" layer="97" />
            <wire x1="406.4" y1="0" x2="406.4" y2="274.32" width="0.25" layer="97" />
            <wire x1="406.4" y1="274.32" x2="0" y2="274.32" width="0.25" layer="97" />
            <wire x1="0" y1="274.32" x2="0" y2="0" width="0.25" layer="97" />
            <text x="7.62" y="264.16" size="1.65" layer="97" font="proportional">ASTRA   /   SOLAR WEATHER STATION</text>
            <text x="7.62" y="252.73" size="4.1" layer="97" font="proportional">Wake timing, clock and ambient sensor</text>
            <text x="7.62" y="247.396" size="1.6" layer="97" font="proportional">Always-on timer, calendar alarm, environmental sensor and wake pulse</text>
            <text x="398.78" y="264.16" size="1.65" layer="97" font="proportional" align="bottom-right">PROTOTYPE  A  /  SHEET  06  OF  07</text>
            <wire x1="7.62" y1="244.602" x2="398.78" y2="244.602" width="0.2" layer="97" />
            <text x="7.62" y="4.445" size="1.55" layer="97" font="proportional">Identical net labels connect across sheets.   |   Pin numbers refer to the top-side package.</text>
            <text x="7.62" y="238.76" size="1.9" layer="97" font="proportional">ALWAYS-ON SUPPLY</text>
            <text x="7.62" y="159.512" size="1.9" layer="97" font="proportional">WAKE TIMER</text>
            <text x="142.24" y="238.76" size="1.9" layer="97" font="proportional">CLOCK AND ALARM</text>
            <text x="142.24" y="149.86" size="1.9" layer="97" font="proportional">AMBIENT SENSOR</text>
            <text x="276.86" y="238.76" size="1.9" layer="97" font="proportional">WAKE PULSE</text>
          </plain>
          <instances>
            <instance part="U401" gate="G$1" x="68.58" y="213.36" rot="R0" smashed="yes">
              <attribute name="NAME" x="58.42" y="225.044" size="2.25" layer="95" font="proportional" rot="R0" />
              <attribute name="VALUE" x="58.42" y="221.5388" size="1.7" layer="96" font="proportional" rot="R0" />
            </instance>
            <instance part="C401" gate="G$1" x="68.58" y="190.5" rot="R0" smashed="yes">
              <attribute name="NAME" x="68.58" y="193.3448" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="68.58" y="188.341" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="C402" gate="G$1" x="68.58" y="175.26" rot="R0" smashed="yes">
              <attribute name="NAME" x="68.58" y="178.1048" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="68.58" y="173.101" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="U404" gate="G$1" x="203.2" y="121.92" rot="R0" smashed="yes">
              <attribute name="NAME" x="190.5" y="136.144" size="2.25" layer="95" font="proportional" rot="R0" />
              <attribute name="VALUE" x="190.5" y="132.6388" size="1.7" layer="96" font="proportional" rot="R0" />
            </instance>
            <instance part="C405" gate="G$1" x="203.2" y="96.52" rot="R0" smashed="yes">
              <attribute name="NAME" x="203.2" y="99.3648" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="203.2" y="94.361" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="C406" gate="G$1" x="203.2" y="81.28" rot="R0" smashed="yes">
              <attribute name="NAME" x="203.2" y="84.1248" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="203.2" y="79.121" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="R405" gate="G$1" x="203.2" y="66.04" rot="R0" smashed="yes">
              <attribute name="NAME" x="203.2" y="68.8848" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="203.2" y="63.881" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="R406" gate="G$1" x="203.2" y="50.8" rot="R0" smashed="yes">
              <attribute name="NAME" x="203.2" y="53.6448" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="203.2" y="48.641" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="U405" gate="G$1" x="337.82" y="200.66" rot="R0" smashed="yes">
              <attribute name="NAME" x="322.58" y="225.044" size="2.25" layer="95" font="proportional" rot="R0" />
              <attribute name="VALUE" x="322.58" y="221.5388" size="1.7" layer="96" font="proportional" rot="R0" />
            </instance>
            <instance part="D401" gate="G$1" x="337.82" y="157.48" rot="R0" smashed="yes">
              <attribute name="NAME" x="325.12" y="166.624" size="2.25" layer="95" font="proportional" rot="R0" />
              <attribute name="VALUE" x="325.12" y="163.1188" size="1.7" layer="96" font="proportional" rot="R0" />
            </instance>
            <instance part="Q401" gate="G$1" x="337.82" y="129.54" rot="R0" smashed="yes">
              <attribute name="NAME" x="327.66" y="138.684" size="2.25" layer="95" font="proportional" rot="R0" />
              <attribute name="VALUE" x="327.66" y="135.1788" size="1.7" layer="96" font="proportional" rot="R0" />
            </instance>
            <instance part="C410" gate="G$1" x="337.82" y="109.22" rot="R0" smashed="yes">
              <attribute name="NAME" x="337.82" y="112.0648" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="337.82" y="107.061" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="C409" gate="G$1" x="337.82" y="93.98" rot="R0" smashed="yes">
              <attribute name="NAME" x="337.82" y="96.8248" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="337.82" y="91.821" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="C408" gate="G$1" x="337.82" y="78.74" rot="R0" smashed="yes">
              <attribute name="NAME" x="337.82" y="81.5848" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="337.82" y="76.581" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="R408" gate="G$1" x="337.82" y="63.5" rot="R0" smashed="yes">
              <attribute name="NAME" x="337.82" y="66.3448" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="337.82" y="61.341" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="R409" gate="G$1" x="337.82" y="48.26" rot="R0" smashed="yes">
              <attribute name="NAME" x="337.82" y="51.1048" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="337.82" y="46.101" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="R407" gate="G$1" x="337.82" y="33.02" rot="R0" smashed="yes">
              <attribute name="NAME" x="337.82" y="35.8648" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="337.82" y="30.861" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="U402" gate="G$1" x="68.58" y="104.14" rot="R0" smashed="yes">
              <attribute name="NAME" x="45.72" y="119.38" size="2.25" layer="95" font="proportional" rot="R0" align="bottom-left" />
              <attribute name="VALUE" x="45.72" y="114.3" size="1.7" layer="96" font="proportional" rot="R0" align="bottom-left" />
            </instance>
            <instance part="C403" gate="G$1" x="20.32" y="116.84" rot="R270" smashed="yes">
              <attribute name="NAME" x="22.86" y="119.38" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="22.86" y="114.3" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="R401" gate="G$1" x="35.56" y="83.82" rot="R270" smashed="yes">
              <attribute name="NAME" x="38.1" y="86.36" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="38.1" y="81.28" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="R402" gate="G$1" x="68.58" y="142.24" rot="R0" smashed="yes">
              <attribute name="NAME" x="63.5" y="147.32" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="63.5" y="137.16" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="R403" gate="G$1" x="104.14" y="129.54" rot="R270" smashed="yes">
              <attribute name="NAME" x="106.68" y="132.08" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="106.68" y="127" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="C404" gate="G$1" x="121.92" y="129.54" rot="R270" smashed="yes">
              <attribute name="NAME" x="124.46" y="132.08" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="124.46" y="127" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="U403" gate="G$1" x="205.74" y="205.74" rot="R0" smashed="yes">
              <attribute name="NAME" x="190.5" y="223.52" size="2.25" layer="95" font="proportional" rot="R0" align="bottom-left" />
              <attribute name="VALUE" x="190.5" y="218.44" size="1.7" layer="96" font="proportional" rot="R0" align="bottom-left" />
            </instance>
            <instance part="Y401" gate="G$1" x="165.1" y="218.44" rot="R270" smashed="yes">
              <attribute name="NAME" x="147.32" y="220.98" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="147.32" y="215.9" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="C407" gate="G$1" x="236.22" y="175.26" rot="R270" smashed="yes">
              <attribute name="NAME" x="238.76" y="177.8" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="238.76" y="172.72" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
            <instance part="R404" gate="G$1" x="165.1" y="185.42" rot="R0" smashed="yes">
              <attribute name="NAME" x="160.02" y="190.5" size="1.8" layer="95" font="proportional" align="bottom-left" rot="R0" />
              <attribute name="VALUE" x="160.02" y="180.34" size="1.5" layer="96" font="proportional" align="bottom-left" rot="R0" />
            </instance>
          </instances>
          <busses />
          <nets>
            <net name="ANY_KEY_N" class="0">
              <segment>
                <pinref part="U405" gate="G$1" pin="2A" />
                <wire x1="355.6" y1="218.44" x2="396.24" y2="218.44" width="0.1524" layer="91" />
                <label x="358.14" y="218.44" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="GND" class="0">
              <segment>
                <pinref part="U401" gate="G$1" pin="GND" />
                <wire x1="55.88" y1="213.36" x2="7.62" y2="213.36" width="0.1524" layer="91" />
                <label x="7.62" y="213.36" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C401" gate="G$1" pin="2" />
                <wire x1="76.2" y1="190.5" x2="127" y2="190.5" width="0.1524" layer="91" />
                <wire x1="127" y1="190.5" x2="127" y2="175.26" width="0.1524" layer="91" />
                <pinref part="C402" gate="G$1" pin="2" />
                <wire x1="76.2" y1="175.26" x2="127" y2="175.26" width="0.1524" layer="91" />
                <label x="78.74" y="190.5" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U404" gate="G$1" pin="GND1" />
                <wire x1="187.96" y1="129.54" x2="142.24" y2="129.54" width="0.1524" layer="91" />
                <label x="142.24" y="129.54" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U404" gate="G$1" pin="SDO" />
                <wire x1="218.44" y1="129.54" x2="261.62" y2="129.54" width="0.1524" layer="91" />
                <label x="220.98" y="129.54" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U404" gate="G$1" pin="GND2" />
                <wire x1="218.44" y1="119.38" x2="261.62" y2="119.38" width="0.1524" layer="91" />
                <label x="220.98" y="119.38" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C405" gate="G$1" pin="2" />
                <wire x1="210.82" y1="96.52" x2="261.62" y2="96.52" width="0.1524" layer="91" />
                <wire x1="261.62" y1="96.52" x2="261.62" y2="81.28" width="0.1524" layer="91" />
                <pinref part="C406" gate="G$1" pin="2" />
                <wire x1="210.82" y1="81.28" x2="261.62" y2="81.28" width="0.1524" layer="91" />
                <label x="213.36" y="96.52" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U405" gate="G$1" pin="2CEXT" />
                <wire x1="320.04" y1="193.04" x2="276.86" y2="193.04" width="0.1524" layer="91" />
                <label x="276.86" y="193.04" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U405" gate="G$1" pin="GND" />
                <wire x1="320.04" y1="182.88" x2="276.86" y2="182.88" width="0.1524" layer="91" />
                <label x="276.86" y="182.88" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U405" gate="G$1" pin="1CEXT" />
                <wire x1="355.6" y1="193.04" x2="396.24" y2="193.04" width="0.1524" layer="91" />
                <label x="358.14" y="193.04" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C410" gate="G$1" pin="2" />
                <wire x1="345.44" y1="109.22" x2="396.24" y2="109.22" width="0.1524" layer="91" />
                <wire x1="396.24" y1="109.22" x2="396.24" y2="93.98" width="0.1524" layer="91" />
                <pinref part="C409" gate="G$1" pin="2" />
                <wire x1="345.44" y1="93.98" x2="396.24" y2="93.98" width="0.1524" layer="91" />
                <wire x1="396.24" y1="93.98" x2="396.24" y2="78.74" width="0.1524" layer="91" />
                <junction x="396.24" y="93.98" />
                <pinref part="C408" gate="G$1" pin="2" />
                <wire x1="345.44" y1="78.74" x2="396.24" y2="78.74" width="0.1524" layer="91" />
                <label x="347.98" y="109.22" size="1.55" layer="95" />
              </segment>
              <segment>
                <wire x1="20.32" y1="68.58" x2="20.32" y2="104.14" width="0.1524" layer="91" />
                <wire x1="20.32" y1="68.58" x2="35.56" y2="68.58" width="0.1524" layer="91" />
                <wire x1="20.32" y1="104.14" x2="20.32" y2="109.22" width="0.1524" layer="91" />
                <wire x1="20.32" y1="104.14" x2="43.18" y2="104.14" width="0.1524" layer="91" />
                <junction x="20.32" y="104.14" />
                <pinref part="C403" gate="G$1" pin="2" />
                <wire x1="35.56" y1="68.58" x2="35.56" y2="76.2" width="0.1524" layer="91" />
                <wire x1="35.56" y1="68.58" x2="68.58" y2="68.58" width="0.1524" layer="91" />
                <junction x="35.56" y="68.58" />
                <pinref part="R401" gate="G$1" pin="2" />
                <pinref part="U402" gate="G$1" pin="GND" />
                <wire x1="68.58" y1="68.58" x2="104.14" y2="68.58" width="0.1524" layer="91" />
                <pinref part="U402" gate="G$1" pin="EN_ONE_SHOT" />
                <wire x1="93.98" y1="99.06" x2="104.14" y2="99.06" width="0.1524" layer="91" />
                <wire x1="104.14" y1="68.58" x2="104.14" y2="99.06" width="0.1524" layer="91" />
                <wire x1="104.14" y1="68.58" x2="129.54" y2="68.58" width="0.1524" layer="91" />
                <junction x="104.14" y="68.58" />
                <wire x1="104.14" y1="116.84" x2="104.14" y2="121.92" width="0.1524" layer="91" />
                <wire x1="104.14" y1="116.84" x2="121.92" y2="116.84" width="0.1524" layer="91" />
                <pinref part="R403" gate="G$1" pin="2" />
                <wire x1="121.92" y1="116.84" x2="121.92" y2="121.92" width="0.1524" layer="91" />
                <wire x1="121.92" y1="116.84" x2="129.54" y2="116.84" width="0.1524" layer="91" />
                <junction x="121.92" y="116.84" />
                <pinref part="C404" gate="G$1" pin="2" />
                <wire x1="129.54" y1="68.58" x2="129.54" y2="116.84" width="0.1524" layer="91" />
                <label x="68.58" y="68.58" size="1.55" layer="95" />
              </segment>
              <segment>
                <wire x1="182.88" y1="162.56" x2="182.88" y2="198.12" width="0.1524" layer="91" />
                <wire x1="182.88" y1="162.56" x2="205.74" y2="162.56" width="0.1524" layer="91" />
                <wire x1="182.88" y1="198.12" x2="187.96" y2="198.12" width="0.1524" layer="91" />
                <pinref part="U403" gate="G$1" pin="VSS" />
                <wire x1="205.74" y1="162.56" x2="236.22" y2="162.56" width="0.1524" layer="91" />
                <wire x1="236.22" y1="162.56" x2="236.22" y2="167.64" width="0.1524" layer="91" />
                <pinref part="C407" gate="G$1" pin="2" />
                <label x="205.74" y="162.56" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="KEY_MONO_RC" class="0">
              <segment>
                <pinref part="U405" gate="G$1" pin="2RCEXT" />
                <wire x1="320.04" y1="187.96" x2="276.86" y2="187.96" width="0.1524" layer="91" />
                <label x="276.86" y="187.96" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C410" gate="G$1" pin="1" />
                <wire x1="330.2" y1="109.22" x2="276.86" y2="109.22" width="0.1524" layer="91" />
                <label x="276.86" y="109.22" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R408" gate="G$1" pin="2" />
                <wire x1="345.44" y1="63.5" x2="396.24" y2="63.5" width="0.1524" layer="91" />
                <label x="347.98" y="63.5" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="KEY_PULSE_N" class="0">
              <segment>
                <pinref part="U405" gate="G$1" pin="2Qn" />
                <wire x1="355.6" y1="203.2" x2="396.24" y2="203.2" width="0.1524" layer="91" />
                <label x="358.14" y="203.2" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="D401" gate="G$1" pin="K2" />
                <wire x1="322.58" y1="154.94" x2="276.86" y2="154.94" width="0.1524" layer="91" />
                <label x="276.86" y="154.94" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="PULSE_GATE_N" class="0">
              <segment>
                <pinref part="D401" gate="G$1" pin="COM_A" />
                <wire x1="353.06" y1="160.02" x2="396.24" y2="160.02" width="0.1524" layer="91" />
                <label x="355.6" y="160.02" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="Q401" gate="G$1" pin="G" />
                <wire x1="325.12" y1="132.08" x2="276.86" y2="132.08" width="0.1524" layer="91" />
                <label x="276.86" y="132.08" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R409" gate="G$1" pin="2" />
                <wire x1="345.44" y1="48.26" x2="396.24" y2="48.26" width="0.1524" layer="91" />
                <label x="347.98" y="48.26" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="RTC_IRQ_N" class="0">
              <segment>
                <pinref part="U405" gate="G$1" pin="1A" />
                <wire x1="320.04" y1="218.44" x2="276.86" y2="218.44" width="0.1524" layer="91" />
                <label x="276.86" y="218.44" size="1.55" layer="95" />
              </segment>
              <segment>
                <wire x1="149.86" y1="203.2" x2="175.26" y2="203.2" width="0.1524" layer="91" />
                <pinref part="R404" gate="G$1" pin="2" />
                <wire x1="172.72" y1="185.42" x2="175.26" y2="185.42" width="0.1524" layer="91" />
                <wire x1="175.26" y1="185.42" x2="175.26" y2="203.2" width="0.1524" layer="91" />
                <wire x1="175.26" y1="203.2" x2="187.96" y2="203.2" width="0.1524" layer="91" />
                <junction x="175.26" y="203.2" />
                <pinref part="U403" gate="G$1" pin="INTn" />
                <label x="149.86" y="203.2" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="RTC_MONO_RC" class="0">
              <segment>
                <pinref part="U405" gate="G$1" pin="1RCEXT" />
                <wire x1="355.6" y1="187.96" x2="396.24" y2="187.96" width="0.1524" layer="91" />
                <label x="358.14" y="187.96" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C409" gate="G$1" pin="1" />
                <wire x1="330.2" y1="93.98" x2="276.86" y2="93.98" width="0.1524" layer="91" />
                <label x="276.86" y="93.98" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R407" gate="G$1" pin="2" />
                <wire x1="345.44" y1="33.02" x2="396.24" y2="33.02" width="0.1524" layer="91" />
                <label x="347.98" y="33.02" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="RTC_PULSE_N" class="0">
              <segment>
                <pinref part="U405" gate="G$1" pin="1Qn" />
                <wire x1="320.04" y1="203.2" x2="276.86" y2="203.2" width="0.1524" layer="91" />
                <label x="276.86" y="203.2" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="D401" gate="G$1" pin="K1" />
                <wire x1="322.58" y1="160.02" x2="276.86" y2="160.02" width="0.1524" layer="91" />
                <label x="276.86" y="160.02" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="SCL" class="0">
              <segment>
                <pinref part="U404" gate="G$1" pin="SCK" />
                <wire x1="187.96" y1="114.3" x2="142.24" y2="114.3" width="0.1524" layer="91" />
                <label x="142.24" y="114.3" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R405" gate="G$1" pin="2" />
                <wire x1="210.82" y1="66.04" x2="261.62" y2="66.04" width="0.1524" layer="91" />
                <label x="213.36" y="66.04" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U403" gate="G$1" pin="SCL" />
                <wire x1="223.52" y1="208.28" x2="231.14" y2="208.28" width="0.1524" layer="91" />
                <wire x1="231.14" y1="208.28" x2="248.92" y2="208.28" width="0.1524" layer="91" />
                <label x="231.14" y="208.28" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="SDA" class="0">
              <segment>
                <pinref part="U404" gate="G$1" pin="SDI" />
                <wire x1="187.96" y1="119.38" x2="142.24" y2="119.38" width="0.1524" layer="91" />
                <label x="142.24" y="119.38" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R406" gate="G$1" pin="2" />
                <wire x1="210.82" y1="50.8" x2="261.62" y2="50.8" width="0.1524" layer="91" />
                <label x="213.36" y="50.8" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U403" gate="G$1" pin="SDA" />
                <wire x1="223.52" y1="213.36" x2="231.14" y2="213.36" width="0.1524" layer="91" />
                <wire x1="231.14" y1="213.36" x2="248.92" y2="213.36" width="0.1524" layer="91" />
                <label x="231.14" y="213.36" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="SYS_AON" class="1">
              <segment>
                <pinref part="U401" gate="G$1" pin="IN" />
                <wire x1="55.88" y1="218.44" x2="7.62" y2="218.44" width="0.1524" layer="91" />
                <label x="7.62" y="218.44" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U401" gate="G$1" pin="EN" />
                <wire x1="55.88" y1="208.28" x2="7.62" y2="208.28" width="0.1524" layer="91" />
                <label x="7.62" y="208.28" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C401" gate="G$1" pin="1" />
                <wire x1="60.96" y1="190.5" x2="7.62" y2="190.5" width="0.1524" layer="91" />
                <label x="7.62" y="190.5" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="VAON" class="0">
              <segment>
                <pinref part="U401" gate="G$1" pin="OUT" />
                <wire x1="81.28" y1="213.36" x2="127" y2="213.36" width="0.1524" layer="91" />
                <label x="83.82" y="213.36" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C402" gate="G$1" pin="1" />
                <wire x1="60.96" y1="175.26" x2="7.62" y2="175.26" width="0.1524" layer="91" />
                <label x="7.62" y="175.26" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U405" gate="G$1" pin="1B" />
                <wire x1="320.04" y1="213.36" x2="276.86" y2="213.36" width="0.1524" layer="91" />
                <label x="276.86" y="213.36" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U405" gate="G$1" pin="1RDn" />
                <wire x1="320.04" y1="208.28" x2="276.86" y2="208.28" width="0.1524" layer="91" />
                <label x="276.86" y="208.28" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U405" gate="G$1" pin="2B" />
                <wire x1="355.6" y1="213.36" x2="396.24" y2="213.36" width="0.1524" layer="91" />
                <label x="358.14" y="213.36" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U405" gate="G$1" pin="2RDn" />
                <wire x1="355.6" y1="208.28" x2="396.24" y2="208.28" width="0.1524" layer="91" />
                <label x="358.14" y="208.28" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U405" gate="G$1" pin="VCC" />
                <wire x1="355.6" y1="182.88" x2="396.24" y2="182.88" width="0.1524" layer="91" />
                <label x="358.14" y="182.88" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="Q401" gate="G$1" pin="S" />
                <wire x1="325.12" y1="127" x2="276.86" y2="127" width="0.1524" layer="91" />
                <label x="276.86" y="127" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C408" gate="G$1" pin="1" />
                <wire x1="330.2" y1="78.74" x2="276.86" y2="78.74" width="0.1524" layer="91" />
                <wire x1="276.86" y1="78.74" x2="276.86" y2="63.5" width="0.1524" layer="91" />
                <pinref part="R408" gate="G$1" pin="1" />
                <wire x1="330.2" y1="63.5" x2="276.86" y2="63.5" width="0.1524" layer="91" />
                <wire x1="276.86" y1="63.5" x2="276.86" y2="48.26" width="0.1524" layer="91" />
                <junction x="276.86" y="63.5" />
                <pinref part="R409" gate="G$1" pin="1" />
                <wire x1="330.2" y1="48.26" x2="276.86" y2="48.26" width="0.1524" layer="91" />
                <wire x1="276.86" y1="48.26" x2="276.86" y2="33.02" width="0.1524" layer="91" />
                <junction x="276.86" y="48.26" />
                <pinref part="R407" gate="G$1" pin="1" />
                <wire x1="330.2" y1="33.02" x2="276.86" y2="33.02" width="0.1524" layer="91" />
                <label x="276.86" y="78.74" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C403" gate="G$1" pin="1" />
                <wire x1="20.32" y1="124.46" x2="20.32" y2="127" width="0.1524" layer="91" />
                <wire x1="20.32" y1="127" x2="35.56" y2="127" width="0.1524" layer="91" />
                <wire x1="35.56" y1="109.22" x2="35.56" y2="127" width="0.1524" layer="91" />
                <wire x1="35.56" y1="109.22" x2="43.18" y2="109.22" width="0.1524" layer="91" />
                <pinref part="U402" gate="G$1" pin="VDD" />
                <label x="20.32" y="127" size="1.55" layer="95" />
              </segment>
              <segment>
                <wire x1="147.32" y1="185.42" x2="157.48" y2="185.42" width="0.1524" layer="91" />
                <pinref part="R404" gate="G$1" pin="1" />
                <label x="147.32" y="185.42" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U403" gate="G$1" pin="VDD" />
                <wire x1="223.52" y1="198.12" x2="236.22" y2="198.12" width="0.1524" layer="91" />
                <pinref part="C407" gate="G$1" pin="1" />
                <wire x1="236.22" y1="182.88" x2="236.22" y2="198.12" width="0.1524" layer="91" />
                <wire x1="236.22" y1="198.12" x2="241.3" y2="198.12" width="0.1524" layer="91" />
                <junction x="236.22" y="198.12" />
                <wire x1="241.3" y1="198.12" x2="248.92" y2="198.12" width="0.1524" layer="91" />
                <label x="241.3" y="198.12" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="VMAIN" class="1">
              <segment>
                <pinref part="U404" gate="G$1" pin="CSB" />
                <wire x1="187.96" y1="124.46" x2="142.24" y2="124.46" width="0.1524" layer="91" />
                <label x="142.24" y="124.46" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U404" gate="G$1" pin="VDDIO" />
                <wire x1="218.44" y1="124.46" x2="261.62" y2="124.46" width="0.1524" layer="91" />
                <label x="220.98" y="124.46" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U404" gate="G$1" pin="VDD" />
                <wire x1="218.44" y1="114.3" x2="261.62" y2="114.3" width="0.1524" layer="91" />
                <label x="220.98" y="114.3" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C405" gate="G$1" pin="1" />
                <wire x1="195.58" y1="96.52" x2="142.24" y2="96.52" width="0.1524" layer="91" />
                <wire x1="142.24" y1="96.52" x2="142.24" y2="81.28" width="0.1524" layer="91" />
                <pinref part="C406" gate="G$1" pin="1" />
                <wire x1="195.58" y1="81.28" x2="142.24" y2="81.28" width="0.1524" layer="91" />
                <wire x1="142.24" y1="81.28" x2="142.24" y2="66.04" width="0.1524" layer="91" />
                <junction x="142.24" y="81.28" />
                <pinref part="R405" gate="G$1" pin="1" />
                <wire x1="195.58" y1="66.04" x2="142.24" y2="66.04" width="0.1524" layer="91" />
                <wire x1="142.24" y1="66.04" x2="142.24" y2="50.8" width="0.1524" layer="91" />
                <junction x="142.24" y="66.04" />
                <pinref part="R406" gate="G$1" pin="1" />
                <wire x1="195.58" y1="50.8" x2="142.24" y2="50.8" width="0.1524" layer="91" />
                <label x="142.24" y="96.52" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="WAKE_MDRV" class="0">
              <segment>
                <pinref part="Q401" gate="G$1" pin="D" />
                <wire x1="350.52" y1="132.08" x2="396.24" y2="132.08" width="0.1524" layer="91" />
                <label x="353.06" y="132.08" size="1.55" layer="95" />
              </segment>
              <segment>
                <wire x1="27.94" y1="99.06" x2="35.56" y2="99.06" width="0.1524" layer="91" />
                <pinref part="R401" gate="G$1" pin="1" />
                <wire x1="35.56" y1="91.44" x2="35.56" y2="99.06" width="0.1524" layer="91" />
                <wire x1="35.56" y1="99.06" x2="43.18" y2="99.06" width="0.1524" layer="91" />
                <junction x="35.56" y="99.06" />
                <pinref part="U402" gate="G$1" pin="DELAY_MDRV" />
                <label x="27.94" y="99.06" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="TIMER_DONE" class="0">
              <segment>
                <wire x1="38.1" y1="142.24" x2="60.96" y2="142.24" width="0.1524" layer="91" />
                <pinref part="R402" gate="G$1" pin="1" />
                <label x="38.1" y="142.24" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="DONE_2V8" class="0">
              <segment>
                <pinref part="R402" gate="G$1" pin="2" />
                <wire x1="76.2" y1="142.24" x2="78.74" y2="142.24" width="0.1524" layer="91" />
                <wire x1="78.74" y1="142.24" x2="96.52" y2="142.24" width="0.1524" layer="91" />
                <pinref part="U402" gate="G$1" pin="DONE" />
                <wire x1="93.98" y1="109.22" x2="96.52" y2="109.22" width="0.1524" layer="91" />
                <wire x1="96.52" y1="109.22" x2="96.52" y2="142.24" width="0.1524" layer="91" />
                <wire x1="96.52" y1="142.24" x2="104.14" y2="142.24" width="0.1524" layer="91" />
                <junction x="96.52" y="142.24" />
                <pinref part="R403" gate="G$1" pin="1" />
                <wire x1="104.14" y1="137.16" x2="104.14" y2="142.24" width="0.1524" layer="91" />
                <wire x1="104.14" y1="142.24" x2="121.92" y2="142.24" width="0.1524" layer="91" />
                <junction x="104.14" y="142.24" />
                <pinref part="C404" gate="G$1" pin="1" />
                <wire x1="121.92" y1="137.16" x2="121.92" y2="142.24" width="0.1524" layer="91" />
                <label x="78.74" y="142.24" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="MAIN_EN" class="0">
              <segment>
                <pinref part="U402" gate="G$1" pin="DRVn" />
                <wire x1="93.98" y1="104.14" x2="106.68" y2="104.14" width="0.1524" layer="91" />
                <wire x1="106.68" y1="104.14" x2="121.92" y2="104.14" width="0.1524" layer="91" />
                <label x="106.68" y="104.14" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="RTC_XI" class="0">
              <segment>
                <pinref part="Y401" gate="G$1" pin="XTAL1" />
                <wire x1="165.1" y1="226.06" x2="165.1" y2="228.6" width="0.1524" layer="91" />
                <wire x1="165.1" y1="228.6" x2="180.34" y2="228.6" width="0.1524" layer="91" />
                <wire x1="180.34" y1="213.36" x2="180.34" y2="228.6" width="0.1524" layer="91" />
                <wire x1="180.34" y1="213.36" x2="187.96" y2="213.36" width="0.1524" layer="91" />
                <pinref part="U403" gate="G$1" pin="OSCI" />
                <label x="165.1" y="228.6" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="RTC_XO" class="0">
              <segment>
                <wire x1="165.1" y1="208.28" x2="165.1" y2="210.82" width="0.1524" layer="91" />
                <wire x1="165.1" y1="208.28" x2="172.72" y2="208.28" width="0.1524" layer="91" />
                <pinref part="Y401" gate="G$1" pin="XTAL2" />
                <wire x1="172.72" y1="208.28" x2="187.96" y2="208.28" width="0.1524" layer="91" />
                <pinref part="U403" gate="G$1" pin="OSCO" />
                <label x="172.72" y="208.28" size="1.55" layer="95" />
              </segment>
            </net>
          </nets>
        </sheet>
        <sheet>
          <description>User controls and battery measurement</description>
          <plain>
            <wire x1="0" y1="0" x2="406.4" y2="0" width="0.25" layer="97" />
            <wire x1="406.4" y1="0" x2="406.4" y2="274.32" width="0.25" layer="97" />
            <wire x1="406.4" y1="274.32" x2="0" y2="274.32" width="0.25" layer="97" />
            <wire x1="0" y1="274.32" x2="0" y2="0" width="0.25" layer="97" />
            <text x="7.62" y="264.16" size="1.65" layer="97" font="proportional">ASTRA   /   SOLAR WEATHER STATION</text>
            <text x="7.62" y="252.73" size="4.1" layer="97" font="proportional">User controls and battery measurement</text>
            <text x="7.62" y="247.396" size="1.6" layer="97" font="proportional">Three wake keys, key decoding and the switched battery divider</text>
            <text x="398.78" y="264.16" size="1.65" layer="97" font="proportional" align="bottom-right">PROTOTYPE  A  /  SHEET  07  OF  07</text>
            <wire x1="7.62" y1="244.602" x2="398.78" y2="244.602" width="0.2" layer="97" />
            <text x="7.62" y="4.445" size="1.55" layer="97" font="proportional">Identical net labels connect across sheets.   |   Pin numbers refer to the top-side package.</text>
            <text x="7.62" y="238.76" size="1.9" layer="97" font="proportional">USER KEYS</text>
            <text x="142.24" y="238.76" size="1.9" layer="97" font="proportional">USER KEYS</text>
            <text x="276.86" y="238.76" size="1.9" layer="97" font="proportional">BATTERY ADC</text>
          </plain>
          <instances>
            <instance part="U406" gate="G$1" x="68.58" y="210.82" rot="R0" smashed="yes">
              <attribute name="NAME" x="58.42" y="225.044" size="2.25" layer="95" font="proportional" rot="R0" />
              <attribute name="VALUE" x="58.42" y="221.5388" size="1.7" layer="96" font="proportional" rot="R0" />
            </instance>
            <instance part="SW401" gate="G$1" x="68.58" y="177.8" rot="R0" smashed="yes">
              <attribute name="NAME" x="58.42" y="186.944" size="2.25" layer="95" font="proportional" rot="R0" />
              <attribute name="VALUE" x="58.42" y="183.4388" size="1.7" layer="96" font="proportional" rot="R0" />
            </instance>
            <instance part="SW402" gate="G$1" x="68.58" y="149.86" rot="R0" smashed="yes">
              <attribute name="NAME" x="58.42" y="159.004" size="2.25" layer="95" font="proportional" rot="R0" />
              <attribute name="VALUE" x="58.42" y="155.4988" size="1.7" layer="96" font="proportional" rot="R0" />
            </instance>
            <instance part="SW403" gate="G$1" x="68.58" y="121.92" rot="R0" smashed="yes">
              <attribute name="NAME" x="58.42" y="131.064" size="2.25" layer="95" font="proportional" rot="R0" />
              <attribute name="VALUE" x="58.42" y="127.5588" size="1.7" layer="96" font="proportional" rot="R0" />
            </instance>
            <instance part="D402" gate="G$1" x="68.58" y="93.98" rot="R0" smashed="yes">
              <attribute name="NAME" x="55.88" y="103.124" size="2.25" layer="95" font="proportional" rot="R0" />
              <attribute name="VALUE" x="55.88" y="99.6188" size="1.7" layer="96" font="proportional" rot="R0" />
            </instance>
            <instance part="D403" gate="G$1" x="68.58" y="66.04" rot="R0" smashed="yes">
              <attribute name="NAME" x="55.88" y="75.184" size="2.25" layer="95" font="proportional" rot="R0" />
              <attribute name="VALUE" x="55.88" y="71.6788" size="1.7" layer="96" font="proportional" rot="R0" />
            </instance>
            <instance part="C412" gate="G$1" x="68.58" y="45.72" rot="R0" smashed="yes">
              <attribute name="NAME" x="68.58" y="48.5648" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="68.58" y="43.561" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="R417" gate="G$1" x="68.58" y="30.48" rot="R0" smashed="yes">
              <attribute name="NAME" x="68.58" y="33.3248" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="68.58" y="28.321" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="R414" gate="G$1" x="203.2" y="223.52" rot="R0" smashed="yes">
              <attribute name="NAME" x="203.2" y="226.3648" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="203.2" y="221.361" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="C413" gate="G$1" x="203.2" y="208.28" rot="R0" smashed="yes">
              <attribute name="NAME" x="203.2" y="211.1248" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="203.2" y="206.121" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="R418" gate="G$1" x="203.2" y="193.04" rot="R0" smashed="yes">
              <attribute name="NAME" x="203.2" y="195.8848" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="203.2" y="190.881" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="R415" gate="G$1" x="203.2" y="177.8" rot="R0" smashed="yes">
              <attribute name="NAME" x="203.2" y="180.6448" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="203.2" y="175.641" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="C414" gate="G$1" x="203.2" y="162.56" rot="R0" smashed="yes">
              <attribute name="NAME" x="203.2" y="165.4048" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="203.2" y="160.401" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="R419" gate="G$1" x="203.2" y="147.32" rot="R0" smashed="yes">
              <attribute name="NAME" x="203.2" y="150.1648" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="203.2" y="145.161" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="R416" gate="G$1" x="203.2" y="132.08" rot="R0" smashed="yes">
              <attribute name="NAME" x="203.2" y="134.9248" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="203.2" y="129.921" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="R410" gate="G$1" x="203.2" y="116.84" rot="R0" smashed="yes">
              <attribute name="NAME" x="203.2" y="119.6848" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="203.2" y="114.681" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="R411" gate="G$1" x="203.2" y="101.6" rot="R0" smashed="yes">
              <attribute name="NAME" x="203.2" y="104.4448" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="203.2" y="99.441" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="R412" gate="G$1" x="203.2" y="86.36" rot="R0" smashed="yes">
              <attribute name="NAME" x="203.2" y="89.2048" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="203.2" y="84.201" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="R413" gate="G$1" x="203.2" y="71.12" rot="R0" smashed="yes">
              <attribute name="NAME" x="203.2" y="73.9648" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="203.2" y="68.961" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="C411" gate="G$1" x="203.2" y="55.88" rot="R0" smashed="yes">
              <attribute name="NAME" x="203.2" y="58.7248" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="203.2" y="53.721" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="U407" gate="G$1" x="337.82" y="213.36" rot="R0" smashed="yes">
              <attribute name="NAME" x="327.66" y="225.044" size="2.25" layer="95" font="proportional" rot="R0" />
              <attribute name="VALUE" x="327.66" y="221.5388" size="1.7" layer="96" font="proportional" rot="R0" />
            </instance>
            <instance part="U408" gate="G$1" x="337.82" y="180.34" rot="R0" smashed="yes">
              <attribute name="NAME" x="327.66" y="192.024" size="2.25" layer="95" font="proportional" rot="R0" />
              <attribute name="VALUE" x="327.66" y="188.5188" size="1.7" layer="96" font="proportional" rot="R0" />
            </instance>
            <instance part="C418" gate="G$1" x="337.82" y="157.48" rot="R0" smashed="yes">
              <attribute name="NAME" x="337.82" y="160.3248" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="337.82" y="155.321" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="R423" gate="G$1" x="337.82" y="142.24" rot="R0" smashed="yes">
              <attribute name="NAME" x="337.82" y="145.0848" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="337.82" y="140.081" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="R424" gate="G$1" x="337.82" y="127" rot="R0" smashed="yes">
              <attribute name="NAME" x="337.82" y="129.8448" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="337.82" y="124.841" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="C417" gate="G$1" x="337.82" y="111.76" rot="R0" smashed="yes">
              <attribute name="NAME" x="337.82" y="114.6048" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="337.82" y="109.601" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="C415" gate="G$1" x="337.82" y="96.52" rot="R0" smashed="yes">
              <attribute name="NAME" x="337.82" y="99.3648" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="337.82" y="94.361" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="R420" gate="G$1" x="337.82" y="81.28" rot="R0" smashed="yes">
              <attribute name="NAME" x="337.82" y="84.1248" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="337.82" y="79.121" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="R422" gate="G$1" x="337.82" y="66.04" rot="R0" smashed="yes">
              <attribute name="NAME" x="337.82" y="68.8848" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="337.82" y="63.881" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="C416" gate="G$1" x="337.82" y="50.8" rot="R0" smashed="yes">
              <attribute name="NAME" x="337.82" y="53.6448" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="337.82" y="48.641" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
            <instance part="R421" gate="G$1" x="337.82" y="35.56" rot="R0" smashed="yes">
              <attribute name="NAME" x="337.82" y="38.4048" size="1.8" layer="95" font="proportional" align="bottom-center" rot="R0" />
              <attribute name="VALUE" x="337.82" y="33.401" size="1.5" layer="96" font="proportional" align="top-center" rot="R0" />
            </instance>
          </instances>
          <busses />
          <nets>
            <net name="ANY_KEY_N" class="0">
              <segment>
                <pinref part="D402" gate="G$1" pin="COM_A" />
                <wire x1="83.82" y1="96.52" x2="127" y2="96.52" width="0.1524" layer="91" />
                <label x="86.36" y="96.52" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="D403" gate="G$1" pin="COM_A" />
                <wire x1="83.82" y1="68.58" x2="127" y2="68.58" width="0.1524" layer="91" />
                <label x="86.36" y="68.58" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R410" gate="G$1" pin="2" />
                <wire x1="210.82" y1="116.84" x2="261.62" y2="116.84" width="0.1524" layer="91" />
                <label x="213.36" y="116.84" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="BTN1" class="0">
              <segment>
                <pinref part="R417" gate="G$1" pin="2" />
                <wire x1="76.2" y1="30.48" x2="127" y2="30.48" width="0.1524" layer="91" />
                <label x="78.74" y="30.48" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="BTN2" class="0">
              <segment>
                <pinref part="R418" gate="G$1" pin="2" />
                <wire x1="210.82" y1="193.04" x2="261.62" y2="193.04" width="0.1524" layer="91" />
                <label x="213.36" y="193.04" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="BTN3" class="0">
              <segment>
                <pinref part="R419" gate="G$1" pin="2" />
                <wire x1="210.82" y1="147.32" x2="261.62" y2="147.32" width="0.1524" layer="91" />
                <label x="213.36" y="147.32" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="GND" class="0">
              <segment>
                <pinref part="U406" gate="G$1" pin="GND" />
                <wire x1="55.88" y1="203.2" x2="7.62" y2="203.2" width="0.1524" layer="91" />
                <label x="7.62" y="203.2" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="SW401" gate="G$1" pin="B1" />
                <wire x1="81.28" y1="180.34" x2="127" y2="180.34" width="0.1524" layer="91" />
                <label x="83.82" y="180.34" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="SW401" gate="G$1" pin="B2" />
                <wire x1="81.28" y1="175.26" x2="127" y2="175.26" width="0.1524" layer="91" />
                <label x="83.82" y="175.26" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="SW402" gate="G$1" pin="B1" />
                <wire x1="81.28" y1="152.4" x2="127" y2="152.4" width="0.1524" layer="91" />
                <label x="83.82" y="152.4" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="SW402" gate="G$1" pin="B2" />
                <wire x1="81.28" y1="147.32" x2="127" y2="147.32" width="0.1524" layer="91" />
                <label x="83.82" y="147.32" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="SW403" gate="G$1" pin="B1" />
                <wire x1="81.28" y1="124.46" x2="127" y2="124.46" width="0.1524" layer="91" />
                <label x="83.82" y="124.46" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="SW403" gate="G$1" pin="B2" />
                <wire x1="81.28" y1="119.38" x2="127" y2="119.38" width="0.1524" layer="91" />
                <label x="83.82" y="119.38" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C412" gate="G$1" pin="2" />
                <wire x1="76.2" y1="45.72" x2="127" y2="45.72" width="0.1524" layer="91" />
                <label x="78.74" y="45.72" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C413" gate="G$1" pin="2" />
                <wire x1="210.82" y1="208.28" x2="261.62" y2="208.28" width="0.1524" layer="91" />
                <label x="213.36" y="208.28" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C414" gate="G$1" pin="2" />
                <wire x1="210.82" y1="162.56" x2="261.62" y2="162.56" width="0.1524" layer="91" />
                <label x="213.36" y="162.56" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C411" gate="G$1" pin="2" />
                <wire x1="210.82" y1="55.88" x2="261.62" y2="55.88" width="0.1524" layer="91" />
                <label x="213.36" y="55.88" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U407" gate="G$1" pin="GND" />
                <wire x1="325.12" y1="213.36" x2="276.86" y2="213.36" width="0.1524" layer="91" />
                <label x="276.86" y="213.36" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U408" gate="G$1" pin="B" />
                <wire x1="325.12" y1="185.42" x2="276.86" y2="185.42" width="0.1524" layer="91" />
                <label x="276.86" y="185.42" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U408" gate="G$1" pin="GND" />
                <wire x1="325.12" y1="180.34" x2="276.86" y2="180.34" width="0.1524" layer="91" />
                <label x="276.86" y="180.34" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C418" gate="G$1" pin="2" />
                <wire x1="345.44" y1="157.48" x2="396.24" y2="157.48" width="0.1524" layer="91" />
                <wire x1="396.24" y1="157.48" x2="396.24" y2="142.24" width="0.1524" layer="91" />
                <pinref part="R423" gate="G$1" pin="2" />
                <wire x1="345.44" y1="142.24" x2="396.24" y2="142.24" width="0.1524" layer="91" />
                <wire x1="396.24" y1="142.24" x2="396.24" y2="127" width="0.1524" layer="91" />
                <junction x="396.24" y="142.24" />
                <pinref part="R424" gate="G$1" pin="2" />
                <wire x1="345.44" y1="127" x2="396.24" y2="127" width="0.1524" layer="91" />
                <wire x1="396.24" y1="127" x2="396.24" y2="111.76" width="0.1524" layer="91" />
                <junction x="396.24" y="127" />
                <pinref part="C417" gate="G$1" pin="2" />
                <wire x1="345.44" y1="111.76" x2="396.24" y2="111.76" width="0.1524" layer="91" />
                <wire x1="396.24" y1="111.76" x2="396.24" y2="96.52" width="0.1524" layer="91" />
                <junction x="396.24" y="111.76" />
                <pinref part="C415" gate="G$1" pin="2" />
                <wire x1="345.44" y1="96.52" x2="396.24" y2="96.52" width="0.1524" layer="91" />
                <label x="347.98" y="157.48" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C416" gate="G$1" pin="2" />
                <wire x1="345.44" y1="50.8" x2="396.24" y2="50.8" width="0.1524" layer="91" />
                <wire x1="396.24" y1="50.8" x2="396.24" y2="35.56" width="0.1524" layer="91" />
                <pinref part="R421" gate="G$1" pin="2" />
                <wire x1="345.44" y1="35.56" x2="396.24" y2="35.56" width="0.1524" layer="91" />
                <label x="347.98" y="50.8" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="KEY1_N" class="0">
              <segment>
                <pinref part="U406" gate="G$1" pin="1A" />
                <wire x1="55.88" y1="218.44" x2="7.62" y2="218.44" width="0.1524" layer="91" />
                <label x="7.62" y="218.44" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="D402" gate="G$1" pin="K1" />
                <wire x1="53.34" y1="96.52" x2="7.62" y2="96.52" width="0.1524" layer="91" />
                <label x="7.62" y="96.52" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C412" gate="G$1" pin="1" />
                <wire x1="60.96" y1="45.72" x2="7.62" y2="45.72" width="0.1524" layer="91" />
                <label x="7.62" y="45.72" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R414" gate="G$1" pin="2" />
                <wire x1="210.82" y1="223.52" x2="261.62" y2="223.52" width="0.1524" layer="91" />
                <label x="213.36" y="223.52" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R411" gate="G$1" pin="2" />
                <wire x1="210.82" y1="101.6" x2="261.62" y2="101.6" width="0.1524" layer="91" />
                <label x="213.36" y="101.6" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="KEY1_OUT" class="0">
              <segment>
                <pinref part="U406" gate="G$1" pin="1Y" />
                <wire x1="81.28" y1="208.28" x2="127" y2="208.28" width="0.1524" layer="91" />
                <label x="83.82" y="208.28" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R417" gate="G$1" pin="1" />
                <wire x1="60.96" y1="30.48" x2="7.62" y2="30.48" width="0.1524" layer="91" />
                <label x="7.62" y="30.48" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="KEY1_SW" class="0">
              <segment>
                <pinref part="SW401" gate="G$1" pin="A1" />
                <wire x1="55.88" y1="180.34" x2="7.62" y2="180.34" width="0.1524" layer="91" />
                <label x="7.62" y="180.34" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="SW401" gate="G$1" pin="A2" />
                <wire x1="55.88" y1="175.26" x2="7.62" y2="175.26" width="0.1524" layer="91" />
                <label x="7.62" y="175.26" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R414" gate="G$1" pin="1" />
                <wire x1="195.58" y1="223.52" x2="142.24" y2="223.52" width="0.1524" layer="91" />
                <label x="142.24" y="223.52" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="KEY2_N" class="0">
              <segment>
                <pinref part="U406" gate="G$1" pin="2A" />
                <wire x1="55.88" y1="208.28" x2="7.62" y2="208.28" width="0.1524" layer="91" />
                <label x="7.62" y="208.28" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="D402" gate="G$1" pin="K2" />
                <wire x1="53.34" y1="91.44" x2="7.62" y2="91.44" width="0.1524" layer="91" />
                <label x="7.62" y="91.44" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C413" gate="G$1" pin="1" />
                <wire x1="195.58" y1="208.28" x2="142.24" y2="208.28" width="0.1524" layer="91" />
                <label x="142.24" y="208.28" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R415" gate="G$1" pin="2" />
                <wire x1="210.82" y1="177.8" x2="261.62" y2="177.8" width="0.1524" layer="91" />
                <label x="213.36" y="177.8" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R412" gate="G$1" pin="2" />
                <wire x1="210.82" y1="86.36" x2="261.62" y2="86.36" width="0.1524" layer="91" />
                <label x="213.36" y="86.36" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="KEY2_OUT" class="0">
              <segment>
                <pinref part="U406" gate="G$1" pin="2Y" />
                <wire x1="81.28" y1="218.44" x2="127" y2="218.44" width="0.1524" layer="91" />
                <label x="83.82" y="218.44" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R418" gate="G$1" pin="1" />
                <wire x1="195.58" y1="193.04" x2="142.24" y2="193.04" width="0.1524" layer="91" />
                <label x="142.24" y="193.04" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="KEY2_SW" class="0">
              <segment>
                <pinref part="SW402" gate="G$1" pin="A1" />
                <wire x1="55.88" y1="152.4" x2="7.62" y2="152.4" width="0.1524" layer="91" />
                <label x="7.62" y="152.4" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="SW402" gate="G$1" pin="A2" />
                <wire x1="55.88" y1="147.32" x2="7.62" y2="147.32" width="0.1524" layer="91" />
                <label x="7.62" y="147.32" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R415" gate="G$1" pin="1" />
                <wire x1="195.58" y1="177.8" x2="142.24" y2="177.8" width="0.1524" layer="91" />
                <label x="142.24" y="177.8" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="KEY3_N" class="0">
              <segment>
                <pinref part="U406" gate="G$1" pin="3A" />
                <wire x1="81.28" y1="213.36" x2="127" y2="213.36" width="0.1524" layer="91" />
                <label x="83.82" y="213.36" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="D403" gate="G$1" pin="K1" />
                <wire x1="53.34" y1="68.58" x2="7.62" y2="68.58" width="0.1524" layer="91" />
                <label x="7.62" y="68.58" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="D403" gate="G$1" pin="K2" />
                <wire x1="53.34" y1="63.5" x2="7.62" y2="63.5" width="0.1524" layer="91" />
                <label x="7.62" y="63.5" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C414" gate="G$1" pin="1" />
                <wire x1="195.58" y1="162.56" x2="142.24" y2="162.56" width="0.1524" layer="91" />
                <label x="142.24" y="162.56" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R416" gate="G$1" pin="2" />
                <wire x1="210.82" y1="132.08" x2="261.62" y2="132.08" width="0.1524" layer="91" />
                <label x="213.36" y="132.08" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R413" gate="G$1" pin="2" />
                <wire x1="210.82" y1="71.12" x2="261.62" y2="71.12" width="0.1524" layer="91" />
                <label x="213.36" y="71.12" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="KEY3_OUT" class="0">
              <segment>
                <pinref part="U406" gate="G$1" pin="3Y" />
                <wire x1="55.88" y1="213.36" x2="7.62" y2="213.36" width="0.1524" layer="91" />
                <label x="7.62" y="213.36" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R419" gate="G$1" pin="1" />
                <wire x1="195.58" y1="147.32" x2="142.24" y2="147.32" width="0.1524" layer="91" />
                <label x="142.24" y="147.32" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="KEY3_SW" class="0">
              <segment>
                <pinref part="SW403" gate="G$1" pin="A1" />
                <wire x1="55.88" y1="124.46" x2="7.62" y2="124.46" width="0.1524" layer="91" />
                <label x="7.62" y="124.46" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="SW403" gate="G$1" pin="A2" />
                <wire x1="55.88" y1="119.38" x2="7.62" y2="119.38" width="0.1524" layer="91" />
                <label x="7.62" y="119.38" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R416" gate="G$1" pin="1" />
                <wire x1="195.58" y1="132.08" x2="142.24" y2="132.08" width="0.1524" layer="91" />
                <label x="142.24" y="132.08" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="MAIN_EN" class="0">
              <segment>
                <pinref part="U408" gate="G$1" pin="C" />
                <wire x1="350.52" y1="175.26" x2="396.24" y2="175.26" width="0.1524" layer="91" />
                <label x="353.06" y="175.26" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="MEAS_FILTER" class="0">
              <segment>
                <pinref part="U408" gate="G$1" pin="A" />
                <wire x1="325.12" y1="175.26" x2="276.86" y2="175.26" width="0.1524" layer="91" />
                <label x="276.86" y="175.26" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C418" gate="G$1" pin="1" />
                <wire x1="330.2" y1="157.48" x2="276.86" y2="157.48" width="0.1524" layer="91" />
                <wire x1="276.86" y1="157.48" x2="276.86" y2="142.24" width="0.1524" layer="91" />
                <pinref part="R423" gate="G$1" pin="1" />
                <wire x1="330.2" y1="142.24" x2="276.86" y2="142.24" width="0.1524" layer="91" />
                <label x="276.86" y="157.48" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R422" gate="G$1" pin="2" />
                <wire x1="345.44" y1="66.04" x2="396.24" y2="66.04" width="0.1524" layer="91" />
                <label x="347.98" y="66.04" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="SENSE_SWITCH_EN" class="0">
              <segment>
                <pinref part="U407" gate="G$1" pin="ON" />
                <wire x1="325.12" y1="208.28" x2="276.86" y2="208.28" width="0.1524" layer="91" />
                <label x="276.86" y="208.28" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U408" gate="G$1" pin="Y" />
                <wire x1="350.52" y1="185.42" x2="396.24" y2="185.42" width="0.1524" layer="91" />
                <label x="353.06" y="185.42" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R424" gate="G$1" pin="1" />
                <wire x1="330.2" y1="127" x2="276.86" y2="127" width="0.1524" layer="91" />
                <label x="276.86" y="127" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="VAON" class="0">
              <segment>
                <pinref part="R410" gate="G$1" pin="1" />
                <wire x1="195.58" y1="116.84" x2="142.24" y2="116.84" width="0.1524" layer="91" />
                <wire x1="142.24" y1="116.84" x2="142.24" y2="101.6" width="0.1524" layer="91" />
                <pinref part="R411" gate="G$1" pin="1" />
                <wire x1="195.58" y1="101.6" x2="142.24" y2="101.6" width="0.1524" layer="91" />
                <wire x1="142.24" y1="101.6" x2="142.24" y2="86.36" width="0.1524" layer="91" />
                <junction x="142.24" y="101.6" />
                <pinref part="R412" gate="G$1" pin="1" />
                <wire x1="195.58" y1="86.36" x2="142.24" y2="86.36" width="0.1524" layer="91" />
                <wire x1="142.24" y1="86.36" x2="142.24" y2="71.12" width="0.1524" layer="91" />
                <junction x="142.24" y="86.36" />
                <pinref part="R413" gate="G$1" pin="1" />
                <wire x1="195.58" y1="71.12" x2="142.24" y2="71.12" width="0.1524" layer="91" />
                <label x="142.24" y="116.84" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U408" gate="G$1" pin="VCC" />
                <wire x1="350.52" y1="180.34" x2="396.24" y2="180.34" width="0.1524" layer="91" />
                <label x="353.06" y="180.34" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C417" gate="G$1" pin="1" />
                <wire x1="330.2" y1="111.76" x2="276.86" y2="111.76" width="0.1524" layer="91" />
                <label x="276.86" y="111.76" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="VBAT" class="1">
              <segment>
                <pinref part="U407" gate="G$1" pin="IN" />
                <wire x1="325.12" y1="218.44" x2="276.86" y2="218.44" width="0.1524" layer="91" />
                <label x="276.86" y="218.44" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C415" gate="G$1" pin="1" />
                <wire x1="330.2" y1="96.52" x2="276.86" y2="96.52" width="0.1524" layer="91" />
                <label x="276.86" y="96.52" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="VBAT_ADC_SRC" class="0">
              <segment>
                <pinref part="U407" gate="G$1" pin="QOD" />
                <wire x1="350.52" y1="213.36" x2="396.24" y2="213.36" width="0.1524" layer="91" />
                <label x="353.06" y="213.36" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="U407" gate="G$1" pin="OUT" />
                <wire x1="350.52" y1="208.28" x2="396.24" y2="208.28" width="0.1524" layer="91" />
                <label x="353.06" y="208.28" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="R420" gate="G$1" pin="1" />
                <wire x1="330.2" y1="81.28" x2="276.86" y2="81.28" width="0.1524" layer="91" />
                <label x="276.86" y="81.28" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="VBAT_MEAS_EN" class="0">
              <segment>
                <pinref part="R422" gate="G$1" pin="1" />
                <wire x1="330.2" y1="66.04" x2="276.86" y2="66.04" width="0.1524" layer="91" />
                <label x="276.86" y="66.04" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="VBAT_SENSE" class="0">
              <segment>
                <pinref part="R420" gate="G$1" pin="2" />
                <wire x1="345.44" y1="81.28" x2="396.24" y2="81.28" width="0.1524" layer="91" />
                <label x="347.98" y="81.28" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C416" gate="G$1" pin="1" />
                <wire x1="330.2" y1="50.8" x2="276.86" y2="50.8" width="0.1524" layer="91" />
                <wire x1="276.86" y1="50.8" x2="276.86" y2="35.56" width="0.1524" layer="91" />
                <pinref part="R421" gate="G$1" pin="1" />
                <wire x1="330.2" y1="35.56" x2="276.86" y2="35.56" width="0.1524" layer="91" />
                <label x="276.86" y="50.8" size="1.55" layer="95" />
              </segment>
            </net>
            <net name="VMAIN" class="1">
              <segment>
                <pinref part="U406" gate="G$1" pin="VCC" />
                <wire x1="81.28" y1="203.2" x2="127" y2="203.2" width="0.1524" layer="91" />
                <label x="83.82" y="203.2" size="1.55" layer="95" />
              </segment>
              <segment>
                <pinref part="C411" gate="G$1" pin="1" />
                <wire x1="195.58" y1="55.88" x2="142.24" y2="55.88" width="0.1524" layer="91" />
                <label x="142.24" y="55.88" size="1.55" layer="95" />
              </segment>
            </net>
          </nets>
        </sheet>
      </sheets>
    </schematic>
  </drawing>
</eagle>
