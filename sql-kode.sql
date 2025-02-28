CREATE DATABASE IF NOT EXISTS nettsidespill;


CREATE TABLE brukere (
    bruker_id INT AUTO_INCREMENT PRIMARY KEY,
    navn VARCHAR(255) NOT NULL,
    etternavn VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    passord VARCHAR(255) NOT NULL, 
    role text NOT NULL default 'user',
    opprettet_tidspunkt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



CREATE TABLE poeng_liste (
    poeng_id INT AUTO_INCREMENT PRIMARY KEY,
    bruker_id INT NOT NULL,
    poeng INT NOT NULL,
    oppnådd_tidspunkt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (bruker_id) REFERENCES brukere(bruker_id) ON DELETE CASCADE
);






