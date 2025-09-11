#!/usr/bin/env python3
"""
Test script to verify all packages are working correctly
"""

def test_imports():
    try:
        import fitz
        print("✅ PyMuPDF (fitz) imported successfully")
    except ImportError as e:
        print(f"❌ PyMuPDF import failed: {e}")
        return False
    
    try:
        from PIL import Image
        print("✅ Pillow (PIL) imported successfully")
    except ImportError as e:
        print(f"❌ Pillow import failed: {e}")
        return False
    
    try:
        import pytesseract
        print("✅ pytesseract imported successfully")
    except ImportError as e:
        print(f"❌ pytesseract import failed: {e}")
        return False
    
    try:
        from gtts import gTTS
        print("✅ gTTS imported successfully")
    except ImportError as e:
        print(f"❌ gTTS import failed: {e}")
        return False
    
    try:
        from pydub import AudioSegment
        print("✅ pydub imported successfully")
    except ImportError as e:
        print(f"❌ pydub import failed: {e}")
        return False
    
    try:
        import pyttsx3
        print("✅ pyttsx3 imported successfully")
    except ImportError as e:
        print(f"❌ pyttsx3 import failed: {e}")
        return False
    
    return True

def test_pdf_processing():
    try:
        import fitz
        from pathlib import Path
        
        pdf_path = "White-ChatGPTPromptPatternsForSWE.pdf"
        if Path(pdf_path).exists():
            doc = fitz.open(pdf_path)
            page_count = len(doc)
            print(f"✅ PDF opened successfully: {page_count} pages")
            doc.close()
            return True
        else:
            print(f"❌ PDF file not found: {pdf_path}")
            return False
    except Exception as e:
        print(f"❌ PDF processing test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing TTS environment...")
    print("=" * 40)
    
    imports_ok = test_imports()
    print()
    
    pdf_ok = test_pdf_processing()
    print()
    
    if imports_ok and pdf_ok:
        print("🎉 All tests passed! Environment is ready.")
    else:
        print("❌ Some tests failed. Check the errors above.")
