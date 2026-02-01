"""
Document parser for extracting text from uploaded files
"""
import io
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


async def parse_document(file_content: bytes, filename: str) -> str:
    """
    Parse document and extract text content
    
    Args:
        file_content: Raw file bytes
        filename: Original filename
        
    Returns:
        Extracted text content
    """
    suffix = Path(filename).suffix.lower()
    
    if suffix == ".txt":
        return _parse_txt(file_content)
    elif suffix == ".docx":
        return _parse_docx(file_content)
    else:
        # Try to decode as text
        return _parse_txt(file_content)


def _parse_txt(content: bytes) -> str:
    """Parse plain text file"""
    # Try different encodings
    for encoding in ["utf-8", "cp1251", "latin-1"]:
        try:
            return content.decode(encoding)
        except UnicodeDecodeError:
            continue
    
    # Fallback with error handling
    return content.decode("utf-8", errors="replace")


def _parse_docx(content: bytes) -> str:
    """Parse DOCX file"""
    try:
        from docx import Document
        
        doc = Document(io.BytesIO(content))
        
        paragraphs = []
        for para in doc.paragraphs:
            if para.text.strip():
                paragraphs.append(para.text)
        
        return "\n\n".join(paragraphs)
        
    except Exception as e:
        logger.error(f"Failed to parse DOCX: {e}")
        raise ValueError(f"Не удалось прочитать DOCX файл: {e}")
