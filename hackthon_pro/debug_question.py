import requests
import json
import google.generativeai as genai

# Test the API directly
def test_api_directly():
    print("=== Testing API Directly ===")
    GOOGLE_AI_API_KEY = "AIzaSyCe8IvHrLiaYe9x0qBLz7znWqp8wg7Kzl8"
    genai.configure(api_key=GOOGLE_AI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    try:
        test_text = "This is a test document about ethical hacking. It contains information about cybersecurity."
        test_question = "What is this document about?"
        
        prompt = f"""
        Based on the following document content, please answer this question: "{test_question}"
        
        Document content:
        {test_text}
        
        Please provide a clear, accurate, and concise answer based only on the information in the document.
        
        Answer:"""
        
        response = model.generate_content(prompt)
        print(f"✅ Direct API test successful: {response.text}")
        return True
    except Exception as e:
        print(f"❌ Direct API test failed: {e}")
        return False

# Test the application
def test_application():
    print("\n=== Testing Application ===")
    try:
        # Get documents
        response = requests.get('http://127.0.0.1:5000/documents')
        documents = response.json()
        print(f"Available documents: {len(documents)}")
        
        if documents:
            doc = documents[0]
            doc_id = doc['id']
            filename = doc['filename']
            content = doc.get('content', '')
            print(f"Document: {filename} (ID: {doc_id})")
            print(f"Content length: {len(content)} characters")
            print(f"Content preview: {content[:200]}...")
            
            # Test question
            question_data = {
                'document_id': doc_id,
                'question': 'What is this document about?'
            }
            
            response = requests.post(
                'http://127.0.0.1:5000/ask',
                json=question_data,
                headers={'Content-Type': 'application/json'}
            )
            
            print(f"Response status: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"Question: {result['question']}")
                print(f"Answer: {result['answer']}")
            else:
                print(f"Error response: {response.text}")
        else:
            print("No documents found")
            
    except Exception as e:
        print(f"Application test failed: {e}")

if __name__ == "__main__":
    # Test API directly first
    api_works = test_api_directly()
    
    if api_works:
        # Then test application
        test_application()
    else:
        print("API is not working, skipping application test") 