from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL


app = Flask(__name__)


#MYSQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'basedatos'
app.config['MYSQL_DB'] = 'GamesCollector'
mysql = MySQL(app)

#settings
app.secret_key = 'mysecretkey'

#Generamos las rutas que necesitamos
@app.route('/')
def Index():
    cur = mysql.connection.cursor()

    # Obtener todos los juegos
    cur.execute('SELECT * FROM Game')
    games = cur.fetchall()

    # Crear un diccionario para almacenar géneros y plataformas
    game_genres = {}
    game_platforms = {}

    for game in games:
        game_id = game[0]  # Asumiendo que el Id_Game es el primer campo
        cur.execute('SELECT Genre FROM Game_Genre WHERE Id_Game = %s', (game_id,))
        genres = cur.fetchall()
        game_genres[game_id] = [genre[0] for genre in genres]

        cur.execute('SELECT Platform FROM Game_Platform WHERE Id_Game = %s', (game_id,))
        platforms = cur.fetchall()
        game_platforms[game_id] = [platform[0] for platform in platforms]

    return render_template('index.html', games=games, game_genres=game_genres, game_platforms=game_platforms)


@app.route('/add_game_form')
def add_game_form():
    # Lista de plataformas disponibles
    available_genres = ['Action', 'Adventure', 'RPG', 'Simulation', 'Strategy', 'Sports']
    available_platforms = ['PC', 'PS4', 'Xbox', 'Nintendo Switch', 'Mobile']
    return render_template('add_game_form.html', available_genres=available_genres, available_platforms=available_platforms)

