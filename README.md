EN
# MUN Card Generator

A Flask web application that automatically generates name badges and placards (PDF) for Model United Nations (MUN) conferences from a participant list (CSV). I built this to solve a real problem I experienced as Head of IT at KAFMUN: designing hundreds of cards by hand before every conference.

## Features

- **Bulk generation from CSV** — produces cards for every participant in one go from a CSV file containing name and country/committee information
- **Upload your own design** — users can upload their own background artwork (badge/placard design) instead of being locked into a single template
- **Click-to-place editor** — click directly on the uploaded design to mark exactly where the name, country, committee, logo, and photo fields should appear
- **Customizable typography** — font size, color, and weight can be set individually for each field
- **Dynamic placard sizing** — unlike badges, placard dimensions vary by conference, so size is entered through the form
- **Automatic country flag matching** — maps everyday country names from the CSV (e.g. "Turkey", "USA", "South Korea") to the correct ISO code using `pycountry` plus an alias table, then fetches the flag from flagcdn, caching it locally so it's never re-downloaded
- **Delegate photo support** — an optional photo URL column in the CSV lets participant photos be placed on the card
- **Multiple cards per page** — users choose how many cards should fit on a single PDF page, with dashed cutting guides to make trimming easier

## Tech Stack

- **Backend:** Python, Flask
- **PDF generation:** WeasyPrint (HTML/CSS → PDF)
- **Templating:** Jinja2
- **Country/flag matching:** pycountry, flagcdn.com
- **Frontend:** HTML, CSS, vanilla JavaScript (Fetch API for async form submission)

## How It Works (Architecture Overview)

1. The user uploads a background image (`/upload-template`)
2. They click on the image to mark field positions as **percentages** (not pixels — this keeps the ratio consistent between the small preview and the actual full-size PDF)
3. This position/style data is saved as a JSON template on disk (`/save-template`)
4. The user uploads a CSV, picks the card type (badge/placard), and sets size/cards-per-page options if applicable
5. The backend renders HTML for every participant based on the saved JSON template (Jinja2), and WeasyPrint converts it to PDF

## Setup

```bash
python -m venv venv
venv\Scripts\Activate.ps1   # Windows
pip install -r requirements.txt
python app.py
```

Then open `http://127.0.0.1:5000/` in your browser.

## Example CSV format

```csv
name,country,committee,photo_url
Ayşe Yılmaz,Turkey,UNSC,
John Smith,United Kingdom,UNGA,
```

## Roadmap

- QR code support (for delegate verification/check-in)
- PNG export format
- Deployment/hosting so the tool can be used across multiple MUN conferences
TR
# MUN Kart Üretici

Model United Nations (MUN) konferansları için delege listesinden (CSV) otomatik olarak **yaka kartı** ve **plakkart** PDF'leri üreten bir Flask uygulaması. Sabit tasarımlı yaka kartlarının yanı sıra, kendi görselinizi yükleyip alanları (isim, ülke, komite, logo, bayrak, fotoğraf) tıklama ile konumlandırarak özel şablonlar da oluşturabilir; tek bir PDF'te sayfa başına birden fazla kart basabilirsiniz.

## Özellikler

