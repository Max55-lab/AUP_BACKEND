# =========================================================
# IMPORTI
# =========================================================

from flask import Flask, jsonify, request
from flask_cors import CORS
from extensions import db, migrate
from models import User, Game, Library, Review
from datetime import date

# =========================================================
# KREIRANJE APP
# =========================================================

app = Flask(__name__)

# =========================================================
# CORS
# =========================================================

CORS(app, supports_credentials=True)

# =========================================================
# DATABASE CONFIG
# =========================================================

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:@localhost/Game_Library"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# =========================================================
# INIT DB
# =========================================================

db.init_app(app)
migrate.init_app(app, db)

# =========================================================
# HOME
# =========================================================

@app.route("/")
def index():

    return jsonify({
        "msg": "Game Library API radi ispravno"
    })

# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard", methods=["GET"])
def dashboard():

    total_users = User.query.count()
    total_games = Game.query.count()
    total_reviews = Review.query.count()
    total_library_entries = Library.query.count()

    avg_query = db.session.query(
        db.func.avg(Review.rating)
    ).scalar()

    average_rating = (
        float(round(avg_query, 2))
        if avg_query else 0
    )

    return jsonify({
        "total_users": total_users,
        "total_games": total_games,
        "total_reviews": total_reviews,
        "total_library_entries": total_library_entries,
        "average_rating": average_rating
    })

# =========================================================
# USERS
# =========================================================

@app.route("/users", methods=["GET"])
def get_users():

    users = User.query.all()

    return jsonify([
        u.to_dict()
        for u in users
    ])

@app.route("/users", methods=["POST"])
def add_user():

    data = request.get_json()

    if not data.get("username") or not data.get("email"):

        return jsonify({
            "error": "Podaci su obavezni"
        }), 400

    try:

        user = User(
            username=data["username"],
            email=data["email"]
        )

        db.session.add(user)
        db.session.commit()

        return jsonify({
            "msg": "Korisnik dodan"
        })

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "error": str(e)
        }), 500

@app.route(
    "/users/<int:user_id>",
    methods=["GET", "PUT", "DELETE"]
)
def handle_user(user_id):

    user = User.query.get_or_404(user_id)

    # GET
    if request.method == "GET":

        return jsonify(user.to_dict())

    # PUT
    if request.method == "PUT":

        data = request.get_json()

        user.username = data.get(
            "username",
            user.username
        )

        user.email = data.get(
            "email",
            user.email
        )

        db.session.commit()

        return jsonify({
            "msg": "Korisnik ažuriran"
        })

    # DELETE
    if request.method == "DELETE":

        db.session.delete(user)
        db.session.commit()

        return jsonify({
            "msg": "Korisnik obrisan"
        })
    return None


# =========================================================
# GAMES
# =========================================================

@app.route("/games", methods=["GET"])
def get_games():

    search = request.args.get("search", "")

    page = request.args.get("page", 1, type=int)

    per_page = request.args.get(
        "per_page",
        50,
        type=int
    )

    query = Game.query

    if search:

        query = query.filter(
            Game.title.ilike(f"%{search}%")
        )

    pag = db.paginate(
        query,
        page=page,
        per_page=per_page,
        error_out=False
    )

    return jsonify({

        "items": [
            g.to_dict()
            for g in pag.items
        ],

        "total_items": pag.total,
        "total_pages": pag.pages,
        "current_page": pag.page
    })

@app.route("/games", methods=["POST"])
def add_game():

    data = request.get_json()

    try:

        game = Game(
            title=data["title"],
            genre=data.get("genre"),
            release_year=data.get("release_year")
        )

        db.session.add(game)
        db.session.commit()

        return jsonify({
            "msg": "Igra dodana"
        })

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "error": str(e)
        }), 500

@app.route(
    "/games/<int:game_id>",
    methods=["GET", "PUT", "DELETE"]
)
def handle_game(game_id):

    game = Game.query.get_or_404(game_id)

    # GET
    if request.method == "GET":

        return jsonify(game.to_dict())

    # PUT
    if request.method == "PUT":

        data = request.get_json()

        game.title = data.get(
            "title",
            game.title
        )

        game.genre = data.get(
            "genre",
            game.genre
        )

        game.release_year = data.get(
            "release_year",
            game.release_year
        )

        db.session.commit()

        return jsonify({
            "msg": "Igra ažurirana"
        })

    # DELETE
    if request.method == "DELETE":

        db.session.delete(game)
        db.session.commit()

        return jsonify({
            "msg": "Igra obrisana"
        })
    return None


# =========================================================
# LIBRARY
# =========================================================

