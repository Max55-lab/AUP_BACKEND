from flask import Flask, request, jsonify

app = Flask(__name__)


# =========================
# HOME
# =========================
@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to Flask demo API",
        "status": "running"
    })


# =========================
# BASIC INFO ROUTES
# =========================
@app.route("/kontakt")
def contact():
    return jsonify({
        "contact": "063 123 456"
    })


@app.route("/email")
def email():
    return jsonify({
        "email": "hrvoje.ljubic@sum.ba"
    })


# =========================
# DYNAMIC ROUTES
# =========================
@app.route("/pozdrav/<ime>")
def pozdrav(ime):
    return jsonify({
        "message": f"Hello {ime}"
    })


@app.route("/pozdrav/<ime>/<prezime>")
def pozdrav2(ime, prezime):
    return jsonify({
        "message": f"Hello {ime} {prezime}"
    })


@app.route("/zbroji/<int:broj1>/<int:broj2>")
def zbroji(broj1, broj2):
    return jsonify({
        "broj1": broj1,
        "broj2": broj2,
        "rezultat": broj1 + broj2
    })


# =========================
# LOGIN (QUERY PARAMS)
# =========================
@app.route("/prijava")
def prijava():
    kor_ime = request.args.get("kor_ime", "")
    lozinka = request.args.get("lozinka", "")

    if kor_ime == "marko" and lozinka == "123456":
        return jsonify({"msg": "Login successful"})
    else:
        return jsonify({"msg": "Invalid credentials"}), 401


# =========================
# APP INFO
# =========================
@app.route("/app_info")
def app_info():
    return jsonify({
        "app": "Flask Demo API",
        "course": "Algoritmi u primjeni",
        "year": "2025/2026",
        "tech": ["Flask", "JSON"]
    })


# =========================
# HTML DEMO
# =========================
@app.route("/html")
def html():
    return """
    <h2>Flask Demo</h2>
    <p style="color:red;">This is a paragraph.</p>
    <a href="https://google.com">Google link</a>
    """


# =========================
# POST: MULTIPLY
# =========================
@app.route("/pomnozi", methods=["POST"])
def pomnozi():
    data = request.get_json(silent=True) or {}

    broj1 = data.get("broj1", 0)
    broj2 = data.get("broj2", 0)

    return jsonify({
        "broj1": broj1,
        "broj2": broj2,
        "rezultat": broj1 * broj2
    })


# =========================
# MIXED INPUT (URL + BODY + QUERY)
# =========================
@app.route("/zadnja/<jmbg>", methods=["POST"])
def zadnja(jmbg):
    data = request.get_json(silent=True) or {}

    return jsonify({
        "jmbg": jmbg,
        "ime": data.get("ime"),
        "prezime": data.get("prezime"),
        "godiste": request.args.get("godiste")
    })


# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(debug=True,port=5001)