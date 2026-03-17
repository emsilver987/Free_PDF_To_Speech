"""Audio processing and optimization"""

from pydub import AudioSegment
from pathlib import Path
import logging
import shutil

logger = logging.getLogger(__name__)

# Check if ffmpeg is available
FFMPEG_AVAILABLE = shutil.which('ffmpeg') is not None and shutil.which('ffprobe') is not None


class AudioProcessor:
    """Post-process and optimize audio files"""
    
    def process_audio(self, audio_path, speed=1.0, normalize=True, format="mp3"):
        """
        Post-process audio with speed adjustment and normalization
        Falls back to simple conversion if ffmpeg unavailable
        
        Args:
            audio_path: Path to source audio
            speed: Playback speed multiplier (0.5-2.0)
            normalize: Whether to normalize volume
            format: Output format (mp3, wav, m4b, etc)
            
        Returns:
            Path to processed audio file
        """
        audio_path = Path(audio_path)
        
        # Detect format from file extension
        file_format = audio_path.suffix.lstrip(".").lower()
        
        try:
            # Load audio
            sound = AudioSegment.from_file(str(audio_path), format=file_format)
            
            # Apply speed adjustment (only if ffmpeg available)
            if speed != 1.0 and FFMPEG_AVAILABLE:
                sound = self._adjust_speed(sound, speed)
            elif speed != 1.0 and not FFMPEG_AVAILABLE:
                logger.warning(f"Speed adjustment skipped (ffmpeg not installed). Audio will play at normal speed.")
            
            # Normalize volume
            if normalize:
                sound = self._normalize_volume(sound)
            
            # Export
            output_path = audio_path.parent / f"{audio_path.stem}_processed.{format}"
            sound.export(str(output_path), format=format)
            
            logger.info(f"Processed audio saved: {output_path}")
            
            # Cleanup source if temporary
            if audio_path != output_path and "temp" in str(audio_path):
                audio_path.unlink(missing_ok=True)
            
            return str(output_path)
        
        except Exception as e:
            logger.error(f"Audio processing failed: {str(e)}")
            # If processing fails, try to just convert to target format without modifications
            try:
                logger.info("Falling back to simple format conversion...")
                sound = AudioSegment.from_file(str(audio_path), format=file_format)
                output_path = audio_path.parent / f"{audio_path.stem}_processed.{format}"
                sound.export(str(output_path), format=format)
                logger.info(f"Fallback conversion saved: {output_path}")
                return str(output_path)
            except Exception as e2:
                logger.error(f"Fallback conversion also failed: {str(e2)}")
                raise
    
    def _adjust_speed(self, sound, speed_factor):
        """Adjust playback speed by changing frame rate"""
        if speed_factor == 1.0:
            return sound
        
        if not FFMPEG_AVAILABLE:
            logger.warning("ffmpeg not available, speed adjustment skipped")
            return sound
        
        # Increase playback speed by reducing frame rate
        new_frame_rate = int(sound.frame_rate * speed_factor)
        
        try:
            # Speed up by resampling
            sound_with_increased_frame_rate = sound._spawn(
                sound.raw_data,
                overrides={"frame_rate": new_frame_rate}
            )
            # Reset to original frame rate (creates speed effect)
            return sound_with_increased_frame_rate.set_frame_rate(sound.frame_rate)
        except Exception as e:
            logger.warning(f"Speed adjustment failed, returning original: {str(e)}")
            return sound
    
    def _normalize_volume(self, sound, target_db=-20.0):
        """Normalize audio to target loudness"""
        try:
            current_db = sound.dBFS
            gain = target_db - current_db
            
            if gain != 0:
                return sound.apply_gain(gain)
            return sound
        except Exception as e:
            logger.warning(f"Normalization failed: {str(e)}")
            return sound
    
    def split_by_chapters(self, audio_path, chapter_markers):
        """
        Split audio into chapters
        
        Args:
            audio_path: Path to full audio
            chapter_markers: List of (name, time_ms) tuples
            
        Returns:
            List of chapter file paths
        """
        audio_path = Path(audio_path)
        file_format = audio_path.suffix.lstrip(".").lower()
        sound = AudioSegment.from_file(str(audio_path), format=file_format)
        
        chapters = []
        output_dir = audio_path.parent / "chapters"
        output_dir.mkdir(exist_ok=True)
        
        for i, (name, start_ms) in enumerate(chapter_markers):
            # Get end time from next marker or end of audio
            end_ms = chapter_markers[i + 1][1] if i + 1 < len(chapter_markers) else len(sound)
            
            # Extract chapter
            chapter = sound[start_ms:end_ms]
            chapter_path = output_dir / f"{i:02d}_{name}.mp3"
            chapter.export(str(chapter_path), format="mp3")
            
            chapters.append(str(chapter_path))
        
        return chapters
    
    def get_audio_info(self, audio_path):
        """Get audio file metadata"""
        audio_path = Path(audio_path)
        file_format = audio_path.suffix.lstrip(".").lower()
        sound = AudioSegment.from_file(str(audio_path), format=file_format)
        
        return {
            "filename": audio_path.name,
            "format": file_format,
            "duration_seconds": len(sound) / 1000.0,
            "channels": sound.channels,
            "sample_rate": sound.frame_rate,
            "file_size_mb": audio_path.stat().st_size / (1024 * 1024)
        }
