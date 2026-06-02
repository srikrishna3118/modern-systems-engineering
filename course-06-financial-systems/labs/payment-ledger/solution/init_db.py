from __future__ import annotations

import argparse

from db import connect


SCHEMA = """
CREATE TABLE IF NOT EXISTS transactions (
  tx_id TEXT PRIMARY KEY,
  idempotency_key TEXT NOT NULL UNIQUE,
  from_account TEXT NOT NULL,
  to_account TEXT NOT NULL,
  amount INTEGER NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS entries (
  entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
  tx_id TEXT NOT NULL,
  account TEXT NOT NULL,
  delta INTEGER NOT NULL,
  created_at TEXT NOT NULL,
  FOREIGN KEY (tx_id) REFERENCES transactions(tx_id)
);

CREATE TABLE IF NOT EXISTS audit_log (
  audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
  tx_id TEXT NOT NULL,
  event TEXT NOT NULL,
  created_at TEXT NOT NULL,
  FOREIGN KEY (tx_id) REFERENCES transactions(tx_id)
);
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="ledger.db")
    args = parser.parse_args()

    conn = connect(args.db)
    conn.executescript(SCHEMA)
    print(f"initialized DB: {args.db}")


if __name__ == "__main__":
    main()
