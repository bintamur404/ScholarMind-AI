import pytesseract
from PIL import Image
from langchain_core.tools import tool

@tool
def ocr_tool(image_path: str) -> str:
    """
    Extracts text from an image for research analysis.
    Args:
        image_path: Absolute path to the image file.
    """
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        return text if text.strip() else "No text detected in image."
    except Exception as e:
        return f"OCR Error: {e}"
