import sqlite3


class SegmentTrackerSQL:
    def __init__(self, db_name="/app/tested_segments.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS segments (
                segment TEXT PRIMARY KEY,
                status TEXT
            )
        """
        )
        self.conn.commit()

    def add_segment(self, segment, status):
        try:
            self.cursor.execute(
                "INSERT INTO segments (segment, status) VALUES (?, ?)",
                (segment, status),
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass

    def is_segment_tested(self, segment):
        self.cursor.execute("SELECT 1 FROM segments WHERE segment = ?", (segment,))
        return self.cursor.fetchone() is not None

    def close(self):
        self.conn.close()
