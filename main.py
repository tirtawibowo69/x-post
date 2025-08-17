import os
import random
import requests
import google.generativeai as genai
import tweepy
import urllib.parse
import feedparser

# --- FUNGSI UNTUK SCRAPING (DIPERBARUI DENGAN RSS) ---
def scrape_google_news_sports():
    """Mengambil satu berita olahraga teratas dari Google News RSS Feed untuk Amerika Serikat."""
    # URL RSS Feed untuk Google News seksi olahraga di Amerika Serikat
    rss_url = "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp1ZEdvU0FtVnpHZ0pKVGlnQVAB?hl=en-US&gl=US&ceid=US:en"
    try:
        # Parsing RSS feed
        news_feed = feedparser.parse(rss_url)

        if not news_feed.entries:
            print("Peringatan: Tidak ada berita yang ditemukan di RSS Feed.")
            return None

        # Mengambil semua judul berita dari feed
        news_titles = [entry.title for entry in news_feed.entries]

        # Memilih satu berita secara acak dari daftar
        selected_news = random.choice(news_titles)
        # print(f"Ditemukan {len(news_titles)} berita dari RSS, memilih satu secara acak: {selected_news}")
        return selected_news

    except Exception as e:
        print(f"Error saat mengakses atau parsing RSS Feed: {e}")
        return None

# --- FUNGSI UNTUK GENERASI KONTEN ---
def generate_post_with_gemini(trend):
    """Membuat konten post dengan Gemini API berdasarkan satu tren."""
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    if not gemini_api_key:
        # Menggunakan raise ValueError agar program berhenti jika kunci API tidak ada
        raise ValueError("GEMINI_API_KEY tidak ditemukan di environment variables!")

    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

    prompt = (
        f"You are a social media expert. Write a short, engaging post in English about this topic: '{trend}'. "
        f"The post MUST have a strong Call to Action to encourage clicks. "
        f"Do NOT add any links or hashtags in your response. Just provide the main text."
    )

    try:
        response = model.generate_content(prompt)
        # print("Konten berhasil dibuat oleh Gemini.")
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
def post_to_x(text_to_post, image_url=None):
    """Memposting teks dan gambar (opsional) ke X.com."""
    try:
        media_ids = []
        if image_url:
            auth = tweepy.OAuth1UserHandler(
                os.getenv('X_API_KEY'), os.getenv('X_API_SECRET'),
                os.getenv('X_ACCESS_TOKEN'), os.getenv('X_ACCESS_TOKEN_SECRET')
            )
            api = tweepy.API(auth)

            filename = 'temp_image.jpg'
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                with open(filename, 'wb') as image_file:
                    for chunk in response.iter_content(1024):
                        image_file.write(chunk)

                media = api.media_upload(filename=filename)
                media_ids.append(media.media_id_string)
                print("✅ Gambar berhasil di-upload.")
            else:
                print(f"Gagal mengunduh gambar. Status code: {response.status_code}")

        client = tweepy.Client(
            bearer_token=os.getenv('X_BEARER_TOKEN'),
            consumer_key=os.getenv('X_API_KEY'),
            consumer_secret=os.getenv('X_API_SECRET'),
            access_token=os.getenv('X_ACCESS_TOKEN'),
            access_token_secret=os.getenv('X_ACCESS_TOKEN_SECRET')
        )

        if media_ids:
            response = client.create_tweet(text=text_to_post, media_ids=media_ids)
        else:
            response = client.create_tweet(text=text_to_post)

        print(f"✅ Berhasil memposting tweet! ID: {response.data['id']}")

    except Exception as e:
        print(f"❌ GAGAL: Error saat memposting ke X.com: {e}")


# --- FUNGSI UTAMA (DIPERBAIKI DENGAN DEBUGGING) ---
if __name__ == "__main__":
    print("Memulai proses auto-posting...")

    # Langkah 1: Mengambil berita olahraga
    selected_news = scrape_google_news_sports()

    if selected_news:
        print(f"✅ Berita berhasil didapatkan: '{selected_news}'")

        # Langkah 2: Mendapatkan link acak
        random_link = get_random_link()
        if random_link:
            print(f"✅ Link berhasil didapatkan: '{random_link}'")

            # Langkah 3: Membuat konten dengan Gemini
            gemini_text = generate_post_with_gemini(selected_news)
            if gemini_text:
                print(f"✅ Teks dari Gemini berhasil dibuat.")
                # print(f"Teks dari Gemini: {gemini_text}") # Uncomment jika ingin lihat teksnya

                # Langkah 4: Membuat URL gambar
                image_url = f"https://tse1.mm.bing.net/th?q={urllib.parse.quote(selected_news)}"
                print(f"✅ URL Gambar dibuat: {image_url}")

                # Gabungkan teks dan link
                final_post_text = f"{gemini_text} {random_link}"

                print("\n--- POSTINGAN FINAL SIAP ---")
                print(f"Teks: {final_post_text}")
                print("----------------------------\n")

                # Langkah 5: Posting ke X.com
                post_to_x(final_post_text, image_url)

            else:
                print("❌ GAGAL: Gemini tidak dapat membuat konten. Proses dihentikan.")
        else:
            print("❌ GAGAL: Tidak ada link yang ditemukan di links.txt. Proses dihentikan.")
    else:
        print("❌ GAGAL: Tidak ada berita yang bisa diambil dari RSS Feed. Proses dihentikan.")

    print("\nProses selesai.")
