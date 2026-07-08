import os
import csv
import io
import json
import uuid
from flask import render_template
from weasyprint import HTML
from werkzeug.utils import secure_filename
from country_flags import get_flag_path

UPLOAD_FOLDER = "static/uploads"
TEMPLATES_FOLDER = "templates_data"


def parse_csv(file_storage):
    """Read an uploaded CSV file and return a list of delegate dicts."""
    stream = io.StringIO(file_storage.stream.read().decode("utf-8"))
    reader = csv.DictReader(stream)
    delegates = []
    for row in reader:
        delegates.append({
            "name": row.get("name", "").strip(),
            "country": row.get("country", "").strip(),
            "committee": row.get("committee", "").strip(),
        })
    return delegates


def attach_flag_paths(delegates):
    """Attach a flag_path key to each delegate dict, in place."""
    for delegate in delegates:
        delegate["flag_path"] = get_flag_path(delegate["country"])
    return delegates


def save_uploaded_image(image_file):
    """Save an uploaded image under a unique name and return its web path."""
    original_filename = secure_filename(image_file.filename)
    unique_filename = f"{uuid.uuid4().hex}_{original_filename}"
    image_path = os.path.join(UPLOAD_FOLDER, unique_filename)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    image_file.save(image_path)
    return image_path.replace("\\", "/")


def save_template(fields, image_path, logo_path):
    """Persist a badge/placard template as JSON and return its id."""
    template_data = {
        "background_image": image_path,
        "logo_image": logo_path,
        "fields": fields,
    }

    template_id = str(uuid.uuid4())
    template_filename = f"template_{template_id}.json"
    os.makedirs(TEMPLATES_FOLDER, exist_ok=True)
    template_path = os.path.join(TEMPLATES_FOLDER, template_filename)

    with open(template_path, "w", encoding="utf-8") as f:
        json.dump(template_data, f, ensure_ascii=False, indent=2)

    return template_id


def load_template(template_id):
    """Load a previously saved template by id, or None if it doesn't exist."""
    template_path = os.path.join(TEMPLATES_FOLDER, f"template_{template_id}.json")
    if not os.path.exists(template_path):
        return None

    with open(template_path, "r", encoding="utf-8") as f:
        return json.load(f)


def render_badges_pdf(delegates, base_url):
    html_string = render_template("badge.html", delegates=delegates)
    return HTML(string=html_string, base_url=base_url).write_pdf()


def render_badges_custom_pdf(delegates, template_data, base_url):
    html_string = render_template(
        "badge_dynamic.html",
        delegates=delegates,
        background_image=template_data["background_image"],
        logo_image=template_data.get("logo_image"),
        fields=template_data["fields"],
    )
    return HTML(string=html_string, base_url=base_url).write_pdf()


def render_placards_custom_pdf(delegates, template_data, width_mm, height_mm, base_url):
    html_string = render_template(
        "placard_dynamic.html",
        delegates=delegates,
        background_image=template_data["background_image"],
        logo_image=template_data.get("logo_image"),
        fields=template_data["fields"],
        width_mm=width_mm,
        height_mm=height_mm,
    )
    return HTML(string=html_string, base_url=base_url).write_pdf()
