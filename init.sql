-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS GamesCollector;
USE GamesCollector;

-- Tabla User: Almacena los datos de los usuarios
CREATE TABLE IF NOT EXISTS User (
    Id_User INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    Username VARCHAR(255),
    Biography TEXT,
    Avatar_URL VARCHAR(255),
    Last_Login TIMESTAMP,
    Date_Created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar usuario inicial con ID 1
INSERT INTO User (Id_User, email, password, Username, Biography, Avatar_URL)
VALUES (1, 'admin@example.com', 'hashed_password', 'Admin', 'Initial admin user', 'https://example.com/avatar.png')
ON DUPLICATE KEY UPDATE Id_User=Id_User;

-- Tabla Game: Almacena los datos de los videojuegos
CREATE TABLE IF NOT EXISTS Game (
    Id_Game INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    Description TEXT,
    Release_Date DATE,
    Developer VARCHAR(255),
    Publisher VARCHAR(255),
    Multiplayer BOOLEAN,
    State ENUM('Played', 'Playing', 'Backlog'),
    Date_Added DATE,
    Image_URL VARCHAR(500),
    Achievements BOOLEAN,
    Rating INT CHECK (Rating BETWEEN 0 AND 5),
    Review TEXT,
    Time_Played TIME
);

-- Tabla Game_Genre: Relaciona los juegos con uno o varios géneros
CREATE TABLE IF NOT EXISTS Game_Genre (
    Id_Game INT,
    Genre VARCHAR(100),
    PRIMARY KEY (Id_Game, Genre),
    FOREIGN KEY (Id_Game) REFERENCES Game(Id_Game) ON DELETE CASCADE
);

-- Tabla Game_Platform: Relaciona los juegos con una o varias plataformas
CREATE TABLE IF NOT EXISTS Game_Platform (
    Id_Game INT,
    Platform VARCHAR(100),
    PRIMARY KEY (Id_Game, Platform),
    FOREIGN KEY (Id_Game) REFERENCES Game(Id_Game) ON DELETE CASCADE
);

-- Tabla Library: Almacena los juegos que cada usuario tiene en su biblioteca
CREATE TABLE IF NOT EXISTS Library (
    Id_Library INT AUTO_INCREMENT PRIMARY KEY,
    Id_User INT,
    Id_Game INT,
    Date_Added DATE,
    Notes TEXT,
    FOREIGN KEY (Id_User) REFERENCES User(Id_User) ON DELETE CASCADE,
    FOREIGN KEY (Id_Game) REFERENCES Game(Id_Game) ON DELETE CASCADE
);

-- Tabla Wishlist: Almacena los juegos que cada usuario desea jugar en el futuro
CREATE TABLE IF NOT EXISTS Wishlist (
    Id_Wishlist INT AUTO_INCREMENT PRIMARY KEY,
    Id_User INT,
    Id_Game INT,
    Date_Added DATE,
    Notes TEXT,
    FOREIGN KEY (Id_User) REFERENCES User(Id_User) ON DELETE CASCADE,
    FOREIGN KEY (Id_Game) REFERENCES Game(Id_Game) ON DELETE CASCADE
);

-- Tabla Game_Rating: Permite que los usuarios califiquen y revisen los juegos
CREATE TABLE IF NOT EXISTS Game_Rating (
    Id_Rating INT AUTO_INCREMENT PRIMARY KEY,
    Id_User INT,
    Id_Game INT,
    Rating INT CHECK (Rating BETWEEN 0 AND 5),
    Review TEXT,
    Date_Rated DATE,
    FOREIGN KEY (Id_User) REFERENCES User(Id_User) ON DELETE CASCADE,
    FOREIGN KEY (Id_Game) REFERENCES Game(Id_Game) ON DELETE CASCADE
);
