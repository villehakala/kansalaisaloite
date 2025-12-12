import db

def get_initiatives():
    sql = """SELECT i.id, i.title, COUNT(c.id) total_comments, i.votes total_votes, MAX(c.created_at) last
             FROM initiatives i, comments c
             WHERE i.id = c.initiative_id
             GROUP BY i.id
             ORDER BY i.id DESC"""
    return db.query(sql)

def get_initiative(initiative_id):
    sql = "SELECT id, title FROM initiatives WHERE id = ?"
    result = db.query(sql, [initiative_id])
    return result[0] if result else None

def search(query):
    sql = """SELECT c.id comment_id,
                    c.initiative_id,
                    i.title initiative_title,
                    c.created_at,
                    u.username
             FROM initiatives i, comments c, users u
             WHERE i.id = c.initiative_id AND
                   u.id = c.user_id AND
                   (c.content LIKE ? or i.title LIKE ?)
             ORDER BY c.created_at DESC"""
    return db.query(sql, ["%" + query + "%", "%" + query + "%"])


def get_comments(initiative_id):
    sql = """SELECT c.id, c.content, c.created_at, c.user_id, u.username
             FROM comments c, users u
             WHERE c.user_id = u.id AND c.initiative_id = ?
             ORDER BY c.id"""
    return db.query(sql, [initiative_id])

def get_comment(comment_id):
    sql = "SELECT id, content, user_id, initiative_id FROM comments WHERE id = ?"
    result = db.query(sql, [comment_id])
    return result[0] if result else None


def get_votes(initiative_id):
    sql = "SELECT votes FROM initiatives WHERE id = ?"
    result = db.query(sql, [initiative_id])
    return result[0]["votes"] if result else 0

def add_initiative(title, content, user_id):
    sql = "INSERT INTO initiatives (title, user_id) VALUES (?, ?)"
    db.execute(sql, [title, user_id])

    initiative_id = db.last_insert_id()
    add_comment(content, user_id, initiative_id)
    return initiative_id


def add_vote(user_id, initiative_id):
    
    sql = """INSERT INTO initiative_votes (user_id, initiative_id)
                    VALUES (?, ?)"""
    db.execute(sql, [user_id, initiative_id])

    sql = """UPDATE initiatives
             SET votes = votes + 1
             WHERE id = ?"""
    db.execute(sql, [initiative_id])


def has_voted(user_id, initiative_id):
    sql = "SELECT 1 FROM initiative_votes WHERE user_id = ? AND initiative_id = ?"
    result = db.query(sql, [user_id, initiative_id])
    return bool(result)


def add_comment(content, user_id, initiative_id):
    sql = """INSERT INTO comments (content, created_at, user_id, initiative_id) VALUES
             (?, datetime('now', 'localtime'), ?, ?)"""
    db.execute(sql, [content, user_id, initiative_id])

def update_comment(comment_id, content):
    sql = "UPDATE comments SET content = ? WHERE id = ?"
    db.execute(sql, [content, comment_id])

def remove_comment(comment_id):
    sql = "DELETE FROM comments WHERE id = ?"
    db.execute(sql, [comment_id])

def add_hashtags(initiative_id, content, selected_tags=None):
    initiative_id = int(initiative_id)
    hashtags = []
    words = content.split()

    for word in words:
        if word.startswith('#') and len(word) > 1:
            hashtag = word.strip().lower().lstrip('#')
            hashtags.append(hashtag)
    
    if selected_tags:
        for tag in selected_tags:
            if not tag:
                continue
            hashtag = str(tag).strip().lower().lstrip('#')
            hashtags.append(hashtag)

    
    for hashtag in hashtags:
        if not hashtag:
            continue

        db.execute("INSERT OR IGNORE INTO hashtags (name) VALUES (?)", [hashtag])
        row = db.query("SELECT id FROM hashtags WHERE name = ?", [hashtag])
        hashtag_id = row[0]["id"]
        print(initiative_id, hashtag_id)
        db.execute("""INSERT OR IGNORE INTO initiative_hashtags (initiative_id, hashtag_id)
                      VALUES (?, ?)""", [initiative_id, hashtag_id])

def get_hashtags(initiative_id):
    sql = """
        SELECT h.id AS id, h.name AS name
        FROM initiative_hashtags ih, hashtags h
        WHERE ih.hashtag_id = h.id
          AND ih.initiative_id = ?
        ORDER BY h.name ASC
    """
    result = db.query(sql, [initiative_id])
    return result
