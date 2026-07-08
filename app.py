from flask import Flask, render_template, request, send_file
from country_flags import check_countries
import generator

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    csv_file = request.files.get("csv_file")
    if not csv_file:
        return "CSV dosyası yüklenmedi.", 400

    delegates = generator.parse_csv(csv_file)
    missing_countries = check_countries(delegates)
    if missing_countries:
        return f"Şu ülkeler bulunamadı, lütfen kontrol edin: {', '.join(missing_countries)}", 400

    return render_template("delegeler.html", delegates=delegates)


@app.route("/generate-badges", methods=["POST"])
def generate_badges():
    csv_file = request.files.get("csv_file")
    if not csv_file:
        return "CSV dosyası yüklenmedi.", 400

    delegates = generator.parse_csv(csv_file)
    pdf = generator.render_badges_pdf(delegates, request.url_root)

    return pdf, 200, {
        "Content-Type": "application/pdf",
        "Content-Disposition": "inline; filename=badges.pdf",
    }


@app.route("/upload-template", methods=["POST"])
def upload_template():
    image_file = request.files.get("template_image")
    if not image_file:
        return "Görsel dosyası yüklenmedi.", 400

    web_path = generator.save_uploaded_image(image_file)

    logo_web_path = None
    logo_file = request.files.get("logo_image")
    if logo_file and logo_file.filename:
        logo_web_path = generator.save_uploaded_image(logo_file)

    return render_template(
        "template_editor.html",
        image_path=web_path,
        logo_path=logo_web_path
    )


@app.route("/save-template", methods=["POST"])
def save_template():
    data = request.get_json()
    fields = data.get("fields", [])
    image_path = data.get("image_path", "")
    logo_path = data.get("logo_path")

    if not fields or not image_path:
        return {"error": "Eksik alanlar."}, 400

    template_id = generator.save_template(fields, image_path, logo_path)

    return {"message": "Şablon kaydedildi", "template_id": template_id}, 200


@app.route("/generate-badges-custom/<template_id>", methods=["POST"])
def generate_badges_custom(template_id):
    csv_file = request.files.get("csv_file")
    if not csv_file:
        return "CSV dosyası yüklenmedi.", 400

    cards_per_page = request.form.get("cards_per_page", default=1, type=int)

    delegates = generator.parse_csv(csv_file)
    generator.attach_media_paths(delegates)

    template_data = generator.load_template(template_id)
    if template_data is None:
        return "Şablon bulunamadı.", 404

    pdf = generator.render_badges_custom_pdf(
        delegates, template_data, request.url_root, cards_per_page=cards_per_page
    )

    return pdf, 200, {
        "Content-Type": "application/pdf",
        "Content-Disposition": "inline; filename=badges.pdf",
    }


@app.route("/generate-placards-custom/<template_id>", methods=["POST"])
def generate_placards_custom(template_id):
    csv_file = request.files.get("csv_file")
    if not csv_file:
        return "CSV dosyası yüklenmedi.", 400

    width_mm = request.form.get("width_mm", type=float)
    height_mm = request.form.get("height_mm", type=float)
    if not width_mm or not height_mm:
        return "Genişlik ve yükseklik girilmedi.", 400

    cards_per_page = request.form.get("cards_per_page", default=1, type=int)

    delegates = generator.parse_csv(csv_file)
    generator.attach_media_paths(delegates)

    template_data = generator.load_template(template_id)
    if template_data is None:
        return "Şablon bulunamadı.", 404

    pdf = generator.render_placards_custom_pdf(
        delegates, template_data, width_mm, height_mm, request.url_root,
        cards_per_page=cards_per_page,
    )

    return pdf, 200, {
        "Content-Type": "application/pdf",
        "Content-Disposition": "inline; filename=placards.pdf",
    }


@app.route("/download-sample")
def download_sample():
    return send_file(
        "sample.csv",
        as_attachment=True,
        download_name="sample.csv",
        mimetype="text/csv",
    )


if __name__ == "__main__":
    app.run(debug=True)
