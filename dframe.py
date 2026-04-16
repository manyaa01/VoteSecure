import sqlite3
import hashlib
from pathlib import Path
from logger import logger

DB_PATH = Path("database") / "votesecure.db"


def get_conn():
    return sqlite3.connect(DB_PATH)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def init_db():
    """Create tables and seed candidate list if not already present."""
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS voters (
                voter_id   INTEGER PRIMARY KEY,
                name       TEXT NOT NULL,
                gender     TEXT NOT NULL,
                age        INTEGER NOT NULL,
                zone       TEXT NOT NULL,
                city       TEXT NOT NULL,
                password   TEXT NOT NULL,
                has_voted  INTEGER NOT NULL DEFAULT 0
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS candidates (
                sign       TEXT PRIMARY KEY,
                name       TEXT NOT NULL,
                vote_count INTEGER NOT NULL DEFAULT 0
            )
        """)
        # Seed candidates only if table is empty
        c.execute("SELECT COUNT(*) FROM candidates")
        if c.fetchone()[0] == 0:
            candidates = [
                ("bjp",  "Narendra Modi",    0),
                ("cong", "Rahul Gandhi",     0),
                ("aap",  "Arvind Kejriwal",  0),
                ("ss",   "Udhav Thakrey",    0),
                ("nota", "NOTA",             0),
            ]
            c.executemany("INSERT INTO candidates VALUES (?, ?, ?)", candidates)
        conn.commit()


def verify(vid, passw):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute(
            "SELECT 1 FROM voters WHERE voter_id=? AND password=?",
            (vid, hash_password(passw))
        )
        return c.fetchone() is not None


def isEligible(vid):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute(
            "SELECT 1 FROM voters WHERE voter_id=? AND has_voted=0",
            (vid,)
        )
        return c.fetchone() is not None


def vote_update(sign, vid):
    with get_conn() as conn:
        c = conn.cursor()
        # Atomically mark voter as voted only if they haven't yet
        c.execute(
            "UPDATE voters SET has_voted=1 WHERE voter_id=? AND has_voted=0",
            (vid,)
        )
        if c.rowcount == 0:
            # Either voter doesn't exist or already voted
            return False
        c.execute(
            "UPDATE candidates SET vote_count = vote_count + 1 WHERE sign=?",
            (sign,)
        )
        conn.commit()
    return True


def show_result():
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("SELECT sign, vote_count FROM candidates")
        return {row[0]: row[1] for row in c.fetchall()}


def taking_data_voter(name, gender, age, zone, city, passw):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("SELECT MAX(voter_id) FROM voters")
        row = c.fetchone()[0]
        vid = 10001 if row is None else row + 1
        c.execute(
            "INSERT INTO voters VALUES (?, ?, ?, ?, ?, ?, ?, 0)",
            (vid, name, gender, age, zone, city, hash_password(passw))
        )
        conn.commit()
    logger.info(f"New voter registered — ID: {vid}, Name: {name}")
    return vid


def count_reset():
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("UPDATE voters SET has_voted=0")
        c.execute("UPDATE candidates SET vote_count=0")
        conn.commit()
    logger.info("Election reset — all votes cleared, all voters re-enabled")


def reset_voter_list():
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM voters")
        conn.commit()


def reset_cand_list():
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("UPDATE candidates SET vote_count=0")
        conn.commit()


# Auto-initialize DB when module is imported
init_db()
