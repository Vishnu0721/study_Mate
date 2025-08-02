#!/usr/bin/env python3
"""
Debug file extraction directly
"""

import os
import PyPDF2
from docx import Document

def debug_file_extraction():
    """Debug file extraction directly"""
    
    print("🔍 Debugging File Extraction Directly")
    print("=" * 50)
    
    # Check upload folder
    upload_folder = "uploads"
    if os.path.exists(upload_folder):
        files = os.listdir(upload_folder)
        print(f"📁 Files in upload folder: {files}")
        
        for filename in files:
            if filename.endswith('.pdf'):
                file_path = os.path.join(upload_folder, filename)
                print(f"\n📄 Testing PDF extraction: {filename}")
                
                try:
                    with open(file_path, 'rb') as file:
                        pdf_reader = PyPDF2.PdfReader(file)
                        print(f"📊 PDF pages: {len(pdf_reader.pages)}")
                        
                        text = ""
                        for i, page in enumerate(pdf_reader.pages[:5]):
                            page_text = page.extract_text()
                            print(f"📄 Page {i+1} length: {len(page_text)} characters")
                            text += page_text + "\n"
                            if len(text) > 4000:
                                break
                        
                        print(f"📝 Total extracted text length: {len(text)} characters")
                        print(f"📝 Text preview:")
                        print("-" * 40)
                        print(text[:500] + "..." if len(text) > 500 else text)
                        print("-" * 40)
                        
                        # Analyze sentences
                        import re
                        sentences = re.split(r'[.!?]+', text)
                        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
                        
                        print(f"\n📊 Sentence Analysis:")
                        print(f"Total sentences: {len(sentences)}")
                        
                        for i, sentence in enumerate(sentences[:10], 1):
                            print(f"{i}. [{len(sentence)} chars] {sentence[:80]}{'...' if len(sentence) > 80 else ''}")
                        
                except Exception as e:
                    print(f"❌ Error extracting PDF: {e}")
                    
            elif filename.endswith('.docx'):
                file_path = os.path.join(upload_folder, filename)
                print(f"\n📄 Testing DOCX extraction: {filename}")
                
                try:
                    doc = Document(file_path)
                    text = ""
                    for i, paragraph in enumerate(doc.paragraphs[:25]):
                        text += paragraph.text + "\n"
                        if len(text) > 4000:
                            break
                    
                    print(f"📝 Total extracted text length: {len(text)} characters")
                    print(f"📝 Text preview:")
                    print("-" * 40)
                    print(text[:500] + "..." if len(text) > 500 else text)
                    print("-" * 40)
                    
                except Exception as e:
                    print(f"❌ Error extracting DOCX: {e}")
    else:
        print("❌ Upload folder not found")

if __name__ == "__main__":
    debug_file_extraction() 