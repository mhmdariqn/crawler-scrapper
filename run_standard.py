import os
import json
import time
import schedule
from datetime import datetime
from base_scraper import scrape_homepage

# Kumpulan link yang sudah pernah ditarik agar tidak duplikat
seen_links = set()

def job_scrape(interval_minutes):
    global seen_links
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Menjalankan crawler...")
    
    articles = scrape_homepage()
    new_articles = []
    
    # Saring hanya artikel yang belum pernah ditarik
    for article in articles:
        if article["link"] not in seen_links:
            new_articles.append(article)
            seen_links.add(article["link"])
            
    if new_articles:
        output_dir = "output_json"
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"standard_latest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(new_articles, f, indent=4, ensure_ascii=False)
        print(f"-> Ditemukan {len(new_articles)} artikel baru. Disimpan di {filepath}")
    else:
        print("-> Tidak ada artikel baru.")
        
    print(f"Menunggu {interval_minutes} menit untuk penarikan selanjutnya...\n")

def main():
    # Konfigurasi interval (contoh: jalan setiap 30 menit)
    INTERVAL_MINUTES = 1
    
    print(f"Memulai Crawler Mode Standard (Interval: {INTERVAL_MINUTES} menit)...")
    print("Tekan Ctrl+C untuk berhenti.\n")
    
    # Jalankan langsung saat pertama kali dihidupkan
    job_scrape(INTERVAL_MINUTES)
    
    # Jadwalkan penarikan berikutnya
    schedule.every(INTERVAL_MINUTES).minutes.do(job_scrape, interval_minutes=INTERVAL_MINUTES)
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nProses dihentikan oleh pengguna.")

if __name__ == "__main__":
    main()