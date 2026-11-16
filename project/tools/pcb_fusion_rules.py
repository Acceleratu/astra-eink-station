"""Load the portable Autodesk Fusion DRC profile into the paired native board."""
from xml.etree import ElementTree as ET

from pcb_model import BASE


def apply_profile(designrules):
    profile = ET.parse(BASE / "board/astra.edru")
    rules = profile.find("designrules/rules")
    if rules is None:
        raise ValueError("Fusion rule profile lacks categories and constraints")
    designrules.insert(1, rules)
