from src.snapshot import capture

def test_capture_example():
    snap = capture("https://example.com")
    assert "hash" in snap and len(snap["hash"]) == 64
