# service/gemini_service.py

import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def analyze_pet_health(user_message):
    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"""
Kamu adalah PetVetAI, asisten kesehatan hewan peliharaan profesional.

Gunakan struktur berikut:

1. **Diagnosis Kemungkinan**
2. **Tingkat Urgensi (low / medium / emergency)**
3. **Gejala yang Harus Diperhatikan**
4. **Yang Bisa Dilakukan di Rumah**
5. **Kapan Harus ke Dokter Hewan**
6. **Pertanyaan Tambahan**

User bertanya: "{user_message}"
"""

    response = model.generate_content(prompt)
    return response.text
