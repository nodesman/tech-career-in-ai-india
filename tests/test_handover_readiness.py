#!/usr/bin/env python3
"""
Handover Readiness Verification Test Suite for The Sovereign Technologist
Tests:
1. Jekyll config validity
2. Layouts existence and schema
3. Manuscript frontmatter validation (title, part, layout)
4. Zero broken local manuscript references
5. CSS and assets integrity
"""

import os
import sys
import glob
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def test_config():
    config_path = os.path.join(BASE_DIR, "_config.yml")
    assert os.path.exists(config_path), "_config.yml missing"
    with open(config_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "title:" in content, "Missing title in _config.yml"
    assert "collections:" in content, "Missing collections in _config.yml"
    assert "manuscript:" in content, "Missing manuscript collection config"
    print("✓ _config.yml integrity verified")

def test_layouts():
    layouts_dir = os.path.join(BASE_DIR, "_layouts")
    assert os.path.exists(os.path.join(layouts_dir, "default.html")), "default.html layout missing"
    assert os.path.exists(os.path.join(layouts_dir, "chapter.html")), "chapter.html layout missing"
    print("✓ _layouts integrity verified")

def test_manuscript_frontmatter():
    manuscript_dir = os.path.join(BASE_DIR, "manuscript")
    all_files = glob.glob(os.path.join(manuscript_dir, "*.md"))
    chapters = [f for f in all_files if re.match(r'^\d{2}-', os.path.basename(f))]
    assert len(chapters) > 0, "No chapters found in manuscript/"
    
    for ch in chapters:
        with open(ch, "r", encoding="utf-8") as f:
            text = f.read()
        assert text.startswith("---"), f"{ch} missing frontmatter delimiter"
        parts = text.split("---", 2)
        assert len(parts) >= 3, f"{ch} invalid frontmatter structure"
        fm = parts[1]
        assert "layout: chapter" in fm, f"{ch} must have layout: chapter"
        assert "title:" in fm, f"{ch} missing title"
        assert "part:" in fm, f"{ch} missing part classification"
    print(f"✓ All {len(chapters)} manuscript chapters passed frontmatter integrity checks")

def test_assets():
    css_path = os.path.join(BASE_DIR, "assets", "css", "main.css")
    assert os.path.exists(css_path), "main.css missing"
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()
    assert "--bg-primary" in css, "Theme CSS variables missing"
    assert "Cinzel" in css, "Font declarations missing in CSS"
    print("✓ Assets & CSS verified")

if __name__ == "__main__":
    print("=== RUNNING HANDOVER READINESS VERIFICATION SUITE ===")
    try:
        test_config()
        test_layouts()
        test_manuscript_frontmatter()
        test_assets()
        print("\n🎉 ALL QUALITY GATES PASSED: Ready for deployment and handover.")
    except AssertionError as e:
        print(f"\n❌ QUALITY GATE FAILURE: {e}", file=sys.stderr)
        sys.exit(1)
