-- Création de la base de données si elle n'existe pas
CREATE DATABASE IF NOT EXISTS bd_django;

-- Utiliser la base de données bd_django
USE bd_django;

-- Création des tables
CREATE TABLE fisa_years (
    year INT NOT NULL PRIMARY KEY,
    nom_promotion VARCHAR(255) NOT NULL
);

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    email_tsp VARCHAR(254),
    fisa_year INT,
    FOREIGN KEY (fisa_year) REFERENCES fisa_years(year)
);

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    email_perso VARCHAR(254),
    is_active TINYINT(1) DEFAULT 1,
    is_superuser TINYINT(1) DEFAULT 0,
    date_joined DATETIME DEFAULT CURRENT_TIMESTAMP,
    student_id INT,
    token CHAR(64),
    auth_cookie VARCHAR(255),
    FOREIGN KEY (student_id) REFERENCES students(id)
);

CREATE TABLE data_link (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fisa_year INT,
    type VARCHAR(100) NOT NULL,
    link TEXT NOT NULL,
    title VARCHAR(255) NOT NULL,
    `desc` TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fisa_year) REFERENCES fisa_years(year)
);

CREATE TABLE SIF (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    bungalow INT,
    pizza VARCHAR(255),
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- Insertion des données initiales

-- Ajouter les années FISA
INSERT INTO fisa_years (year, nom_promotion) VALUES 
    (0, 'FISA'),
    (1, 'Lima'),
    (2, 'Kilo'),
    (3, 'Juliet');

-- Ajouter un étudiant
INSERT INTO students (first_name, last_name, email_tsp, fisa_year) VALUES 
    ('Corentin', 'R', 'corentin.r@telecom-sudparis.eu', 2);

-- Ajouter des liens à présenter
INSERT INTO data_link (fisa_year, type, link, title, `desc`, created_at) VALUES 
    (0, 'WhatsApp', 'https://chat.whatsapp.com/EXnszNls8PN3ivAK2XTlmS', 'Whatsapp de l\'ASINT', 'Le groupe Whatsapp de l\'association sportive de TSP', NOW()),
    (0, 'Instagram', 'https://www.instagram.com/fipa_kilo?igsh=Nm8wZmZvN21lcGdn', 'Instagram FISA Kilo (2A)', 'Page Instagram des FISA Kilo. Abonnez-vous !', NOW()),
    (0, 'Web', 'https://ecampus.imtbs-tsp.eu/', 'Ecampus', 'Site web d\'accès à l\'espace personnel étudiant. Ici, vous pourrez consulter vos mails, accéder à Moodle, gérer vos impressions...', NOW());
