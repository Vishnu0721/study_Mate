import os
import fitz  # PyMuPDF
import tempfile
import cv2
import numpy as np
from PIL import Image
import easyocr
import pytesseract

def debug_ocr_issue():
    """Debug why OCR is failing for the chemistry PDF"""
    
    print("=== Debugging OCR Issue for Chemistry PDF ===")
    
    # Find the chemistry PDF file
    uploads_dir = 'uploads'
    chemistry_file = None
    
    for filename in os.listdir(uploads_dir):
        if 'chemistry' in filename.lower() and filename.endswith('.pdf'):
            chemistry_file = os.path.join(uploads_dir, filename)
            break
    
    if not chemistry_file:
        print("❌ Chemistry PDF not found in uploads directory")
        return
    
    print(f"✅ Found chemistry PDF: {chemistry_file}")
    
    try:
        # Open PDF and check pages
        pdf_document = fitz.open(chemistry_file)
        print(f"📄 PDF has {len(pdf_document)} pages")
        
        # Test each page
        for page_num in range(min(3, len(pdf_document))):
            print(f"\n🔍 Testing Page {page_num + 1}:")
            
            page = pdf_document[page_num]
            
            # Convert page to image with high resolution
            mat = fitz.Matrix(2.0, 2.0)  # 2x zoom for better quality
            pix = page.get_pixmap(matrix=mat)
            
            # Save temporary image
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                pix.save(temp_file.name)
                temp_image_path = temp_file.name
            
            print(f"  📸 Saved image: {temp_image_path}")
            
            # Test OCR on the image
            test_ocr_on_image(temp_image_path, page_num + 1)
            
            # Clean up
            os.unlink(temp_image_path)
        
        pdf_document.close()
        
    except Exception as e:
        print(f"❌ Error processing PDF: {e}")

def test_ocr_on_image(image_path, page_num):
    """Test OCR on a specific image"""
    
    print(f"  🔍 Testing OCR on page {page_num} image...")
    
    try:
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            print(f"    ❌ Could not read image")
            return
        
        print(f"    📐 Image size: {image.shape}")
        
        # Test EasyOCR
        print(f"    🔍 Testing EasyOCR...")
        try:
            # Convert to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Initialize EasyOCR
            reader = easyocr.Reader(['en'], gpu=False)
            
            # Extract text using EasyOCR with optimized settings
            results = reader.readtext(
                image_rgb,
                paragraph=True,
                detail=1,
                contrast_ths=0.1,
                adjust_contrast=0.5,
                text_threshold=0.6,
                link_threshold=0.4,
                low_text=0.3,
                canvas_size=2560,
                mag_ratio=1.5
            )
            
            # Combine all detected text
            text = ""
            for (bbox, detected_text, confidence) in results:
                if confidence > 0.2:
                    text += detected_text + " "
            
            print(f"    ✅ EasyOCR extracted {len(text.strip())} characters")
            if len(text.strip()) > 0:
                print(f"    📝 Sample text: {text[:100]}...")
            else:
                print(f"    ❌ No text detected by EasyOCR")
                
        except Exception as e:
            print(f"    ❌ EasyOCR error: {e}")
        
        # Test Tesseract
        print(f"    🔍 Testing Tesseract...")
        try:
            # Preprocess image
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply advanced preprocessing
            denoised = cv2.fastNlMeansDenoising(gray)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            enhanced = clahe.apply(denoised)
            _, thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Extract text using Tesseract
            custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,!?()[]{}:;"\'-_+=/\\|@#$%^&*~` '
            tesseract_text = pytesseract.image_to_string(thresh, config=custom_config)
            
            print(f"    ✅ Tesseract extracted {len(tesseract_text.strip())} characters")
            if len(tesseract_text.strip()) > 0:
                print(f"    📝 Sample text: {tesseract_text[:100]}...")
            else:
                print(f"    ❌ No text detected by Tesseract")
                
        except Exception as e:
            print(f"    ❌ Tesseract error: {e}")
        
        # Test basic Tesseract without preprocessing
        print(f"    🔍 Testing basic Tesseract...")
        try:
            basic_text = pytesseract.image_to_string(image)
            print(f"    ✅ Basic Tesseract extracted {len(basic_text.strip())} characters")
            if len(basic_text.strip()) > 0:
                print(f"    📝 Sample text: {basic_text[:100]}...")
            else:
                print(f"    ❌ No text detected by basic Tesseract")
                
        except Exception as e:
            print(f"    ❌ Basic Tesseract error: {e}")
            
    except Exception as e:
        print(f"    ❌ Error processing image: {e}")

if __name__ == "__main__":
    debug_ocr_issue() 