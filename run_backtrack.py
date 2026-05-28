import os
import argparse
import json
from datetime import datetime
from base_scraper import scrape_homepage

def main():
    # Setup penerima argumen dari terminal
    parser = argparse.ArgumentParser(description="Crawler Bisnis.com - Mode Backtrack")
    parser.add_argument("--start", required=True, help="Start date (Format: YYYY-MM-DD)")
    parser.add_argument("--end", required=True, help="End date (Format: YYYY-MM-DD)")
    args = parser.parse_args()

    try:
        # Ubah string input menjadi object datetime untuk perbandingan
        start_date = datetime.strptime(args.start, "%Y-%m-%d")
        # Tambahkan waktu 23:59:59 pada end date agar mencakup artikel di hari tersebut
        end_date = datetime.strptime(args.end, "%Y-%m-%d").replace(hour=23, minute=59, second=59)
    except ValueError:
        print("Error: Format tanggal salah. Gunakan format YYYY-MM-DD.")
        return

    print(f"Mencari artikel dari {args.start} hingga {args.end}...")
    
    # Ambil semua data (bisa dimodifikasi untuk pagination jika perlu)
    all_articles = scrape_homepage()
    filtered_articles = []

    # Filter artikel berdasarkan rentang tanggal
    for article in all_articles:
        try:
            pub_date = datetime.fromisoformat(article["published_at"])
            if start_date <= pub_date <= end_date:
                filtered_articles.append(article)
        except ValueError:
            continue

    # Buat folder tujuan
    output_dir = "output_json"
    os.makedirs(output_dir, exist_ok=True)

    # Gabungkan path folder dan nama file
    filename = f"backtrack_{args.start}_to_{args.end}.json"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(filtered_articles, f, indent=4, ensure_ascii=False)
        
    print(f"Selesai! Menyimpan {len(filtered_articles)} artikel ke {filepath}")

if __name__ == "__main__":
    main()