CREATE TABLE subject (
    name VARCHAR PRIMARY KEY
);

CREATE TABLE teacher (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR,
    subject VARCHAR REFERENCES subject(name)
);

CREATE TABLE timetable (
    id SERIAL PRIMARY KEY,
    day VARCHAR,
    subject VARCHAR REFERENCES subject(name),
    room_number VARCHAR,
    start_time TIMESTAMP
);


-- Заполнение таблицы предметов (subject)
INSERT INTO subject (name) VALUES
('Математика'),
('Физика'),
('Химия'),
('История'),
('Литература');

-- Заполнение таблицы преподавателей (teacher)
INSERT INTO teacher (full_name, subject) VALUES
('Иванов Иван Иванович', 'Математика'),
('Петров Петр Петрович', 'Физика'),
('Сидоров Сидор Сидорович', 'Химия'),
('Кузнецова Анна Петровна', 'История'),
('Смирнова Елена Александровна', 'Литература');

-- Заполнение таблицы расписания (timetable)
INSERT INTO timetable (day, subject, room_number, start_time) VALUES
('Понедельник', 'Математика', '101', '2024-05-05 08:30:00'),
('Понедельник', 'Физика', '102', '2024-05-05 10:00:00'),
('Понедельник', 'Химия', '103', '2024-05-05 11:30:00'),
('Понедельник', 'История', '104', '2024-05-05 13:00:00'),
('Понедельник', 'Литература', '105', '2024-05-05 14:30:00'),

('Вторник', 'Математика', '101', '2024-05-06 08:30:00'),
('Вторник', 'Физика', '102', '2024-05-06 10:00:00'),
('Вторник', 'Химия', '103', '2024-05-06 11:30:00'),
('Вторник', 'История', '104', '2024-05-06 13:00:00'),
('Вторник', 'Литература', '105', '2024-05-06 14:30:00'),

('Среда', 'Математика', '101', '2024-05-07 08:30:00'),
('Среда', 'Физика', '102', '2024-05-07 10:00:00'),
('Среда', 'Химия', '103', '2024-05-07 11:30:00'),
('Среда', 'История', '104', '2024-05-07 13:00:00'),
('Среда', 'Литература', '105', '2024-05-07 14:30:00'),

('Четверг', 'Математика', '101', '2024-05-08 08:30:00'),
('Четверг', 'Физика', '102', '2024-05-08 10:00:00'),
('Четверг', 'Химия', '103', '2024-05-08 11:30:00'),
('Четверг', 'История', '104', '2024-05-08 13:00:00'),
('Четверг', 'Литература', '105', '2024-05-08 14:30:00'),

('Пятница', 'Математика', '101', '2024-05-09 08:30:00'),
('Пятница', 'Физика', '102', '2024-05-09 10:00:00'),
('Пятница', 'Химия', '103', '2024-05-09 11:30:00'),
('Пятница', 'История', '104', '2024-05-09 13:00:00'),
('Пятница', 'Литература', '105', '2024-05-09 14:30:00');
