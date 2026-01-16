# --- 1. INSTALL LIBRARY YANG DIBUTUHKAN ---
# Jalankan ini di sel pertama Google Colab jika menggunakan Notebook
# !pip install fastapi uvicorn pyngrok nest-asyncio transformers torch -q

from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
import uvicorn
from pyngrok import ngrok
import nest_asyncio
import os
import asyncio

# --- 2. LOAD MODEL DARI HUGGING FACE ---
# Menggunakan repositori publik agar orang lain bisa menjalankan tanpa akses Drive
model_path = "Faol/indobert-sentiment-final-boss"

print(f"✅ Sedang memuat model dari: {model_path}")
try:
    # Memuat pipeline sentiment analysis
    nlp = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path)
    print("🚀 Model siap melayani permintaan API.")
except Exception as e:
    print(f"❌ Gagal memuat model: {e}")

# --- 3. KONFIGURASI FASTAPI ---
app = FastAPI(
    title="IndoBERT Sentiment API",
    description="API untuk klasifikasi sentimen berita menggunakan model IndoBERT"
)
nest_asyncio.apply()

class NewsInput(BaseModel):
    text: str
    judul: str

@app.post("/predict")
async def predict_sentiment(item: NewsInput):
    """
    Endpoint untuk prediksi sentimen.
    Input: JSON dengan field 'text' dan 'judul'
    """
    # Melakukan prediksi
    res = nlp(item.text)[0]

    # Mapping label berdasarkan konfigurasi model IndoBERT
    label_map = {'LABEL_0': 'Negatif', 'LABEL_1': 'Netral', 'LABEL_2': 'Positif'}
    label_final = label_map.get(res['label'], res['label'])
    confidence = float(res['score'])

    # Logika kepercayaan (is_reliable) untuk alur n8n
    is_reliable = confidence > 0.6

    return {
        "judul": item.judul,
        "sentiment": label_final,
        "confidence": confidence,
        "is_reliable": is_reliable,
        "status": "success"
    }

# --- 4. KONEKSI NGROK ---
# Dapatkan token gratis di: https://dashboard.ngrok.com/get-started/your-authtoken
# Untuk keamanan di GitHub, biarkan kosong atau gunakan environment variable
NGROK_TOKEN = "MASUKKAN_TOKEN_NGROK_ANDA_DISINI" 

if NGROK_TOKEN == "MASUKKAN_TOKEN_NGROK_ANDA_DISINI":
    print("⚠️  Peringatan: Token Ngrok belum diisi. API tidak akan bisa diakses publik.")
else:
    ngrok.set_auth_token(NGROK_TOKEN)
    # Membuat Tunnel ke Internet (Port 8000)
    public_url = ngrok.connect(8000)
    print(f"\n" + "="*50)
    print(f"🌍 API ANDA SUDAH ONLINE!")
    print(f"🔗 URL UNTUK n8n: {public_url}/predict")
    print(f"Metode: POST")
    print("="*50 + "\n")

# --- 5. RUN SERVER ---
if __name__ == "__main__":
    # Konfigurasi uvicorn untuk dijalankan di lingkungan Colab
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    
    # Menggunakan loop yang sudah ada (khusus Colab/Jupyter)
    loop = asyncio.get_event_loop()
    loop.create_task(server.serve())