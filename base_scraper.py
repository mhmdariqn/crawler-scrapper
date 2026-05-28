import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re

def parse_indo_date_to_iso(date_str: str) -> str:
    """Mengubah string tanggal bahasa Indonesia ke format ISO 8601."""
    bulan_indo = {
        'januari': '01', 'februari': '02', 'maret': '03', 'april': '04',
        'mei': '05', 'juni': '06', 'juli': '07', 'agustus': '08',
        'september': '09', 'oktober': '10', 'november': '11', 'desember': '12'
    }
    
    try:
        # Ubah ke huruf kecil untuk mempermudah pencocokan
        date_str = date_str.lower()
        
        # Ganti nama bulan dengan angka
        for nama, angka in bulan_indo.items():
            if nama in date_str:
                date_str = date_str.replace(nama, angka)
                break
                
        # Ekstrak semua angka di dalam string [tanggal, bulan, tahun, jam, menit]
        match = re.findall(r'\d+', date_str)
        
        if len(match) >= 5:
            # Format datetime(year, month, day, hour, minute)
            dt = datetime(int(match[2]), int(match[1]), int(match[0]), int(match[3]), int(match[4]))
            return dt.isoformat()
            
    except Exception as e:
        print(f"Gagal memparsing tanggal '{date_str}': {e}")
        
    return datetime.now().isoformat() # Fallback ke waktu saat ini jika gagal

def get_article_details(url: str) -> dict:
    """Melakukan scraping ke halaman dalam artikel untuk mengambil isi dan tanggal pastinya."""
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. Mengambil Isi Artikel
        content = ""
        content_div = soup.find(class_='detailsContent')
        if content_div:
            paragraphs = content_div.find_all('p')
            content = " ".join([p.text.strip() for p in paragraphs])
            
        # 2. Mengambil Tanggal Terbit
        published_at = ""
        date_div = soup.find(class_='detailsAttributeDates')
        if date_div:
            date_text = date_div.text.strip()
            published_at = parse_indo_date_to_iso(date_text)
            
        return {
            "content": content,
            "published_at": published_at
        }
    except Exception as e:
        print(f"Gagal mengambil detail dari {url}: {e}")
        return {"content": "", "published_at": datetime.now().isoformat()}

def scrape_homepage(url: str = "https://www.bisnis.com"):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    articles_data = []
    
    # Langsung cari tag <a> yang memiliki class 'artLink'
    for a_tag in soup.find_all('a', class_='artLink'):
        # Pastikan tag <a> ini memiliki judul di dalamnya
        title_tag = a_tag.find(class_='artTitle')
        if not title_tag:
            continue
            
        title = title_tag.text.strip()
        link = a_tag.get('href')
        
        if not link.startswith('http'):
             link = "https://www.bisnis.com" + link
             
        # Ambil tanggal dari dalam artikel dan isi teksnya
        details = get_article_details(link)
        
        # Validasi jika gagal mengambil isi
        if not details["content"]:
            continue
            
        articles_data.append({
            "link": link,
            "title": title,
            "published_at": details["published_at"],
            "content": details["content"]
        })
        
        # scrapping brp artikel
        # if len(articles_data) >= 2:
        #     break
            
    return articles_data