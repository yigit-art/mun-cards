import os
import requests
import pycountry

FLAG_CACHE_DIR = "static/flags"

COUNTRY_ALIASES = {
    "usa": "United States",
    "us": "United States",
    "united states of america": "United States",
    "uk": "United Kingdom",
    "great britain": "United Kingdom",
    "britain": "United Kingdom",
    "uae": "United Arab Emirates",
    "south korea": "Korea, Republic of",
    "north korea": "Korea, Democratic People's Republic of",
    "dprk": "Korea, Democratic People's Republic of",
    "russia": "Russian Federation",
    "iran": "Iran, Islamic Republic of",
    "syria": "Syrian Arab Republic",
    "venezuela": "Venezuela, Bolivarian Republic of",
    "bolivia": "Bolivia, Plurinational State of",
    "tanzania": "Tanzania, United Republic of",
    "vietnam": "Viet Nam",
    "laos": "Lao People's Democratic Republic",
    "moldova": "Moldova, Republic of",
    "brunei": "Brunei Darussalam",
    "ivory coast": "Côte d'Ivoire",
    "cote d'ivoire": "Côte d'Ivoire",
    "drc": "Congo, The Democratic Republic of the",
    "democratic republic of congo": "Congo, The Democratic Republic of the",
    "congo": "Congo",
    "republic of congo": "Congo",
    "czech republic": "Czechia",
    "macedonia": "North Macedonia",
    "swaziland": "Eswatini",
    "cape verde": "Cabo Verde",
    "turkey": "Türkiye",
    "türkiye": "Türkiye",
    "palestine": "Palestine, State of",
    "micronesia": "Micronesia, Federated States of",
    "burma": "Myanmar",
    "east timor": "Timor-Leste",
    "holy see": "Holy See",
    "vatican": "Holy See",
}


def normalize_country_name(raw_name):
    """CSV'den gelen ülke ismini pycountry'nin tanıyacağı hale getir."""
    key = raw_name.strip().lower()
    if key in COUNTRY_ALIASES:
        return COUNTRY_ALIASES[key]
    return raw_name.strip()


def get_country_code(raw_name):
    """
    Verilen ülke ismi için ISO 3166-1 alpha-2 kodunu (örn. 'tr') döner.
    Bulunamazsa None döner.
    """
    normalized = normalize_country_name(raw_name)

    if normalized is None:
        return None

    try:
        result = pycountry.countries.search_fuzzy(normalized)
        return result[0].alpha_2.lower()
    except LookupError:
        return None


def get_flag_path(raw_name):
    """
    Verilen ülke ismi için yerel bayrak dosyasının yolunu döner.
    Dosya önbellekte yoksa flagcdn'den indirir.
    Ülke bulunamazsa None döner.
    """
    code = get_country_code(raw_name)
    if not code:
        return None

    os.makedirs(FLAG_CACHE_DIR, exist_ok=True)
    local_path = os.path.join(FLAG_CACHE_DIR, f"{code}.png")

    if os.path.exists(local_path):
        return local_path.replace("\\", "/")

    url = f"https://flagcdn.com/w320/{code}.png"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        with open(local_path, "wb") as f:
            f.write(response.content)
        return local_path.replace("\\", "/")
    except requests.RequestException:
        return None


def check_countries(delegates):
    """
    Delege listesindeki tüm ülkeleri kontrol eder.
    Bulunamayanların isimlerini bir liste olarak döner (boşsa hepsi bulunmuş demektir).
    """
    not_found = []
    for delegate in delegates:
        code = get_country_code(delegate["country"])
        if not code:
            not_found.append(delegate["country"])
    return not_found