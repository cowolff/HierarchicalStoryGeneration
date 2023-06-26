import sqlite3

class Data():
    def __init__(self, db_file="data.db") -> None:
        self.conn = sqlite3.connect(db_file)
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS result(prompt text PRIMARY KEY, result text, timestamp integer)")
        cursor.close()
        self.conn.commit()

    def addResult(self, prompt: str, output: str, timestamp: int) -> None:
        cursor = self.conn.cursor()
        prompt = prompt.replace('"', "'")
        prompt = prompt.replace("!", ".")
        
        output = output.replace('"', "'")
        output = output.replace("!", ".")
        try:
            cursor.execute('INSERT INTO result VALUES("{}", "{}", {});'.format(prompt, output, timestamp))
            cursor.close()
            self.conn.commit()
        except sqlite3.Error as e:
            cursor.execute('UPDATE result SET timestamp={} WHERE prompt="{}";'.format(timestamp, prompt))
            cursor.close()
            self.conn.commit()

    def getResults(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM result")
        results = cursor.fetchall()
        results = [{"prompt":x[0], "result":x[1], "timestamp":x[2]} for x in results]
        cursor.close()
        return results

    def deleteResult(self):
        pass