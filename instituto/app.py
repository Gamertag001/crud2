from flask import Flask, render_template, request, redirect, url_for
from db import get_connection

app = Flask(__name__)


@app.route('/cursos')
def lista_cursos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.id, c.nombre, c.descripcion, COUNT(e.id) as total
        FROM cursos c
        LEFT JOIN estudiantes e ON c.id = e.curso_id
        GROUP BY c.id
    """)
    cursos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('cursos.html', cursos=cursos)

@app.route('/cursos/agregar', methods=['GET','POST'])
def agregar_curso():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cursos (nombre, descripcion) VALUES (%s, %s)", (nombre, descripcion))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('lista_cursos'))
    return render_template('curso_form.html', curso=None)

@app.route('/cursos/editar/<int:id>', methods=['GET','POST'])
def editar_curso(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        cursor.execute("UPDATE cursos SET nombre=%s, descripcion=%s WHERE id=%s", (nombre, descripcion, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('lista_cursos'))

    cursor.execute("SELECT * FROM cursos WHERE id=%s", (id,))
    curso = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('curso_form.html', curso=curso)

@app.route('/cursos/eliminar/<int:id>')
def eliminar_curso(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cursos WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('lista_cursos'))


@app.route('/estudiantes')
def lista_estudiantes():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT e.id, e.nombre, e.email, c.nombre as curso
        FROM estudiantes e
        LEFT JOIN cursos c ON e.curso_id = c.id
    """)
    estudiantes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('estudiantes.html', estudiantes=estudiantes)

@app.route('/estudiantes/agregar', methods=['GET','POST'])
def agregar_estudiante():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cursos")
    cursos = cursor.fetchall()

    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        curso_id = request.form['curso_id']
        cursor2 = conn.cursor()
        cursor2.execute("INSERT INTO estudiantes (nombre, email, curso_id) VALUES (%s,%s,%s)", (nombre, email, curso_id))
        conn.commit()
        cursor2.close()
        conn.close()
        return redirect(url_for('lista_estudiantes'))

    cursor.close()
    conn.close()
    return render_template('estudiante_form.html', estudiante=None, cursos=cursos)

@app.route('/estudiantes/editar/<int:id>', methods=['GET','POST'])
def editar_estudiante(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cursos")
    cursos = cursor.fetchall()

    cursor.execute("SELECT * FROM estudiantes WHERE id=%s", (id,))
    estudiante = cursor.fetchone()

    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        curso_id = request.form['curso_id']
        cursor2 = conn.cursor()
        cursor2.execute("UPDATE estudiantes SET nombre=%s, email=%s, curso_id=%s WHERE id=%s", (nombre, email, curso_id, id))
        conn.commit()
        cursor2.close()
        conn.close()
        return redirect(url_for('lista_estudiantes'))

    cursor.close()
    conn.close()
    return render_template('estudiante_form.html', estudiante=estudiante, cursos=cursos)

@app.route('/estudiantes/eliminar/<int:id>')
def eliminar_estudiante(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM estudiantes WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('lista_estudiantes'))


@app.route('/')
def inicio():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)