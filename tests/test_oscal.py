"""Test phased OSCAL Assessment Results export."""
from src.ccm.nodes import run_pipeline
from src.ccm.oscal import to_oscal_assessment_results


def test_oscal_structure():
    state = run_pipeline()
    ar = to_oscal_assessment_results(state)
    assert "assessment-results" in ar
    root = ar["assessment-results"]
    assert "uuid" in root
    assert "metadata" in root
    assert root["metadata"]["oscal-version"] == "1.1.2"
    assert "results" in root
    assert len(root["results"]) >= 1
    result = root["results"][0]
    assert "observations" in result
    assert "findings" in result
    # journey and chain appear in props
    props = {p["name"]: p["value"] for p in root["metadata"].get("props", [])}
    assert "journey-status" in props
    assert "evidence-chain-root" in props
