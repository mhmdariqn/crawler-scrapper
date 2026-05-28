from base_scraper import scrape_homepage
import json

if __name__ == "__main__":
    print("Mencoba scraping halaman utama...")
    hasil = scrape_homepage()
    
    # Tampilkan 2 artikel pertama saja dalam bentuk JSON yang rapi
    if hasil:
        print(json.dumps(hasil[:2], indent=4, ensure_ascii=False))
    else:
        print("Scraping gagal atau data tidak ditemukan.")