import os
import google.generativeai as genai

print("--- API Key Test Script ---")

try:
    # 1. Check if the environment variable exists
    api_key = os.environ["GOOGLE_API_KEY"]
    print("✅ Step 1: GOOGLE_API_KEY found in environment.")

    # 2. Configure the library with the key
    genai.configure(api_key=api_key)
    print("✅ Step 2: Google AI library configured.")

    # 3. Attempt to connect and generate content
    print("\n⏳ Step 3: Attempting to call the Gemini API...")
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    response = model.generate_content("test")
    
    print("✅ SUCCESS! The API key is working correctly.")
    print(f"API Response: {response.text}")

except KeyError:
    print("❌ FAILURE: The GOOGLE_API_KEY environment variable was not found inside the container.")
except Exception as e:
    print(f"❌ FAILURE: An error occurred. The API key might be invalid.")
    print(f"   Error details: {e}")