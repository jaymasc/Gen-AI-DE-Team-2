DROP TABLE IF EXISTS species;
DROP TABLE IF EXISTS addresses;
DROP TABLE IF EXISTS people;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS people_addresses;
DROP TABLE IF EXISTS student_course_registration;
DROP TABLE IF EXISTS student_course_attendance;

CREATE TABLE species (
    species_id INT PRIMARY KEY,
    name VARCHAR(255),
    planet_of_origin VARCHAR(255),
    member_of_starfleet BOOLEAN
);

CREATE TABLE addresses (
    address_id INT PRIMARY KEY,
    line_1 VARCHAR(255),
    line_2 VARCHAR(255),
    city VARCHAR(100),
    zip_postcode VARCHAR(50),
    state_province_county VARCHAR(100),
    country VARCHAR(100),
    planet VARCHAR(100)
);

CREATE TABLE people (
    person_id INT PRIMARY KEY,
    first_name VARCHAR(100),
    middle_name VARCHAR(100),
    last_name VARCHAR(100),
    cell_mobile_number VARCHAR(20),
    email_address VARCHAR(255),
    species_id INT,
    FOREIGN KEY (species_id) REFERENCES species(species_id)
);

CREATE TABLE students (
    student_id INT PRIMARY KEY,
    student_details TEXT
);

CREATE TABLE courses (
    course_id INT PRIMARY KEY,
    course_name VARCHAR(255),
    course_description TEXT,
    other_details TEXT
);

CREATE TABLE people_addresses (
    person_address_id INT PRIMARY KEY,
    person_id INT,
    address_id INT,
    date_from DATE,
    date_to DATE,
    FOREIGN KEY (person_id) REFERENCES people(person_id),
    FOREIGN KEY (address_id) REFERENCES addresses(address_id)
);

