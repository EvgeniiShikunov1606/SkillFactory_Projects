import sqlite3

# Создаем и подключаемся к базе данных
conn = sqlite3.connect('taylor_swift_reputation.db')
cursor = conn.cursor()

# Создаем таблицу для песен
cursor.execute('''
CREATE TABLE IF NOT EXISTS songs (
    track_number INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    duration TEXT NOT NULL
)
''')

# Список песен с номером и длительностью
songs = [
    (1, '...Ready for It?', '3:28'),
    (2, 'End Game', '4:04'),
    (3, 'I Did Something Bad', '3:58'),
    (4, 'Don’t Blame Me', '3:56'),
    (5, 'Delicate', '3:52'),
    (6, 'Look What You Made Me Do', '3:31'),
    (7, 'So It Goes...', '3:47'),
    (8, 'Gorgeous', '3:29'),
    (9, 'Getaway Car', '3:54'),
    (10, 'King of My Heart', '3:34'),
    (11, 'Dancing with Our Hands Tied', '3:31'),
    (12, 'Dress', '3:50'),
    (13, 'This Is Why We Can’t Have Nice Things', '3:27'),
    (14, 'Call It What You Want', '3:23'),
    (15, 'New Year’s Day', '3:55')
]

# Вставляем данные в таблицу
cursor.executemany('INSERT INTO songs (track_number, title, duration) VALUES (?, ?, ?)', songs)

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()
