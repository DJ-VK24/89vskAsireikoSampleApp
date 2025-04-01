import sys, datetime, bcrypt, os
sys.path.append('C:\\sample_app')

from flask import Flask, render_template, session, request, redirect, url_for
from app.connect import DB

app = Flask(__name__)
app.secret_key = os.urandom(24).hex()

@app.route('/v1/home', methods=['GET'])
def home():
    user = session.get('user')
    return render_template('home.html', usr=user)


@app.route('/v1/signin', methods=['GET', 'POST'])
def login():
    match request.method:
        case 'GET':
            user = session.get('user')
            if user:
                return redirect(url_for('home'))
            else:
                return render_template('login.html', err=False)
        case 'POST':
            db = DB()
            filter = "email = '{}'".format(request.form['email'])
            db_user = db.select('users', filter)
            db.conn.close()
            if db_user:
                if bcrypt.checkpw(str.encode(request.form['password']), str.encode(db_user[0][4])):
                    user = {
                        'id': db_user[0][0],
                        'name': db_user[0][2],
                        'surname': db_user[0][3],
                        'email': db_user[0][1],
                        'role': db_user[0][5]
                    }
                    session['user'] = user
                    return redirect(url_for('home'))
            return render_template('login.html', err=True)


@app.route('/v1/signup', methods=['GET', 'POST'])
def register():
    match request.method:
        case 'GET':
            return render_template('register.html', usr='', err=False)
        case 'POST':
            db = DB()
            salt = bcrypt.gensalt()
            pwd = bcrypt.hashpw(str.encode(request.form['password']), salt)
            values = "'{}','{}','{}','{}','{}'".format(
                request.form['email'],
                request.form['name'],
                request.form['surname'],
                pwd.decode('utf-8'),
                datetime.datetime.now()
            )
            inserted = db.insert_user('users', values)
            db.conn.commit()
            db.conn.close()

            if inserted:
                user = {
                    'id': inserted.lastrowid,
                    'name': request.form['name'],
                    'surname': request.form['surname'],
                    'email': request.form['email'],
                    'role': 'user'
                }
                session['user'] = user
                return redirect(url_for('home'))
            else:
                return render_template('register.html', usr='', err=True)


@app.route('/v1/signout', methods=['GET'])
def logout():
    session.pop('user')
    return redirect(url_for('home'))


@app.route('/v1/notes', methods=['GET', 'POST'])
def notes():
    user = session.get('user')
    if not user:
        return redirect(url_for('home'))
    match request.method:
        case 'GET':
            db = DB()
            filter = "user_id = '{}'".format(user['id'])
            notes = db.select('notes', filter)
            return render_template('note.html', usr=user, items=notes)
        case 'POST':
            db = DB()
            values = "'{}','{}','{}'".format(
                request.form['text'],
                user['id'],
                datetime.datetime.now()
            )
            inserted = db.insert_note('notes', values)
            db.conn.commit()
            db.conn.close()
            if inserted:
                return redirect(url_for('notes'))
            return render_template('note.html', usr=user, err=True)


@app.route('/v1/notes/<note_id>', methods=['POST'])
def share_note(note_id):
    user = session.get('user')
    if not user:
        return redirect(url_for('home'))
    db = DB()
    filter = "email = '{}'".format(request.form['share_to'])
    share_to = db.select('users', filter)
    values = "'{}','{}','{}'".format(
        share_to[0][0],
        note_id,
        datetime.datetime.now()
    )
    inserted = db.insert_shared_note('shared_notes', values)
    db.conn.commit()
    db.conn.close()
    return redirect(url_for('notes'))


@app.route('/v1/tasks', methods=['GET', 'POST'])
def tasks():
    user = session.get('user')
    if not user:
        return redirect(url_for('home'))
    match request.method:
        case 'GET':
            db = DB()
            filter = "user_id = '{}'".format(user['id'])
            tasks = db.select('tasks', filter)
            subtasks = db.select('subtasks', '')
            return render_template('todo.html', usr=user, items=tasks, subitems=subtasks)
        case 'POST':
            db = DB()
            values = "'{}','{}','{}'".format(
                request.form['todo_name'],
                user['id'],
                datetime.datetime.now()
            )
            inserted = db.insert_task('tasks', values)
            db.conn.commit()
            db.conn.close()
            if inserted:
                return redirect(url_for('tasks'))
            return render_template('todo.html', usr=user, err=True)
        

@app.route('/v1/tasks/<task_id>', methods=['GET'])
def remove_task(task_id):
    user = session.get('user')
    if not user:
        return redirect(url_for('home'))
    db = DB()
    filter = "task_id = '{}'".format(task_id)
    del_subtask = db.delete('subtasks', filter)
    filter = "id = '{}'".format(task_id)
    del_task = db.delete('tasks', filter)
    db.conn.commit()
    db.conn.close()
    return redirect(url_for('tasks'))


@app.route('/v1/subtask/<task_id>', methods=['POST'])
def subtasks(task_id):
    user = session.get('user')
    if not user:
        return redirect(url_for('home'))
    db = DB()
    values = "'{}','{}','{}','{}'".format(
        request.form['subtask'],
        task_id,
        0,
        datetime.datetime.now()
    )
    inserted = db.insert_subtask('subtasks', values)
    db.conn.commit()
    db.conn.close()
    if inserted:
        return redirect(url_for('tasks'))
    return render_template('todo.html', usr=user, err=True)


@app.route('/v1/sharednotes', methods=['GET'])
def shared_notes():
    user = session.get('user')
    if not user:
        return redirect(url_for('home'))
    
    db = DB()
    filter = "user_id = '{}'".format(user['id'])
    shared_notes = db.select('shared_notes', filter)
    note_ids = [item[1] for item in shared_notes] if shared_notes else []
    if not note_ids:
        return render_template('shared_note.html', usr=user, items=[])
    if len(note_ids) == 1:
        filter = "id = '{}'".format(note_ids[0])
    else:
        filter = "id IN {}".format(tuple(note_ids))

    notes = db.select('notes', filter) or []
    if not isinstance(notes, list):
        notes = []

    updated_notes = []
    for note in notes:
        filter = "id = '{}'".format(note[2])
        author = db.select('users', filter)
        if author:
            new_note = [
                note[0],
                note[1],
                f"{author[0][2]} {author[0][3]}",
                note[3]
            ]
            updated_notes.append(new_note)

    db.conn.commit()
    db.conn.close()

    return render_template('shared_note.html', usr=user, items=updated_notes)



@app.route('/v1/users', methods=['GET'])
def users():
    user = session.get('user')
    if not user:
        return redirect(url_for('home'))
    db = DB()
    users = db.select('users', '')
    return render_template('admin_users.html', usr=user, items=users)