CREATE TABLE student_course_registrations (
    student_id INT,
    course_id INT,
    registration_date DATE,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

CREATE TABLE student_course_attendance (
    student_id INT,
    course_id INT,
    date_of_attendance DATE,
    grade VARCHAR(2),
    PRIMARY KEY (student_id, course_id, date_of_attendance),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

INSERT INTO species (species_id, name, planet_of_origin, member_of_starfleet) VALUES
(1, 'Human', 'Earth', TRUE),
(2, 'Vulcan', 'Vulcan', TRUE),
(3, 'Klingon', 'QonoS', FALSE),
(4, 'Andorian', 'Andoria', TRUE),
(5, 'Betazoid', 'Betazed', TRUE),
(6, 'Ferengi', 'Ferenginar', FALSE),
(7, 'Cardassian', 'Cardassia', FALSE),
(8, 'Bajoran', 'Bajor', TRUE),
(9, 'Trill', 'Trill', TRUE),
(10, 'Romulan', 'Romulus', FALSE);

INSERT INTO addresses (address_id, line_1, line_2, city, zip_postcode, state_province_county, country, planet) VALUES
(1, '23 Spock Street', NULL, 'ShiKahr', 'VU239', 'Vulcana Regar', 'TKhasi', 'Vulcan'),
(2, '47 TPaal Road', NULL, 'Raal', 'VU542', 'Vulcana Regar', 'TKhasi', 'Vulcan'),
(3, '12 Kirk Avenue', NULL, 'San Francisco', 'SF901', 'California', 'United States', 'Earth'),
(4, '88 Picard Lane', NULL, 'La Barre', 'LB742', 'Burgundy', 'France', 'Earth'),
(5, '5 Sulu Way', NULL, 'Kyoto', 'KY103', 'Kyoto Prefecture', 'Japan', 'Earth'),
(6, '91 Uhura Plaza', NULL, 'Nairobi', 'NA254', 'Nairobi County', 'Kenya', 'Earth'),
(7, '15 Scott Court', NULL, 'Aberdeen', 'AB10', 'Scotland', 'United Kingdom', 'Earth'),
(8, '3 McCoy Drive', NULL, 'Atlanta', 'AT303', 'Georgia', 'United States', 'Earth'),
(9, '36 Martok Lane', NULL, 'First City', 'QO101', 'Ketha Province', 'QonoS', 'Klingon'),
(10, '22 Worf Boulevard', NULL, 'Mekrovik', 'QO202', 'Mekrovik District', 'QonoS', 'Klingon'),
(11, '14 Crusher Street', NULL, 'Coppelius', 'CP879', 'Synth Settlement', 'United Federation of Planets', 'Coppelius'),
(12, '2 Troi Road', NULL, 'Betazed City', 'BZ356', 'Leran District', 'Betazed', 'Betazed'),
(13, '29 La Forge Lane', NULL, 'Mogadishu', 'MG111', 'Banaadir', 'Somalia', 'Earth'),
(14, '7 Chekov Circle', NULL, 'Saint Petersburg', 'SP190', 'Northwestern District', 'Russia', 'Earth'),
(15, '19 Yar Avenue', NULL, 'Turkana IV Colony', 'TIV842', 'Coalition Space', 'Turkana IV', 'Turkana IV'),
(16, '33 Sarek Street', NULL, 'Vulcanis City', 'VU654', 'Tasmeen District', 'TKhasi', 'Vulcan'),
(17, '6 Dax Way', NULL, 'Trill City', 'TR330', 'Leran Manev', 'Trill', 'Trill'),
(18, '55 Kira Nerys Road', NULL, 'Bajoran Central', 'BJ091', 'Hedrikspool Province', 'Bajor', 'Bajor'),
(19, '21 Odo Street', NULL, 'New Bajor', 'NB052', 'Kendra Valley', 'Bajor', 'Bajor'),
(20, '11 Riker Lane', NULL, 'Alaska City', 'AK907', 'Alaska', 'United States', 'Earth');

INSERT INTO people (person_id, first_name, middle_name, last_name, cell_mobile_number, email_address, species_id) VALUES
(1, 'Tuvok', NULL, 'Son of Tuvan', '111-222-3333', 'tuvok@starfleet.com', 2),
(2, 'Sarek', NULL, 'Son of Skon', '111-222-4444', 'sarek@vulcan.gov', 2),
(3, 'James', 'T.', 'Kirk', '111-222-5555', 'jkirk@starfleet.com', 1),
(4, 'Jean-Luc', NULL, 'Picard', '111-222-6666', 'picard@starfleet.com', 1),
(5, 'Hikaru', NULL, 'Sulu', '111-222-7777', 'hsulu@starfleet.com', 1),
(6, 'Nyota', NULL, 'Uhura', '111-222-8888', 'nuhura@starfleet.com', 1),
(7, 'Montgomery', NULL, 'Scott', '111-222-9999', 'mscott@starfleet.com', 1),
(8, 'Leonard', 'H.', 'McCoy', '111-222-0000', 'lmccoy@starfleet.com', 1),
(9, 'Martok', NULL, 'Son of Urthog', '333-444-5555', 'martok@klingonempire.gov', 3),
(10, 'Worf', 'Son of', 'Mogh', '333-444-6666', 'worf@starfleet.com', 3),
(11, 'Soji', NULL, 'Asher', '444-555-6666', 'soji@coppelius.synth', 1),
(12, 'Deanna', NULL, 'Troi', '555-666-7777', 'dtroi@starfleet.com', 5),
(13, 'Geordi', NULL, 'La Forge', '111-222-1234', 'lforge@starfleet.com', 1),
(14, 'Pavel', NULL, 'Chekov', '111-222-2345', 'pchekov@starfleet.com', 1),
(15, 'Tasha', NULL, 'Yar', '666-777-8888', 'tyar@starfleet.com', 1),
(16, 'Spock', NULL, 'Son of Sarek', '111-222-3456', 'spock@starfleet.com', 2),
(17, 'Jadzia', NULL, 'Dax', '777-888-9999', 'jdax@starfleet.com', 9),
(18, 'Kira', 'Nerys', NULL, '888-999-1111', 'kneris@bajor.gov', 8),
(19, 'Odo', NULL, NULL, '999-111-2222', 'odo@bajor.gov', 8),
(20, 'William', 'T.', 'Riker', '111-222-4567', 'wriker@starfleet.com', 1);

INSERT INTO students (student_id, student_details) VALUES
(1, 'Majoring in Security and Tactical Operations'),
(2, 'Majoring in Vulcan Philosophy and Diplomacy'),
(3, 'Majoring in Command and Starship Operations'),
(4, 'Majoring in Archaeology and Warp Field Theory'),
(5, 'Majoring in Helmsmanship and Astrophysics'),
(6, 'Majoring in Xenolinguistics and Communications'),
(7, 'Majoring in Starship Engineering and Warp Drive Mechanics'),
(8, 'Majoring in Xenobiology and Medical Sciences'),
(9, 'Majoring in Klingon Warfare and Strategy'),
(10, 'Majoring in Klingon Culture and Starfleet Security'),
(11, 'Majoring in Synthetic Life Studies and Ethics'),
(12, 'Majoring in Psychology and Betazoid Empathic Skills'),
(13, 'Majoring in Starship Engineering and Holotechnology'),
(14, 'Majoring in Stellar Cartography and Navigation'),
(15, 'Majoring in Security Operations and Tactical Analysis'),
(16, 'Majoring in Intergalactic Diplomacy and Science'),
(17, 'Majoring in Trill Symbiotic Studies and Science'),
(18, 'Majoring in Bajoran Religious Studies and Military Tactics'),
(19, 'Majoring in Investigative Techniques and Security'),
(20, 'Majoring in Command Strategy and Poker Theory');

INSERT INTO courses (course_id, course_name, course_description, other_details) VALUES
(1, 'Intergalactic Diplomacy', 'An in-depth study of diplomatic principles and practices in the United Federation of Planets.', 'Focus on negotiation, cultural sensitivity, and conflict resolution.'),
(2, 'Warp Field Theory', 'Advanced concepts in warp drive technology and subspace physics.', 'Includes practical applications and theoretical limits of warp technology.'),
(3, 'Xenobiology', 'Study of alien life forms, their biology, and ecosystems.', 'Includes field research methods and xenobiological ethics.'),
(4, 'Quantum Mechanics in Starship Engineering', 'Application of quantum mechanics in the design and operation of starship systems.', 'Emphasis on practical engineering solutions.'),
(5, 'Federation History', 'A comprehensive overview of the history of the United Federation of Planets.', 'Includes political, cultural, and military developments.'),
(6, 'Exoarchaeology', 'Archaeological methods and practices in the exploration of alien civilizations.', 'Focus on fieldwork and analysis of artifacts.'),
(7, 'Astrophysics and Cosmology', 'Study of the universe, including stars, galaxies, and cosmic phenomena.', 'Covers theoretical and observational approaches.'),
(8, 'Starfleet Medical Practices', 'Principles and practices of medicine within Starfleet.', 'Includes alien physiology, emergency medicine, and advanced medical technologies.'),
(9, 'Cybernetics and Artificial Intelligence', 'Fundamentals of cybernetics and development of artificial intelligence.', 'Ethical implications and practical applications in robotics and AI.'),
(10, 'Temporal Mechanics', 'Theoretical study of time, temporal paradoxes, and time travel.', 'Discussion of time travel ethics and the Temporal Prime Directive.'),
(11, 'Xenolinguistics', 'Study of alien languages and communication methods.', 'Techniques for translation and understanding of non-human languages.'),
(12, 'Subspace Communication', 'Principles of faster-than-light communication technologies.', 'Practical applications in deep-space communication.'),
(13, 'Alien Ethics and Law', 'Study of ethical systems and legal practices among various alien species.', 'Comparison with Federation law and moral philosophy.'),
(14, 'Stellar Cartography', 'Mapping and analysis of star systems, nebulas, and other celestial phenomena.', 'Use of advanced sensors and astrometric techniques.'),
(15, 'Quantum Chemistry', 'Study of chemical processes and reactions at the quantum level.', 'Application in material science and energy production.');

INSERT INTO people_addresses (person_address_id, person_id, address_id, date_from, date_to) VALUES
(1, 1, 1, '2210-01-01', '2212-12-31'),
(2, 2, 2, '2211-02-15', '2213-06-30'),
(3, 3, 3, '2210-03-01', '2212-07-15'),
(4, 4, 4, '2212-04-20', '2215-09-10'),
(5, 5, 5, '2213-05-05', '2216-11-20'),
(6, 6, 6, '2210-06-10', '2212-08-30'),
(7, 7, 7, '2211-07-15', '2214-10-05'),
(8, 8, 8, '2212-08-01', '2215-12-15'),
(9, 9, 9, '2213-09-20', '2216-03-25'),
(10, 10, 10, '2210-10-30', '2213-04-10'),
(11, 11, 11, '2211-11-11', '2214-05-16'),
(12, 12, 12, '2210-12-12', '2213-06-22'),
(13, 13, 13, '2212-01-20', '2215-07-30'),
(14, 14, 14, '2213-02-25', '2216-09-05'),
(15, 15, 15, '2211-03-30', '2214-08-15'),
(16, 16, 16, '2212-05-10', '2215-10-20'),
(17, 17, 17, '2213-06-15', '2216-12-31'),
(18, 18, 18, '2210-07-25', '2212-11-30'),
(19, 19, 19, '2211-08-08', '2214-01-13'),
(20, 20, 20, '2212-09-17', '2215-02-28');

INSERT INTO student_course_registrations (student_id, course_id, registration_date) VALUES
(1, 1, '2211-09-01'),
(2, 2, '2211-09-01'),
(3, 3, '2211-09-01'),
(4, 4, '2211-09-01'),
(5, 5, '2211-09-01'),
(6, 1, '2211-09-01'),
(7, 2, '2211-09-01'),
(8, 3, '2211-09-01'),
(9, 4, '2211-09-01'),
(10, 5, '2211-09-01'),
(11, 1, '2211-09-01'),
(12, 2, '2211-09-01'),
(13, 6, '2211-09-01'),
(14, 7, '2211-09-01'),
(15, 8, '2211-09-01'),
(16, 9, '2211-09-01'),
(17, 10, '2211-09-01'),
(18, 11, '2211-09-01');

INSERT INTO student_course_attendance (student_id, course_id, date_of_attendance, grade) VALUES
(1, 12, '2210-02-15', 'A'),
(2, 13, '2210-03-10', 'C'),
(3, 14, '2210-04-05', 'B'),
(4, 12, '2210-02-20', 'A-'),
(5, 15, '2210-05-01', 'F'),
(6, 12, '2210-02-25', 'B+'),
(7, 13, '2210-03-15', 'A'),
(8, 14, '2210-04-10', 'D'),
(9, 15, '2210-05-06', 'B-'),
(10, 12, '2210-03-01', 'F');