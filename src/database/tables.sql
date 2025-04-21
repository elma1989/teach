CREATE TABLE subject(
    sub_abr CHAR(3) NOT NULL PRIMARY KEY,
    sub_name VARCHAR(20) NOT NULL
);
CREATE TABLE teacher(
    teach_id INTEGER NOT NULL PRIMARY KEY,
    teach_first_name VARCHAR(20) NOT NULL,
    teach_last_name VARCHAR(20) NOT NULL,
    teach_birth_date DATE NOT NULL
);
CREATE TABLE teacher_subject(
    teach_id INTEGER NOT NULL REFERENCES teacher(teach_id),
    sub_abr CHAR(3) NOT NULL REFERENCES subject(sub_abr),
    PRIMARY KEY (teach_id, sub_abr)
);