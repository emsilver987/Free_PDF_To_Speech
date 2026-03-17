"""TTS engine abstraction supporting multiple providers"""

from gtts import gTTS
import pyttsx3
from pathlib import Path
import logging
import uuid

logger = logging.getLogger(__name__)


class TTSEngine:
    """Unified interface for multiple TTS engines"""
    
    def __init__(self):
        self.engines = {
            "gtts": self._gtts,
            "system": self._pyttsx3,
            # "elevenlabs": self._elevenlabs,  # TODO: requires API key
            # "coqui": self._coqui_tts,  # TODO: requires model download
        }
    
    def get_voices(self, engine="gtts"):
        """Get available voices for an engine"""
        if engine == "gtts":
            return [
                {"id": "en", "name": "English (Google TTS)", "lang": "en"},
                {"id": "es", "name": "Spanish", "lang": "es"},
                {"id": "fr", "name": "French", "lang": "fr"},
                {"id": "de", "name": "German", "lang": "de"},
                {"id": "it", "name": "Italian", "lang": "it"},
                {"id": "pt", "name": "Portuguese", "lang": "pt"},
                {"id": "ja", "name": "Japanese", "lang": "ja"},
            ]
        
        elif engine == "system":
            try:
                engine_obj = pyttsx3.init()
                voices = engine_obj.getProperty("voices")
                return [
                    {"id": v.id, "name": v.name, "gender": getattr(v, "gender", "unknown")}
                    for v in voices
                ]
            except Exception as e:
                logger.error(f"Failed to get system voices: {str(e)}")
                return []
        
        return []
    
    def synthesize(self, text, engine="gtts", voice=None, output_dir=None):
        """
        Synthesize text to speech
        
        Args:
            text: Text to convert
            engine: TTS engine (gtts, system, elevenlabs, coqui)
            voice: Voice ID or language code
            output_dir: Directory to save output
            
        Returns:
            Path to generated audio file
        """
        if output_dir is None:
            output_dir = Path("outputs")
        
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        if engine not in self.engines:
            raise ValueError(f"Unknown engine: {engine}")
        
        return self.engines[engine](text, voice, output_dir)
    
    def _gtts(self, text, voice=None, output_dir=None):
        """Google TTS synthesis"""
        lang = voice or "en"
        output_file = Path(output_dir) / f"speech_{uuid.uuid4()}.mp3"
        
        try:
            tts = gTTS(text, lang=lang)
            tts.save(str(output_file))
            logger.info(f"Generated speech: {output_file}")
            return str(output_file)
        except Exception as e:
            logger.error(f"gTTS failed: {str(e)}")
            raise
    
    def _pyttsx3(self, text, voice=None, output_dir=None):
        """System TTS (Windows/macOS/Linux)"""
        output_file = Path(output_dir) / f"speech_{uuid.uuid4()}.wav"
        
        try:
            engine = pyttsx3.init()
            
            # Set voice if specified
            if voice:
                engine.setProperty("voice", voice)
            
            # Configure speech rate
            engine.setProperty("rate", 150)  # Words per minute
            engine.setProperty("volume", 0.9)
            
            # Save to file
            engine.save_to_file(text, str(output_file))
            engine.runAndWait()
            
            logger.info(f"Generated speech: {output_file}")
            return str(output_file)
        except Exception as e:
            logger.error(f"pyttsx3 failed: {str(e)}")
            raise
    
    def _elevenlabs(self, text, voice=None, output_dir=None):
        """
        ElevenLabs TTS (high quality, requires API key)
        TODO: Requires ELEVENLABS_API_KEY environment variable
        """
        raise NotImplementedError("ElevenLabs support coming soon. Requires API key setup.")
    
    def _coqui_tts(self, text, voice=None, output_dir=None):
        """
        Coqui TTS (open-source, offline)
        TODO: Requires model download and GPU (optional but recommended)
        """
        raise NotImplementedError("Coqui TTS support coming soon. Requires model setup.")
