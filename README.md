📰 Hybrid News Sentiment Analysis & Emergency Monitoring System
Integration of n8n Workflow Automation and IndoBERT–LLaMA Model for Summarization, Sentiment Analysis, and Determination of Online News Urgency Levels

Sistem pemantauan berita otomatis yang menggabungkan kekuatan IndoBERT untuk klasifikasi sentimen cepat dan Llama 3 (Ollama) untuk analisis entitas serta ringkasan mendalam. Sistem ini diorkestrasi menggunakan n8n untuk mengotomatisasi seluruh alur kerja dari pengambilan berita hingga pelaporan.

🚀 Fitur Utama
Real-time Monitoring: Penarikan berita otomatis dari RSS Feed Detik News dan Antara News secara terjadwal.

Hybrid AI Processing:

IndoBERT (Cloud Path): Klasifikasi sentimen (Positif, Netral, Negatif) menggunakan model yang di-host di Hugging Face.

Llama 3 (Fallback Path): Digunakan saat skor kepercayaan model IndoBERT rendah untuk ekstraksi tokoh, lokasi, dan ringkasan mendalam.

Urgensi Booster: Algoritma berbasis JavaScript untuk mendeteksi kata kunci krisis guna menghitung skor urgensi berita secara dinamis.

Automated Reporting: Sinkronisasi database ke Google Sheets dan notifikasi email otomatis untuk berita dengan tingkat urgensi tinggi.

🛠️ Arsitektur Sistem
Sistem ini menggunakan arsitektur Hybrid Deployment:

Backend API (Cloud): IndoBERT dijalankan melalui FastAPI di Google Colab, diakses secara publik menggunakan Ngrok.

LLM Engine (Local): Llama 3 dijalankan secara lokal menggunakan Ollama API (127.0.0.1:11434).

Orchestrator: n8n sebagai pengatur logika alur kerja, pembersihan data, hingga pengiriman laporan.

📦 Persiapan & Instalasi
1. API IndoBERT (Cloud)
Jalankan file app_colab.py (tersedia di folder api/) pada Google Colab.

Model secara otomatis akan ditarik dari Hugging Face: Faol/indobert-sentiment-final-boss.

Masukkan NGROK_TOKEN Anda dan salin URL publik yang muncul (contoh: https://abcd-123.ngrok-free.dev/predict).

2. LLM Lokal (Ollama)
Pastikan Ollama terinstal di perangkat lokal (Rekomendasi Versi 0.13.5 atau terbaru).

Unduh dan jalankan model Llama 3:
ollama run llama3

3. Konfigurasi n8n
Instal n8n secara lokal (npm install n8n -g).

Import Workflow: Gunakan file IndoBERT_Hybrid_V5_Final.json yang ada di folder n8n/.

Penyesuaian Node:

Ganti URL pada node "IndoBERT Final Boss" dengan URL Ngrok terbaru Anda.

Masukkan kredensial SMTP pada node "Send email".

Masukkan URL Web App Google Apps Script Anda pada node "HTTP Request".

📂 Struktur Repositori
api/app_colab.py: Skrip FastAPI untuk deployment model IndoBERT.

n8n/IndoBERT_Hybrid_V5_Final.json: File ekspor workflow n8n.

requirements.txt: Daftar library Python yang diperlukan.

📊 Analisis Performa
Sistem dioptimalkan dengan logika Confidence Threshold:

Confidence > 0.6: Diproses langsung oleh IndoBERT (Fast Entity Extraction).

Confidence < 0.6: Dialihkan ke Ollama (Llama 3) untuk analisis mendalam.

👤 Author
Frenz Znerf (Faol)

Hugging Face Repository: indobert-sentiment-final-boss
