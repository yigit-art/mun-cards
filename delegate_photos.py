import os
import hashlib
import requests

PHOTO_CACHE_DIR = "static/photos"


def get_delegate_photo(url):
    """
    Verilen URL'den delege fotoğrafını indirip yerel önbelleğe alır.
    Yerel dosya yolunu döner. URL boşsa veya indirilemezse None döner.
    """
    if not url:
        return None

    os.makedirs(PHOTO_CACHE_DIR, exist_ok=True)

    url_hash = hashlib.sha256(url.encode("utf-8")).hexdigest()
    ext = os.path.splitext(url.split("?")[0])[1]
    if not ext or len(ext) > 5:
        ext = ".jpg"
    local_path = os.path.join(PHOTO_CACHE_DIR, f"{url_hash}{ext}")

    if os.path.exists(local_path):
        return local_path.replace("\\", "/")

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        with open(local_path, "wb") as f:
            f.write(response.content)
        return local_path.replace("\\", "/")
    except requests.RequestException:
        return None
