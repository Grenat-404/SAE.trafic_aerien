
CREATE DATABASE IF NOT EXISTS trafic_aerien;
USE trafic_aerien;

-- Table aeroports
CREATE TABLE aeroports (
    id INT PRIMARY KEY,
    nom VARCHAR(100),
    pays VARCHAR(50)
);

-- Table compagnies
CREATE TABLE compagnies (
    id INT PRIMARY KEY,
    nom VARCHAR(100),
    description TEXT,
    pays_rattachement VARCHAR(50)
);

-- Table types_avions
CREATE TABLE types_avions (
    id INT PRIMARY KEY,
    marque VARCHAR(50),
    modele VARCHAR(50),
    description TEXT,
    images TEXT,
    longueur_piste_necessaire INT
);

-- Table avions
CREATE TABLE avions (
    id INT PRIMARY KEY,
    nom VARCHAR(20),
    compagnie INT,
    modele INT,
    FOREIGN KEY (compagnie) REFERENCES compagnies(id),
    FOREIGN KEY (modele) REFERENCES types_avions(id)
);

-- Table pistes_atterrissage
CREATE TABLE pistes_atterrissage (
    id INT PRIMARY KEY,
    numero VARCHAR(20),
    aeroport INT,
    longueur INT,
    FOREIGN KEY (aeroport) REFERENCES aeroports(id)
);

-- Table vols
CREATE TABLE vols (
    id INT PRIMARY KEY,
    avion INT,
    pilote VARCHAR(100),
    aeroport_depart INT,
    date_heure_depart DATETIME,
    aeroport_arrivee INT,
    date_heure_arrivee DATETIME,
    FOREIGN KEY (avion) REFERENCES avions(id),
    FOREIGN KEY (aeroport_depart) REFERENCES aeroports(id),
    FOREIGN KEY (aeroport_arrivee) REFERENCES aeroports(id)
);

-- Insertion des données

INSERT INTO aeroports VALUES
(1, 'Aéroport Charles de Gaulle', 'France'),
(2, 'Aéroport de Londres Heathrow', 'Royaume-Uni'),
(3, 'Aéroport John F. Kennedy', 'États-Unis'),
(4, 'Aéroport de Francfort', 'Allemagne'),
(5, 'Aéroport de Madrid-Barajas', 'Espagne'),
(6, 'Aeroportevaluation', 'France');

INSERT INTO compagnies VALUES
(1, 'Air France', 'Compagnie aérienne nationale française', 'France'),
(2, 'British Airways', 'Compagnie aérienne britannique', 'Royaume-Uni'),
(3, 'Lufthansa', 'Compagnie aérienne allemande', 'Allemagne'),
(4, 'American Airlines', 'Compagnie aérienne américaine', 'États-Unis'),
(5, 'Iberia', 'Compagnie aérienne espagnole', 'Espagne');

INSERT INTO types_avions VALUES
(1, 'Airbus', 'A320', 'Avion de ligne moyen-courrier biréacteur', 'a320_1.jpg,a320_2.jpg', 2500),
(2, 'Boeing', '737-800', 'Avion de ligne court et moyen-courrier', 'b737_1.jpg,b737_2.jpg', 2400),
(3, 'Airbus', 'A380', 'Très gros porteur long-courrier quadriréacteur', 'a380_1.jpg,a380_2.jpg', 3000),
(4, 'Boeing', '777-300ER', 'Avion de ligne long-courrier biréacteur', 'b777_1.jpg,b777_2.jpg', 3200),
(5, 'Airbus', 'A350-900', 'Avion de ligne long-courrier nouvelle génération', 'a350_1.jpg,a350_2.jpg', 2900);

INSERT INTO avions VALUES
(1, 'F-GKXA', 1, 1),
(2, 'F-HEPJ', 1, 3),
(3, 'G-EUUU', 2, 2),
(4, 'G-XLEC', 2, 3),
(5, 'D-AIMA', 3, 3),
(6, 'D-AIXA', 3, 5),
(7, 'N775AN', 4, 4),
(8, 'N321AA', 4, 1),
(9, 'EC-MXV', 5, 1),
(10, 'EC-NBE', 5, 5),
(11, 'test', 1, 1);

INSERT INTO pistes_atterrissage VALUES
(1, '09L/27R', 1, 4215),
(2, '09R/27L', 1, 4000),
(3, '08L/26R', 1, 2700),
(4, '09L/27R', 2, 3902),
(5, '09R/27L', 2, 3660),
(6, '04L/22R', 3, 4423),
(7, '04R/22L', 3, 3460),
(8, '07C/25C', 4, 4000),
(9, '14L/32R', 5, 4179),
(10, '1', 6, 30);

INSERT INTO vols VALUES
(1, 1, 'Jean Dupont', 1, '2024-12-15 10:30:00', 2, '2024-12-15 12:45:00'),
(2, 3, 'John Smith', 2, '2024-12-15 14:20:00', 3, '2024-12-15 22:10:00'),
(3, 5, 'Klaus Mueller', 4, '2024-12-16 08:15:00', 1, '2024-12-16 18:30:00'),
(4, 7, 'Mike Johnson', 3, '2024-12-16 16:45:00', 4, '2024-12-17 06:25:00'),
(5, 9, 'Carlos Rodriguez', 5, '2024-12-17 09:00:00', 2, '2024-12-17 12:15:00'),
(6, 2, 'Pierre Martin', 1, '2024-12-17 15:30:00', 3, '2024-12-18 01:45:00'),
(7, 6, 'Hans Weber', 4, '2024-12-18 11:20:00', 5, '2024-12-18 13:35:00'),
(8, 8, 'Robert Taylor', 3, '2024-12-18 19:10:00', 1, '2024-12-19 07:25:00'),
(9, 2, 'pilote test', 2, '2024-08-16 13:50:00', 3, '2024-08-16 15:00:00');
