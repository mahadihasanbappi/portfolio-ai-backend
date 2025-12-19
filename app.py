import google.generativeai as genai

# Apnar API Key ti ekhane bosan
genai.configure(api_key="AIzaSyCVE4wxLGyCvs9kIKoRRV7aRBZ4lK8Kkxc")

def generate_content(user_prompt):
    try:
        # Paid model er bodole 'gemini-1.5-flash' use kora hocche (Free Tier er jonno sera)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        response = model.generate_content(user_prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# Test korar jonno:
print(generate_content("Hello, how are you?"))
