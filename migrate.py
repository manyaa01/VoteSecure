"""
Run this once to migrate existing CSV data into the SQLite database.
    python migrate.py
"""
import sqlite3
import hashlib
import pandas as pd
from pathlib import Path

DB_PATH = Path("database") / "votesecure.db"

def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

def migrate():
    import dframe  # ensures tables are created

    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()

        # Migrate voters
        voters = pd.read_csv(Path("database") / "voterList.csv")
        for _, row in voters.iterrows():
            c.execute("SELECT 1 FROM voters WHERE voter_id=?", (int(row["voter_id"]),))
            if c.fetchone() is None:
                c.execute(
                    "INSERT INTO voters VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        int(row["voter_id"]),
                        row["Name"],
                        row["Gender"],
                        0,  # age unknown from old CSV, defaulting to 0
                        row["Zone"],
                        row["City"],
                        hash_password(str(row["Passw"])),
                        int(row["hasVoted"]),
                    ),
                )
                print(f"Migrated voter: {row['voter_id']} - {row['Name']}")

        # Migrate vote counts
        cands = pd.read_csv(Path("database") / "cand_list.csv")
        for _, row in cands.iterrows():
            c.execute(
                "UPDATE candidates SET vote_count=? WHERE sign=?",
                (int(row["Vote Count"]), row["Sign"]),
            )
            print(f"Updated votes for: {row['Sign']} = {row['Vote Count']}")

        conn.commit()
    print("\nMigration complete!")

if __name__ == "__main__":
    migrate()
