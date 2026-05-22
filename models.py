from extensions import db
from datetime import date, datetime


# =========================================================
# FUNKCIJA ZA PRETVARANJE DATUMA U STRING
# =========================================================

def safe_isoformat(dt):

    # Ako je vrijednost prazna -> vrati None
    if dt is None:
        return None

    # Provjerava da li je objekat date ili datetime
    if isinstance(dt, (date, datetime)):

        # Pretvara datum u ISO format
        # primjer: 2026-05-14T18:30:00
        return dt.isoformat()

    # Ako je već string -> samo ga vrati
    return str(dt)


# =========================================================
# USER MODEL
# =========================================================

class User(db.Model):

    # Naziv tabele u bazi
    __tablename__ = "users"

    # Primarni ključ
    # SQL automatski povećava ID
    id = db.Column(db.Integer, primary_key=True)

    # Korisničko ime
    # max 50 karaktera
    # nullable=False -> mora imati vrijednost
    # index=True -> brža pretraga u bazi
    username = db.Column(
        db.String(50),
        nullable=False,
        index=True
    )

    # Email korisnika
    # unique=True -> ne mogu postojati 2 ista emaila
    email = db.Column(
        db.String(100),
        nullable=False,
        unique=True,
        index=True
    )

    # Datum kreiranja korisnika
    # db.func.now() -> trenutno vrijeme iz baze
    created_at = db.Column(
        db.DateTime,
        default=db.func.now()
    )

    # Datum zadnje izmjene
    # onupdate -> automatski update pri promjeni podataka
    updated_at = db.Column(
        db.DateTime,
        default=db.func.now(),
        onupdate=db.func.now()
    )

    # =====================================================
    # RELACIJA PREMA LIBRARY MODELU
    # =====================================================

    # Jedan korisnik može imati više igara
    # u svojoj biblioteci
    libraries = db.relationship(
        "Library",

        # Povezuje relaciju sa atributom "user"
        # iz Library modela
        back_populates="user",

        # Ako se obriše korisnik
        # brišu se i povezani podaci
        cascade="all, delete-orphan"
    )

    # =====================================================
    # RELACIJA PREMA REVIEW MODELU
    # =====================================================

    # Jedan korisnik može imati više recenzija
    reviews = db.relationship(
        "Review",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # =====================================================
    # PRETVARANJE OBJEKTA U DICTIONARY
    # =====================================================

    def to_dict(self):

        # self predstavlja trenutni objekat
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,

            # Pretvaranje datuma u string
            "created_at": safe_isoformat(self.created_at),
            "updated_at": safe_isoformat(self.updated_at)
        }


# =========================================================
# GAME MODEL
# =========================================================

class Game(db.Model):

    # Naziv tabele
    __tablename__ = "games"

    # Primarni ključ
    id = db.Column(db.Integer, primary_key=True)

    # Naziv igre
    title = db.Column(
        db.String(100),
        nullable=False,
        index=True
    )

    # Žanr igre
    genre = db.Column(
        db.String(50),
        index=True
    )

    # Godina izlaska igre
    release_year = db.Column(db.Integer)

    # Datum kreiranja
    created_at = db.Column(
        db.DateTime,
        default=db.func.now()
    )

    # Datum zadnje izmjene
    updated_at = db.Column(
        db.DateTime,
        default=db.func.now(),
        onupdate=db.func.now()
    )

    # =====================================================
    # RELACIJA SA LIBRARY
    # =====================================================

    # Jedna igra može biti kod više korisnika
    libraries = db.relationship(
        "Library",
        back_populates="game",
        cascade="all, delete-orphan"
    )

    # =====================================================
    # RELACIJA SA REVIEW
    # =====================================================

    # Jedna igra može imati više recenzija
    reviews = db.relationship(
        "Review",
        back_populates="game",
        cascade="all, delete-orphan"
    )

    # =====================================================
    # SERIALIZACIJA
    # =====================================================

    def to_dict(self):

        return {
            "id": self.id,
            "title": self.title,
            "genre": self.genre,
            "release_year": self.release_year,
            "created_at": safe_isoformat(self.created_at),
            "updated_at": safe_isoformat(self.updated_at)
        }


# =========================================================
# LIBRARY MODEL
# =========================================================

