import db

def get_initiatives():
    sql = """SELECT i.id, i.title, COUNT(c.id) total, MAX(c.created_at) last
             FROM initiatives i, comments c
             WHERE i.id = c.initiative_id
             GROUP BY i.id
             ORDER BY i.id DESC"""
    return db.query(sql)

def get_initiative(initiative_id):
    sql = "SELECT id, title FROM initiatives WHERE id = ?"
    return db.query(sql, [initiative_id])[0]

def get_comments(initiative_id):
    sql = """SELECT c.id, c.content, c.created_at, c.user_id, u.username
             FROM comments c, users u
             WHERE c.user_id = u.id AND c.initiative_id = ?
             ORDER BY c.id"""
    return db.query(sql, [initiative_id])

def get_comment(comment_id):
    sql = "SELECT id, content, user_id, initiative_id FROM comments WHERE id = ?"
    return db.query(sql, [comment_id])[0]

def add_initiative(title, content, user_id):
    sql = "INSERT INTO initiatives (title, user_id) VALUES (?, ?)"
    db.execute(sql, [title, user_id])
    initiative_id = db.last_insert_id()
    add_comment(content, user_id, initiative_id)
    return initiative_id

def add_comment(content, user_id, initiative_id):
    sql = """INSERT INTO comments (content, created_at, user_id, initiative_id) VALUES
             (?, datetime('now'), ?, ?)"""
    db.execute(sql, [content, user_id, initiative_id])

def update_comment(comment_id, content):
    sql = "UPDATE comments SET content = ? WHERE id = ?"
    db.execute(sql, [content, comment_id])

def remove_comment(comment_id):
    sql = "DELETE FROM comments WHERE id = ?"
    db.execute(sql, [comment_id])