@app.route('/add_game', methods=['POST'])
def add_game():
    if request.method == 'POST':
        # Obtener datos del formulario
        Title = request.form['Title']
        Description = request.form['Description']
        Release_Date = request.form['Release_Date']
        Developer = request.form['Developer']
        Publisher = request.form['Publisher']
        Multiplayer = bool(int(request.form['Multiplayer']))  # Convertir a booleano
        State = request.form['State']
        Date_Added = request.form['Date_Added']
        Image_URL = request.form['Image_URL']
        Achievements = bool(int(request.form['Achievements']))  # Convertir a booleano
        Rating = int(request.form['Rating'])  # Convertir a entero
        Review = request.form['Review']
        Time_Played = request.form['Time_Played']
        Add_To = request.form['Add_To']  # Obtener wishlist o library
        user_id = 1  # Usa el ID del usuario actual aquí
        
        # Insertar datos en la base de datos
        cur = mysql.connection.cursor()
        cur.execute('''
            INSERT INTO Game (
                Title, Description, Release_Date, Developer, Publisher, 
                Multiplayer, State, Date_Added, Image_URL, Achievements, 
                Rating, Review, Time_Played
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            Title, Description, Release_Date, Developer, Publisher, 
            Multiplayer, State, Date_Added, Image_URL, Achievements, 
            Rating, Review, Time_Played
        ))

        # Obtener el ID del juego recién insertado
        game_id = cur.lastrowid
        
        # Insertar géneros
        genres = request.form.getlist('Genres')
        for genre in genres:
            cur.execute('''
                INSERT INTO Game_Genre (Id_Game, Genre) VALUES (%s, %s)
            ''', (game_id, genre))

        # Insertar plataformas
        platforms = request.form.getlist('Platforms')
        for platform in platforms:
            cur.execute('''
                INSERT INTO Game_Platform (Id_Game, Platform) VALUES (%s, %s)
            ''', (game_id, platform))

        # Insertar en Wishlist o Library según la selección
        if Add_To == 'wishlist':
            cur.execute('''
                INSERT INTO Wishlist (Id_User, Id_Game, Date_Added, Notes)
                VALUES (%s, %s, %s, %s)
            ''', (user_id, game_id, Date_Added, ''))
        elif Add_To == 'library':
            cur.execute('''
                INSERT INTO Library (Id_User, Id_Game, Date_Added, Notes)
                VALUES (%s, %s, %s, %s)
            ''', (user_id, game_id, Date_Added, ''))

        
        # Confirmar y notificar al usuario
        mysql.connection.commit()
        flash('Game Added Successfully')

    return redirect(url_for('Index'))

    
        


@app.route('/edit/<id>')
def get_game(id):
    cur = mysql.connection.cursor()
    
    # Obtener datos del juego
    cur.execute('SELECT * FROM Game WHERE Id_Game = %s', (id,))
    data = cur.fetchone()  # Usa fetchone ya que esperas un solo juego

    if data is None:
        flash('Game not found.')
        return redirect(url_for('Index'))

    # Obtener géneros del juego
    cur.execute('SELECT Genre FROM Game_Genre WHERE Id_Game = %s', (id,))
    genres = [row[0] for row in cur.fetchall()]

    # Verificar si el juego está en Library o Wishlist
    cur.execute('SELECT Id_Library FROM Library WHERE Id_Game = %s', (id,))
    in_library = cur.fetchone() is not None

    cur.execute('SELECT Id_Wishlist FROM Wishlist WHERE Id_Game = %s', (id,))
    in_wishlist = cur.fetchone() is not None

    # Determinar colección actual
    current_collection = 'library' if in_library else 'wishlist' if in_wishlist else ''


    # Obtener plataformas del juego
    cur.execute('SELECT Platform FROM Game_Platform WHERE Id_Game = %s', (id,))
    platforms = [row[0] for row in cur.fetchall()]
    
    # Asegúrate de pasar las listas de géneros y plataformas disponibles a la plantilla
    available_genres = ['Action', 'Adventure', 'RPG', 'Simulation', 'Strategy', 'Sports']  # Ejemplo de géneros disponibles
    available_platforms = ['PC', 'PS4', 'Xbox One', 'Switch', 'Mobile']  # Ejemplo de plataformas disponibles

    return render_template('edit_game.html', game=data, game_genres=genres, game_platforms=platforms, available_genres=available_genres, available_platforms=available_platforms, current_collection=current_collection)


@app.route('/update/<id>', methods=['POST'])  # POST también sirve para obtener datos del HTML
def update_game(id):
    if request.method == 'POST':
        # Obtener datos del formulario
        Title = request.form['Title']
        Description = request.form['Description']
        Release_Date = request.form['Release_Date']
        Developer = request.form['Developer']
        Publisher = request.form['Publisher']
        Multiplayer = bool(int(request.form['Multiplayer']))  # Convertir a booleano
        State = request.form['State']
        Date_Added = request.form['Date_Added']
        Image_URL = request.form['Image_URL']
        Achievements = bool(int(request.form['Achievements']))  # Convertir a booleano
        #Rating = int(request.form['Rating'])  # Convertir a entero
        Rating = int(request.form['Rating']) if request.form['Rating'] else 0
        Review = request.form['Review']
        Time_Played = request.form['Time_Played']
        user_id = 1
        
        # Actualizar datos en la base de datos
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE Game
            SET Title = %s,
                Description = %s,
                Release_Date = %s,
                Developer = %s,
                Publisher = %s,
                Multiplayer = %s,
                State = %s,
                Date_Added = %s,
                Image_URL = %s,
                Achievements = %s,
                Rating = %s,
                Review = %s,
                Time_Played = %s
            WHERE Id_Game = %s
        """, (
            Title, Description, Release_Date, Developer, Publisher, 
            Multiplayer, State, Date_Added, Image_URL, Achievements, 
            Rating, Review, Time_Played, id
        ))

        # Verificar y actualizar wishlist o library
        selected_collection = request.form['collection']
        cur.execute('DELETE FROM Library WHERE Id_Game = %s AND Id_User = %s', (id, user_id))
        cur.execute('DELETE FROM Wishlist WHERE Id_Game = %s AND Id_User = %s', (id, user_id))

        if selected_collection == 'library':
            cur.execute('INSERT INTO Library (Id_User, Id_Game, Date_Added) VALUES (%s, %s, %s)', (user_id, id, Date_Added))
        elif selected_collection == 'wishlist':
            cur.execute('INSERT INTO Wishlist (Id_User, Id_Game, Date_Added) VALUES (%s, %s, %s)', (user_id, id, Date_Added))

        # Actualizar géneros
        cur.execute('DELETE FROM Game_Genre WHERE Id_Game = %s', (id,))
        selected_genres = request.form.getlist('Genres')
        for genre in selected_genres:
            cur.execute('INSERT INTO Game_Genre (Id_Game, Genre) VALUES (%s, %s)', (id, genre))
        
        # Actualizar plataformas
        cur.execute('DELETE FROM Game_Platform WHERE Id_Game = %s', (id,))
        selected_platforms = request.form.getlist('Platforms')
        for platform in selected_platforms:
            cur.execute('INSERT INTO Game_Platform (Id_Game, Platform) VALUES (%s, %s)', (id, platform))
    
        # Confirmar cambios y notificar al usuario
        mysql.connection.commit()
        flash('Game Updated Successfully')
        
    return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def delete_game(id):
    cur = mysql.connection.cursor()
    user_id = 1
    
    # Eliminar el juego de la tabla principal Game
    cur.execute('DELETE FROM Game WHERE Id_Game = %s', (id,))
    
    # También puedes eliminar los datos relacionados en otras tablas
    cur.execute('DELETE FROM Game_Genre WHERE Id_Game = %s', (id,))
    cur.execute('DELETE FROM Game_Platform WHERE Id_Game = %s', (id,))

    # Eliminar el juego de la Library del usuario actual
    cur.execute('DELETE FROM Library WHERE Id_Game = %s AND Id_User = %s', (id, user_id))
    
    # Eliminar el juego de la Wishlist del usuario actual
    cur.execute('DELETE FROM Wishlist WHERE Id_Game = %s AND Id_User = %s', (id, user_id))
    
    mysql.connection.commit()
    flash('Game Removed Successfully')
    return redirect(url_for('Index'))


@app.route('/library/<string:id>')
def library(id):
    cur = mysql.connection.cursor()
    
    # Obtener juegos de la biblioteca del usuario actual usando el ID proporcionado
    cur.execute("""
        SELECT g.Id_Game, g.Image_URL 
        FROM Game g
        JOIN Library l ON g.Id_Game = l.Id_Game
        WHERE l.Id_User = %s
    """, (id,))
    
    games = cur.fetchall()
    
    return render_template('library.html', games=games)

@app.route('/wishlist/<string:id>')
def wishlist(id):
    cur = mysql.connection.cursor()
    
    # Obtener juegos de la lista de deseos del usuario actual usando el ID proporcionado
    cur.execute("""
        SELECT g.Id_Game, g.Image_URL 
        FROM Game g
        JOIN Wishlist w ON g.Id_Game = w.Id_Game
        WHERE w.Id_User = %s
    """, (id,))
    
    games = cur.fetchall()
    
    return render_template('wishlist.html', games=games)

@app.route('/profile/<string:id>')
def view_profile(id):
    cur = mysql.connection.cursor()
    
    # Obtener juegos de la biblioteca del usuario actual usando el ID proporcionado
    cur.execute('SELECT * FROM User WHERE Id_User = %s', (id,))
    profile = cur.fetchone()
    
    return render_template('view_profile.html', profile=profile)

@app.route('/edit_profile/<string:id>')
def get_profile(id):
    cur = mysql.connection.cursor()
    
    # Obtener juegos de la biblioteca del usuario actual usando el ID proporcionado
    cur.execute('SELECT * FROM User WHERE Id_User = %s', (id,))
    profile = cur.fetchone()
    
    return render_template('edit_profile.html', profile=profile)

@app.route('/update_profile/<id>', methods=['POST'])  # POST también sirve para obtener datos del HTML
def update_profile(id):
    if request.method == 'POST':
        # Obtener datos del formulario
        Username = request.form['Username']
        Biography = request.form['Biography']
        email = request.form['email']
        Avatar_URL = request.form['Avatar_URL']
        #user_id = id
        
        # Actualizar datos en la base de datos
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE User
            SET Username = %s,
                Biography = %s,
                email = %s,
                Avatar_URL = %s
            WHERE Id_User = %s
        """, (
            Username, Biography, email, Avatar_URL, id
        ))

    
        # Confirmar cambios y notificar al usuario
        mysql.connection.commit()
        #flash('Game Updated Successfully')
        
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port= 3000, debug = True)