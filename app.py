from flask import Flask, render_template, request, redirect , url_for, flash
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'productos'
mysql = MySQL(app)


app.secret_key = "mysecretkey"

@app.route("/")
def index():
    con = mysql.connection.cursor()
    con.execute("SELECT * FROM productos")
    dat = con.fetchall()
    return render_template("agregar.html", productos = dat)


@app.route("/agregar", methods=["POST"])
def agregar():
    if request.method == "POST": 
        nombre = request.form["nombre"]
        precio = request.form["precio"]
        es_valido = True
        if nombre == "":
            es_valido = False
            flash("pone el nombre")
        if precio == "":
            es_valido = False
            flash("y precio, o no pasas")
        if not precio.isdigit():
            es_valido = False

        if es_valido == False:
            return render_template("agregar.html", nombre=nombre, precio=precio)

        con = mysql.connection.cursor()
        con.execute("INSERT INTO productos (nombre, precio) VALUES (%s,%s)",(nombre,precio))
        mysql.connection.commit()
        flash("Nuevo Producto Agregado a la Lista")
        return redirect(url_for("index"))

@app.route("/eliminar/<string:id>")
def eliminar(id):
    con = mysql.connection.cursor()
    con.execute('DELETE FROM productos WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('producto eliminado')
    return redirect(url_for('index'))

@app.route("/editar/<id>")
def editar(id):
        con = mysql.connection.cursor()
        con.execute('SELECT * FROM productos WHERE id = %s', (id,))
        dat = con.fetchall()
        return render_template('actualizar.html', productos = dat[0])

@app.route('/actualizar/<id>', methods=["POST"])
def actualizar(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        con = mysql.connection.cursor()
        con.execute("""
            UPDATE productos
            SET nombre = %s,
                precio = %s
            WHERE id = %s
        """, (nombre, precio, id))
        mysql.connection.commit()
        flash('productos actualizados')
        return redirect(url_for('index'))

if __name__ =='__main__':
    app.run(port = 3000, debug = True)
