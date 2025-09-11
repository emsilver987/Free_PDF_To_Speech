import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import pyttsx3
from pathlib import Path

pdf_path = "White-ChatGPTPromptPatternsForSWE.pdf"
doc = fitz.open(pdf_path)

all_text = []

for page_num, page in enumerate(doc, 1):
    text = page.get_text("text")
    if not text.strip():  # Fallback to OCR
        print(f"Page {page_num}: OCR in progress...")
        pix = page.get_pixmap(matrix=fitz.Matrix(1.7, 1.7), alpha=False)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        text = pytesseract.image_to_string(img, lang="eng", config="--psm 6")
    all_text.append(text)

full_text = "\n".join(all_text)

# Initialize offline TTS engine
engine = pyttsx3.init()

# Set properties (optional)
engine.setProperty('rate', 200)  # Speed of speech
engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)

# Get available voices
voices = engine.getProperty('voices')
if voices:
    # Use the first available voice
    engine.setProperty('voice', voices[0].id)

print("Starting text-to-speech conversion...")
print(f"Text length: {len(full_text)} characters")

# Speak the text
engine.say(full_text)
engine.runAndWait()

print("✅ Text-to-speech conversion completed!")
