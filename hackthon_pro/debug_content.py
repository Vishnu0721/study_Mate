#!/usr/bin/env python3
"""
Debug script to examine document content extraction
"""

import requests
import json

def debug_document_content():
    """Debug the document content extraction"""
    
    base_url = "http://localhost:5000"
    
    print("🔍 Debugging Document Content Extraction")
    print("=" * 50)
    
    # Get documents
    try:
        response = requests.get(f"{base_url}/documents", timeout=5)
        if response.status_code == 200:
            documents = response.json()
            if documents:
                document = documents[0]
                document_id = document['id']
                filename = document['filename']
                content = document.get('content', '')
                
                print(f"📄 Document: {filename}")
                print(f"📏 Content length: {len(content)} characters")
                print(f"📝 Content preview:")
                print("-" * 40)
                print(content[:500] + "..." if len(content) > 500 else content)
                print("-" * 40)
                
                # Analyze sentences
                import re
                sentences = re.split(r'[.!?]+', content)
                sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
                
                print(f"\n📊 Sentence Analysis:")
                print(f"Total sentences: {len(sentences)}")
                
                for i, sentence in enumerate(sentences[:10], 1):
                    print(f"{i}. [{len(sentence)} chars] {sentence[:80]}{'...' if len(sentence) > 80 else ''}")
                
                # Test question answering with debug info
                print(f"\n🧪 Testing Question Answering:")
                test_question = "What is the main topic?"
                
                response = requests.post(
                    f"{base_url}/ask",
                    json={
                        "document_id": document_id,
                        "question": test_question
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    answer = result.get('answer', 'No answer')
                    print(f"Question: {test_question}")
                    print(f"Answer: {answer}")
                else:
                    print(f"Error: {response.status_code}")
                    
            else:
                print("No documents found")
        else:
            print("Failed to get documents")
            
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_document_content() 