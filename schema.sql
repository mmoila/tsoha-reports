CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	username TEXT UNIQUE,
	password TEXT,
	is_admin BOOLEAN,
	is_active BOOLEAN
);


CREATE TABLE locations (
	id SERIAL PRIMARY KEY,
	ICAO_ident TEXT UNIQUE,
	IATA_ident TEXT UNIQUE,
	location_name TEXT
);


CREATE TABLE reports (
	id SERIAL PRIMARY KEY,
	date DATE,
	title TEXT,
	description TEXT,
	user_id INTEGER REFERENCES users,
	location_id INTEGER REFERENCES locations,
	created_at TIMESTAMP
);

INSERT INTO locations (ICAO_ident, IATA_ident, location_name)
VALUES
	('EFHK', 'HEL', 'Helsinki-Vantaa'),
	('EFTU', 'TKU', 'Turku'),
	('EFTP', 'TMP', 'Tampere'),
	('EFVA', 'VAA', 'Vaasa'),
	('EFOU', 'OUL', 'Oulu');