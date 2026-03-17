"""PDF text extraction with OCR fallback"""

import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class PDFProcessor:
    """Extract text from PDFs with automatic OCR fallback"""
    
    def __init__(self, ocr_scale=1.7):
        self.ocr_scale = ocr_scale
    
    def extract_text(self, pdf_path):
        """
        Extract all text from PDF
        Falls back to OCR for image-based pages
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Full text content as string
        """
        doc = fitz.open(pdf_path)
        all_text = []
        
        try:
            for page_num, page in enumerate(doc, 1):
                text = page.get_text("text")
                
                # Fallback to OCR if no text extracted
                if not text.strip():
                    logger.info(f"Page {page_num}: Using OCR (no text found)")
                    text = self._ocr_page(page)
                
                all_text.append(text)
        finally:
            doc.close()
        
        return "\n".join(all_text)
    
    def extract_by_pages(self, pdf_path):
        """
        Extract text page-by-page for granular control
        
        Returns:
            List of dicts with page number and text
        """
        doc = fitz.open(pdf_path)
        pages = []
        
        try:
            for page_num, page in enumerate(doc, 1):
                text = page.get_text("text")
                
                if not text.strip():
                    text = self._ocr_page(page)
                
                pages.append({
                    "page": page_num,
                    "text": text
                })
        finally:
            doc.close()
        
        return pages
    
    def _ocr_page(self, page):
        """OCR a single page"""
        try:
            pix = page.get_pixmap(matrix=fitz.Matrix(self.ocr_scale, self.ocr_scale), alpha=False)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text = pytesseract.image_to_string(img, lang="eng", config="--psm 6")
            return text
        except Exception as e:
            logger.error(f"OCR failed: {str(e)}")
            return ""
    
    def get_metadata(self, pdf_path):
        """Extract PDF metadata"""
        doc = fitz.open(pdf_path)
        metadata = doc.metadata
        doc.close()
        
        return {
            "title": metadata.get("title", ""),
            "author": metadata.get("author", ""),
            "subject": metadata.get("subject", ""),
            "pages": len(doc)
        }
