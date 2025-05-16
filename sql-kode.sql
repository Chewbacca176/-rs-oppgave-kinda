CREATE DATABASE IF NOT EXISTS portfoolje;


CREATE TABLE if not exists brukere (
    bruker_id INT AUTO_INCREMENT PRIMARY KEY,
    navn VARCHAR(255) NOT NULL,
    etternavn VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    passord VARCHAR(255) NOT NULL, 
    role text NOT NULL default 'user',
    opprettet_tidspunkt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



CREATE TABLE if not exists poeng_liste (
    poeng_id INT AUTO_INCREMENT PRIMARY KEY,
    bruker_id INT NOT NULL,
    poeng INT NOT NULL,
    oppnådd_tidspunkt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (bruker_id) REFERENCES brukere(bruker_id) ON DELETE CASCADE
);




CREATE TABLE if not exists bokbestillinger (
    bok_id INT AUTO_INCREMENT PRIMARY KEY,
    bruker_id INT NOT NULL,
    Boknavn VARCHAR(255) NOT NULL,
    Sider VARCHAR(255) NOT NULL,
    Ord VARCHAR(255) NOT NULL ,
    Beskrivelse VARCHAR(255) NOT NULL, 
    is_active VARCHAR(255) NOT NULL DEFAULT 'yes',
    opprettet_tidspunkt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (bruker_id) REFERENCES brukere(bruker_id) ON DELETE CASCADE
);

