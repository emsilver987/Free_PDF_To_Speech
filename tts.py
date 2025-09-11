import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from gtts import gTTS
from pydub import AudioSegment
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

# Base filename: same as PDF, but with .mp3
output_mp3 = str(Path(pdf_path).with_suffix(".mp3"))

# Generate TTS and save temporary file
tts = gTTS(full_text, lang="en")
temp_file = "temp.mp3"
tts.save(temp_file)

# Speed it up 1.5x
sound = AudioSegment.from_mp3(temp_file)
faster = sound._spawn(
    sound.raw_data,
    overrides={"frame_rate": int(sound.frame_rate * 1.5)}
).set_frame_rate(sound.frame_rate)

# Export final MP3 (overwrite if exists)
faster.export(output_mp3, format="mp3")

# Clean up temp file
Path(temp_file).unlink(missing_ok=True)

print(f"✅ Saved as {output_mp3}")
