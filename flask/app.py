# importar el framework Flask
import re
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# ininicaliza variable para usar Flask
app = Flask(__name__)

# conexion con la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_db'

# setting
app.secret_key = 'mysecretkey'

#preparar la conexion con la base de datos
mysql = MySQL(app)

# crear una ruta para la raiz de la aplicacion
@app.route('/')
def index():
    # consultar todo de la bd de la tabla tb_albums
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tb_albums")
    data = cur.fetchall()
    return render_template('index.html', albums = data)

@app.route('/agregar')
def agregar():
    return render_template('agregarAlbum.html')

@app.route('/nuevoAlbum', methods=['POST'])
def agregarAlbum():
    if(request.method == 'POST'):
        album = request.form['album']
        artista = request.form['artista']
        anio = request.form['anio']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tb_albums (album, artista, anio) VALUES (%s, %s, %s)", (album, artista, anio))
        mysql.connection.commit()
        cur.close()
        flash('Album agregado correctamente', 'success')
        return redirect(url_for('index'))

@app.route('/editar/<id>')
def editar(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tb_albums WHERE id = %s", [id])
    data = cur.fetchall()
    return render_template('editarAlbum.html', album = data[0])

@app.route('/editarAlbum/<id>', methods=['POST'])
def editarAlbum(id):
    if(request.method == 'POST'):
        album = request.form['album']
        artista = request.form['artista']
        anio = request.form['anio']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE tb_albums SET album = %s, artista = %s, anio = %s WHERE id = %s", (album, artista, anio, id))
        mysql.connection.commit()
        cur.close()
        flash('Album editado correctamente', 'success')
        return redirect(url_for('index'))


@app.route('/eliminar/<id>')
def eliminar(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tb_albums WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash('Album eliminado correctamente', 'info') 
    return redirect(url_for('index'))

# iniciar servidor
if __name__ == '__main__':
    app.run(port = 3000, debug = True)
    