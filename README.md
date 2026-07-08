# MUN Kart Üretici

Model United Nations (MUN) konferansları için delege listesinden (CSV) otomatik olarak **yaka kartı** ve **plakkart** PDF'leri üreten bir Flask uygulaması. Sabit tasarımlı yaka kartlarının yanı sıra, kendi görselinizi yükleyip alanları (isim, ülke, komite, logo, bayrak) sürükle-bırak yerine tıklama ile konumlandırarak özel şablonlar da oluşturabilirsiniz.

## Özellikler

- **CSV'den delege listesi önizleme** — `name`, `country`, `committee` sütunlarını okur ve tabloyu gösterir.
- **Ülke doğrulama** — `pycountry` ile ülke isimlerini ISO 3166 standardına eşler; yaygın kısaltma ve alternatif isimler (`usa`, `uk`, `türkiye`, `dprk` vb.) için alias listesi içerir. Tanınmayan ülkeler varsa PDF üretilmeden önce hata döner.
- **Otomatik bayrak indirme** — Ülke koduna göre [flagcdn.com](https://flagcdn.com)'dan bayrak görselini indirip `static/flags/` altında önbelleğe alır.
- **Hazır tasarımlı yaka kartı PDF'i** — Sabit stilde (komite şeridi, isim, ülke) 90mm x 120mm yaka kartları üretir.
- **Özel şablon editörü** — Kendi arka plan görselinizi (ve isteğe bağlı logo) yükleyip, görsel üzerine tıklayarak isim/ülke/komite/logo/bayrak alanlarının konumunu, font boyutunu, rengini ve kalınlığını belirleyebilirsiniz. Şablon JSON olarak `templates_data/` altına kaydedilir ve bir şablon ID'si döner.
- **Özel şablonla yaka kartı veya plakkart üretimi** — Kaydedilen şablon ID'si ve delege CSV'si ile PDF üretir; plakkart için genişlik/yükseklik (mm) ayarlanabilir. Arayüzde tek bir form üzerinden dropdown ile kart türü seçilir.

## Kullanılan Teknolojiler

- **Python 3** / **Flask** — web sunucusu ve route'lar
- **WeasyPrint** — HTML/CSS'ten PDF üretimi
- **Jinja2** (Flask ile birlikte gelir) — HTML şablonlama
- **pycountry** — ülke ismi normalizasyonu ve ISO kod eşleme
- **requests** — flagcdn.com'dan bayrak görseli indirme
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

1. **Delege listesini önizle**: `name,country,committee` sütunlu bir CSV yükleyip listeyi kontrol edin.
2. **Yaka kartlarını PDF olarak indir**: Aynı CSV ile sabit tasarımlı yaka kartı PDF'i üretin.
3. **Özel şablon oluştur**:
   - "Şablon Yükle" formuyla arka plan görseli (ve isteğe bağlı logo) yükleyin.
   - Açılan şablon editöründe görsele tıklayarak alanları (isim, ülke, komite, logo, bayrak) yerleştirin, font ayarlarını girin ve "Kaydet"e basın. Size bir **şablon ID**'si verilecektir.
4. **Özel şablonla kart oluştur**: Şablon ID'sini girin, kart türünü (Yaka kartı / Plakkart) dropdown'dan seçin, plakkart için genişlik/yükseklik (mm) girin, CSV'yi yükleyip PDF'i indirin.

## CSV Formatı

```csv
name,country,committee
Ahmet Yılmaz,Turkey,UNSC
Jane Doe,United States,UNGA
```

## Proje Yapısı

```
app.py               Flask route'ları
generator.py          CSV ayrıştırma, şablon kaydetme/yükleme, PDF üretim mantığı
country_flags.py      Ülke ismi normalizasyonu, ISO kod eşleme, bayrak indirme
templates/            Jinja2 HTML şablonları (arayüz, kart tasarımları, şablon editörü)
static/flags/         Önbelleğe alınmış bayrak görselleri
static/uploads/       Yüklenen şablon/logo görselleri
templates_data/       Kaydedilen özel şablonların JSON dosyaları
```