@app.route("/library", methods=["GET", "POST"])
def library_base():

    # POST
    if request.method == "POST":

        data = request.get_json()

        try:

            entry = Library(
                user_id=data["user_id"],
                game_id=data["game_id"],
                added_at=date.fromisoformat(
                    data.get(
                        "purchase_date",
                        date.today().isoformat()
                    )
                )
            )

            db.session.add(entry)
            db.session.commit()

            return jsonify({
                "msg": "Dodano u biblioteku"
            })

        except Exception as e:

            db.session.rollback()

            return jsonify({
                "error": str(e)
            }), 500

    # GET
    entries = Library.query.all()

    return jsonify([

        {
            "id": e.id,

            "user_id": e.user_id,
            "username": e.user.username,

            "game_id": e.game_id,
            "game_title": e.game.title,

            "purchase_date": e.added_at.isoformat()
        }

        for e in entries
    ])

@app.route(
    "/library/<int:library_id>",
    methods=["GET", "PUT", "DELETE"]
)
def handle_library_item(library_id):

    entry = Library.query.get_or_404(library_id)

    # GET
    if request.method == "GET":

        return jsonify({

            "id": entry.id,

            "user_id": entry.user_id,
            "username": entry.user.username,

            "game_id": entry.game_id,
            "game_title": entry.game.title,

            "purchase_date": entry.added_at.isoformat()
        })

    # PUT
    if request.method == "PUT":

        data = request.get_json()

        entry.user_id = data.get(
            "user_id",
            entry.user_id
        )

        entry.game_id = data.get(
            "game_id",
            entry.game_id
        )

        if data.get("purchase_date"):

            entry.added_at = date.fromisoformat(
                data["purchase_date"]
            )

        db.session.commit()

        return jsonify({
            "msg": "Biblioteka ažurirana"
        })

    # DELETE
    if request.method == "DELETE":

        db.session.delete(entry)
        db.session.commit()

        return jsonify({
            "msg": "Uklonjeno iz biblioteke"
        })
    return None


# =========================================================
# REVIEWS
# =========================================================

@app.route("/reviews", methods=["GET", "POST"])
def handle_reviews():

    # POST
    if request.method == "POST":

        data = request.get_json()

        if data["rating"] < 1 or data["rating"] > 10:

            return jsonify({
                "error": "Ocjena mora biti između 1 i 10"
            }), 400

        try:

            rev = Review(
                user_id=data["user_id"],
                game_id=data["game_id"],
                rating=data["rating"],
                comment=data.get("comment")
            )

            db.session.add(rev)
            db.session.commit()

            return jsonify({
                "msg": "Recenzija dodana"
            })

        except Exception as e:

            db.session.rollback()

            return jsonify({
                "error": str(e)
            }), 500

    # GET
    reviews = Review.query.all()

    return jsonify([

        {
            "id": r.id,

            "user_id": r.user_id,
            "username": r.user.username,

            "game_id": r.game_id,
            "game_title": r.game.title,

            "rating": r.rating,
            "comment": r.comment
        }

        for r in reviews
    ])

# =========================================================
# SINGLE REVIEW
# =========================================================

@app.route(
    "/reviews/<int:review_id>",
    methods=["GET", "PUT", "DELETE"]
)
def handle_review(review_id):

    review = Review.query.get_or_404(review_id)

    # GET
    if request.method == "GET":

        return jsonify({
            "id": review.id,
            "user_id": review.user_id,
            "username": review.user.username,
            "game_id": review.game_id,
            "game_title": review.game.title,
            "rating": review.rating,
            "comment": review.comment,
            "created_at": review.created_at.isoformat()
        })

    # PUT
    if request.method == "PUT":

        data = request.get_json()

        if data.get("rating"):

            if data["rating"] < 1 or data["rating"] > 10:

                return jsonify({
                    "error": "Ocjena mora biti između 1 i 10"
                }), 400

        review.user_id = data.get(
            "user_id",
            review.user_id
        )

        review.game_id = data.get(
            "game_id",
            review.game_id
        )

        review.rating = data.get(
            "rating",
            review.rating
        )

        review.comment = data.get(
            "comment",
            review.comment
        )

        db.session.commit()

        return jsonify({
            "msg": "Recenzija ažurirana"
        })

    # DELETE
    if request.method == "DELETE":

        db.session.delete(review)
        db.session.commit()

        return jsonify({
            "msg": "Recenzija obrisana"
        })
    return None


# =========================================================
# RUN APP
# =========================================================

if __name__ == "__main__":

    app.run(debug=True)