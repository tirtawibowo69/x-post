import os
import random
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import tweepy

# --- FUNGSI UNTUK SCRAPING ---
def scrape_trends_from_trends24():
    """Mengambil 4 tren teratas dari trends24.in untuk United States."""
    url = "https://trends24.in/united-states/"
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        trend_list = soup.select('ol.trend-card__list li a')
        
        trends = [trend.text.strip().replace('#', '') for trend in trend_list[:4]]
        
        if not trends:
            print("Peringatan: Tidak ada tren yang ditemukan. Mungkin struktur website berubah.")
            return None
            
        print(f"Tren yang ditemukan: {trends}")
        return trends
    except requests.exceptions.RequestException as e:
        print(f"Error saat mengakses trends24.in: {e}")
        return None

# --- FUNGSI UNTUK GENERASI KONTEN ---
# --- DIUBAH --- Memperbarui fungsi untuk membuat prompt yang lebih spesifik
def generate_post_with_gemini(trends, link):
    """Membuat konten post dengan Gemini API, menyertakan CTA dan link."""
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY tidak ditemukan di environment variables!")
        
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    # --- DIUBAH --- Prompt yang lebih detail untuk menghasilkan CTA
    prompt = (
        f"You are a social media expert creating a post for X.com. "
        f"Write a short, engaging post in English about these topics: '{', '.join(trends)}'. The post MUST include a strong Call to Action {link}"
        f"Do NOT add any hashtags in your response. Just provide the main text with the CTA and the link."
    )
    
    try:
        response = model.generate_content(prompt)
        print("Konten berhasil dibuat oleh Gemini.")
        # Membersihkan output dari Gemini jika ada markdown atau karakter aneh
        return response.text.strip()
    except Exception as e:
        print(f"Error saat menghubungi Gemini API: {e}")
        return None

# --- FUNGSI UNTUK MENDAPATKAN LINK ---
def get_random_link(filename="links.txt"):
    """Membaca file dan memilih satu link secara acak."""
    try:
        with open(filename, 'r') as f:
            links = [line.strip() for line in f if line.strip()]
        return random.choice(links) if links else None
    except FileNotFoundError:
        print(f"Error: File '{filename}' tidak ditemukan.")
        return None

# --- FUNGSI UNTUK POSTING KE X.COM ---
def post_to_x(text_to_post):
    """Memposting teks ke X.com menggunakan API v2."""
    try:
        client = tweepy.Client(
            bearer_token=os.getenv('X_BEARER_TOKEN'),
            consumer_key=os.getenv('X_API_KEY'),
            consumer_secret=os.getenv('X_API_SECRET'),
            access_token=os.getenv('X_ACCESS_TOKEN'),
            access_token_secret=os.getenv('X_ACCESS_TOKEN_SECRET')
        )
        response = client.create_tweet(text=text_to_post)
        print(f"Berhasil memposting tweet ID: {response.data['id']}")
    except Exception as e:
        print(f"Error saat memposting ke X.com: {e}")

# --- FUNGSI UTAMA ---
if __name__ == "__main__":
    print("Memulai proses auto-posting...")
    
    top_trends = scrape_trends_from_trends24()
    
    if top_trends:
        random_link = get_random_link()
        
        if random_link:
            gemini_text = generate_post_with_gemini(top_trends, random_link)
            
            if gemini_text:
                # --- DIUBAH --- Logika baru untuk memformat postingan
                print(f"Teks dari Gemini: {gemini_text}")

                # 1. Membuat string hashtag dari daftar tren
                # Menghilangkan spasi dari tren untuk hashtag yang valid (misal: "New York" -> "#NewYork")
                hashtags_string = " ".join([f"#{trend.replace(' ', '')}" for trend in top_trends])
                print(f"Hashtag yang dibuat: {hashtags_string}")

                # 2. Menggabungkan teks AI dan hashtag dengan format yang diinginkan
                # Menggunakan "\n\n" untuk membuat baris kosong (enter)
                final_post = f"{gemini_text}\n\n{hashtags_string}"
                
                print("--- POSTINGAN FINAL ---")
                print(final_post)
                print("-----------------------")
                
                # 3. Posting ke X.com
                post_to_x(final_post)
    
    print("Proses selesai.")