- **CSV'den delege listesi önizleme** — `name`, `country`, `committee` sütunlarını okur ve tabloyu gösterir.
- **Ülke doğrulama** — `pycountry` ile ülke isimlerini ISO 3166 standardına eşler; yaygın kısaltma ve alternatif isimler (`usa`, `uk`, `türkiye`, `dprk` vb.) için alias listesi içerir. Tanınmayan ülkeler varsa PDF üretilmeden önce hata döner.
- **Otomatik bayrak indirme** — Ülke koduna göre [flagcdn.com](https://flagcdn.com)'dan bayrak görselini indirip `static/flags/` altında önbelleğe alır.
- **Katılımcı fotoğrafı desteği** — CSV'deki opsiyonel `photo_url` sütunundan verilen görseli indirip `static/photos/` altında önbelleğe alır (`delegate_photos.py`); sütun yoksa veya URL boş/geçersizse sorun çıkarmaz, ilgili alan sadece atlanır.
- **Hazır tasarımlı yaka kartı PDF'i** — Sabit stilde (komite şeridi, isim, ülke) 90mm x 120mm yaka kartları üretir.
- **Özel şablon editörü** — Kendi arka plan görselinizi (ve isteğe bağlı logo) yükleyip, görsel üzerine tıklayarak isim/ülke/komite/logo/bayrak/fotoğraf alanlarının konumunu, font boyutunu, rengini ve kalınlığını belirleyebilirsiniz. Şablon JSON olarak `templates_data/` altına kaydedilir ve bir şablon ID'si döner.
- **Özel şablonla yaka kartı veya plakkart üretimi** — Kaydedilen şablon ID'si ve delege CSV'si ile PDF üretir; plakkart için genişlik/yükseklik (mm) ayarlanabilir. Arayüzde tek bir form üzerinden dropdown ile kart türü seçilir.
- **Sayfa başına çoklu kart (print grid)** — "Sayfa Başına Kart" değeri girilerek birden fazla kart aynı PDF sayfasına, otomatik hesaplanan bir CSS grid (satır/sütun sayısı kart adedinin kareköküne göre belirlenir) ile yerleştirilir.
- **Kesim çizgileri** — Grid içindeki her kartın kenarında ince kesikli (dashed) gri çizgi bulunur; yazdırıp makasla kesmek için görsel referans sağlar.
- **Örnek CSV indirme** — Ana sayfadaki "Örnek Şablonu İndir" butonu, `/download-sample` route'u üzerinden doğru sütun başlıklarını (`name,country,committee,photo_url`) içeren bir `sample.csv` indirir.

## Kullanılan Teknolojiler

- **Python 3** / **Flask** — web sunucusu ve route'lar
- **WeasyPrint** — HTML/CSS'ten PDF üretimi
- **Jinja2** (Flask ile birlikte gelir) — HTML şablonlama, `batch` filtresiyle sayfa başına kart gruplama
- **pycountry** — ülke ismi normalizasyonu ve ISO kod eşleme
- **requests** — flagcdn.com'dan bayrak ve verilen URL'lerden delege fotoğrafı indirme
- **Werkzeug** — güvenli dosya adlandırma (`secure_filename`)
- Vanilla **HTML/CSS/JavaScript** — arayüz ve şablon editörü (`fetch` ile AJAX istekleri)

## Kurulum

1. Depoyu klonlayın / indirin ve proje klasörüne girin.
2. Sanal ortam oluşturup etkinleştirin (Windows / PowerShell):
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
3. Gerekli paketleri kurun:
   ```powershell
   pip install flask weasyprint werkzeug requests pycountry
   ```
   > **Not:** WeasyPrint, Windows'ta ek olarak GTK için sistem kütüphaneleri (Pango, Cairo vb.) gerektirir. Kurulum sorunu yaşarsanız [WeasyPrint Windows kurulum belgelerine](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#windows) bakın.

## Çalıştırma

```powershell
python app.py
```

Uygulama varsayılan olarak `http://127.0.0.1:5000` adresinde, debug modunda çalışır. Tarayıcıdan bu adrese giderek arayüzü kullanabilirsiniz.

## Kullanım Akışı

1. **Delege listesini önizle**: `name,country,committee` (ve opsiyonel `photo_url`) sütunlu bir CSV yükleyip listeyi kontrol edin. Doğru formatı görmek için ana sayfadaki "Örnek Şablonu İndir" ile `sample.csv` indirebilirsiniz.
2. **Yaka kartlarını PDF olarak indir**: Aynı CSV ile sabit tasarımlı yaka kartı PDF'i üretin.
3. **Özel şablon oluştur**:
   - "Şablon Yükle" formuyla arka plan görseli (ve isteğe bağlı logo) yükleyin.
   - Açılan şablon editöründe görsele tıklayarak alanları (isim, ülke, komite, logo, bayrak, fotoğraf) yerleştirin, font ayarlarını girin ve "Kaydet"e basın. Size bir **şablon ID**'si verilecektir.
4. **Özel şablonla kart oluştur**: Şablon ID'sini girin, kart türünü (Yaka kartı / Plakkart) dropdown'dan seçin, plakkart için genişlik/yükseklik (mm) girin, isteğe bağlı olarak "Sayfa Başına Kart" sayısını artırın, CSV'yi yükleyip PDF'i indirin. Kartlar otomatik hesaplanan bir grid'e yerleştirilir ve aralarında kesim çizgileri bulunur.

## CSV Formatı

```csv
name,country,committee,photo_url
Ahmet Yılmaz,Turkey,UNSC,
Jane Doe,United States,UNGA,https://example.com/jane.jpg
```

`photo_url` sütunu tamamen opsiyoneldir; sütun hiç yoksa veya bir satırda boşsa uygulama sorunsuz çalışmaya devam eder, sadece o delege için fotoğraf alanı boş kalır.

## Proje Yapısı

```
app.py                Flask route'ları
generator.py           CSV ayrıştırma, grid/sayfa hesaplama, şablon kaydetme/yükleme, PDF üretim mantığı
country_flags.py       Ülke ismi normalizasyonu, ISO kod eşleme, bayrak indirme
delegate_photos.py     Delege fotoğrafı indirme ve önbelleğe alma (photo_url -> static/photos/)
sample.csv             /download-sample route'unun sunduğu örnek CSV şablonu
templates/             Jinja2 HTML şablonları (arayüz, kart tasarımları, şablon editörü, katılımcı listesi)
static/flags/          Önbelleğe alınmış bayrak görselleri
static/photos/         Önbelleğe alınmış delege fotoğrafları
static/uploads/        Yüklenen şablon/logo görselleri
templates_data/        Kaydedilen özel şablonların JSON dosyaları
```
