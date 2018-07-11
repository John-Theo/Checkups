import sqlite3

conn = sqlite3.connect('../db/classification.db')
c = conn.cursor()

c.execute("""CREATE TABLE result (
            file_name text,
            label text,
            IMG_report float,
            IMG_paper_n_report float,
            IMG_n_paper float,
            TXT_report float,
            TXT_paper_n_report float,
            TXT_n_paper float
        )""")

# tuples = [
#     ('0.jpg', 0.580, 0.53, 0.56),
#     ('1.jpg', 0.580, 0.53, 0.56),
#     ('2.jpg', 0.580, 0.53, 0.56),
#     ('3.jpg', 0.580, 0.53, 0.56)
# ]
#
# for atuple in tuples:
#     c.execute("INSERT INTO test_db VALUES (?, ?, ?, ?)", atuple)
#     conn.commit()
#
# c.execute("SELECT * FROM test_db WHERE a=0.580")
#
# print(c.fetchall())

conn.commit()
conn.close()
