"""
Unit tests for MixaClip aspect ratio preservation rules.
"""

from mixaclip.utils.aspect_ratio import get_proportional_filter

def test_proportional_filter_preserves_aspect_ratio():
    filter_str = get_proportional_filter(720, 1280)
    assert "force_original_aspect_ratio=increase" in filter_str, "Must force proportional scaling"
    assert "crop=720:1280" in filter_str, "Must center crop excess without squishing"
    assert "setsar=1" in filter_str, "Must ensure 1:1 square pixel aspect ratio"
    print("[PASS] test_proportional_filter_preserves_aspect_ratio passed!")

if __name__ == "__main__":
    test_proportional_filter_preserves_aspect_ratio()
