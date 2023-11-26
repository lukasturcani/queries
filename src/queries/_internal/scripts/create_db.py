import argparse
import sqlite3
from pathlib import Path


def main() -> None:
    args = _parse_args()
    connection = sqlite3.connect(args.database)
    connection.execute(
        """
CREATE TABLE IF NOT EXISTS
boards (
    name TEXT PRIMARY KEY NOT NULL
);

CREATE TABLE IF NOT EXISTS
tasks (
    id INTEGER PRIMARY KEY NOT NULL,
    title TEXT NOT NULL,
    board_name TEXT NOT NULL,
    FOREIGN KEY (board_name) REFERENCES boards (name)
);

CREATE TABLE IF NOT EXISTS
users (
    id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS
task_assignments (
    id INTEGER PRIMARY KEY NOT NULL,
    task_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks (id),
    FOREIGN KEY (user_id) REFERENCES users (id),
    UNIQUE (task_id, user_id)
);
"""
    )
    connection.executemany(
        "INSERT INTO boards (name) VALUES (?)",
        [(f"board-{i}",) for i in range(args.num_boards)],
    )
    connection.commit()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "database",
        type=Path,
        help="Path to the database file",
    )
    parser.add_argument(
        "--num-boards",
        type=int,
        default=1_000,
    )
    return parser.parse_args()