# OVA TABELA POVEZUJE:
# USER <-> GAME
#
# Jedan korisnik može imati više igara
# Jedna igra može pripadati više korisnika
#
# Ovo je MANY TO MANY relacija

class Library(db.Model):

    # Naziv tabele
    __tablename__ = "libraries"

    # Primarni ključ
    id = db.Column(db.Integer, primary_key=True)

    # =====================================================
    # STRANI KLJUČ PREMA USERS TABELI
    # =====================================================

    user_id = db.Column(

        # Integer vrijednost
        db.Integer,

        # ForeignKey povezuje ovu tabelu
        # sa users.id
        db.ForeignKey(
            "users.id",

            # Ako se obriše korisnik
            # brišu se i njegovi library podaci
            ondelete="CASCADE"
        ),

        nullable=False,
        index=True
    )

    # =====================================================
    # STRANI KLJUČ PREMA GAMES TABELI
    # =====================================================

    game_id = db.Column(
        db.Integer,

        db.ForeignKey(
            "games.id",
            ondelete="CASCADE"
        ),

        nullable=False,
        index=True
    )

    # Datum kada je igra dodana u biblioteku
    added_at = db.Column(
        db.Date,

        # Automatski postavlja današnji datum
        default=date.today,

        nullable=False
    )

    # =====================================================
    # RELACIJA PREMA USER MODELU
    # =====================================================

    # Svaki library zapis pripada jednom korisniku
    user = db.relationship(
        "User",
        back_populates="libraries"
    )

    # =====================================================
    # RELACIJA PREMA GAME MODELU
    # =====================================================

    # Svaki library zapis pripada jednoj igri
    game = db.relationship(
        "Game",
        back_populates="libraries"
    )

    # =====================================================
    # UNIQUE CONSTRAINT
    # =====================================================

    # Sprječava da korisnik doda
    # istu igru više puta
    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "game_id",
            name="unique_user_game"
        ),
    )

    # =====================================================
    # SERIALIZACIJA
    # =====================================================

    def to_dict(self):

        return {
            "id": self.id,
            "user_id": self.user_id,
            "game_id": self.game_id,
            "added_at": safe_isoformat(self.added_at)
        }


# =========================================================
# REVIEW MODEL
# =========================================================

class Review(db.Model):

    # Naziv tabele
    __tablename__ = "reviews"

    # Primarni ključ
    id = db.Column(db.Integer, primary_key=True)

    # =====================================================
    # FOREIGN KEY -> USER
    # =====================================================

    user_id = db.Column(
        db.Integer,

        db.ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),

        nullable=False,
        index=True
    )

    # =====================================================
    # FOREIGN KEY -> GAME
    # =====================================================

    game_id = db.Column(
        db.Integer,

        db.ForeignKey(
            "games.id",
            ondelete="CASCADE"
        ),

        nullable=False,
        index=True
    )

    # =====================================================
    # OCJENA IGRE
    # =====================================================

    # Korisnik daje ocjenu od 1 do 10
    rating = db.Column(
        db.Integer,
        nullable=False
    )

    # Tekst komentara
    comment = db.Column(db.Text)

    # Datum kreiranja recenzije
    created_at = db.Column(
        db.DateTime,
        default=db.func.now()
    )

    # =====================================================
    # VALIDACIJA RATINGA
    # =====================================================

    # Ne dozvoljava:
    # rating < 1
    # rating > 10
    __table_args__ = (
        db.CheckConstraint(
            "rating >= 1 AND rating <= 10"
        ),
    )

    # =====================================================
    # RELACIJA SA USER
    # =====================================================

    # Recenzija pripada jednom korisniku
    user = db.relationship(
        "User",
        back_populates="reviews"
    )

    # =====================================================
    # RELACIJA SA GAME
    # =====================================================

    # Recenzija pripada jednoj igri
    game = db.relationship(
        "Game",
        back_populates="reviews"
    )

    # =====================================================
    # SERIALIZACIJA
    # =====================================================

    def to_dict(self):

        return {
            "id": self.id,
            "user_id": self.user_id,
            "game_id": self.game_id,
            "rating": self.rating,
            "comment": self.comment,
            "created_at": safe_isoformat(self.created_at)
        }