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
    teach_id INTEGER NOT NULL REFERENCES teacher(teach_id) ON DELETE CASCADE,
    sub_abr CHAR(3) NOT NULL REFERENCES subject(sub_abr) ON DELETE CASCADE,
    PRIMARY KEY (teach_id, sub_abr)
);
CREATE TABLE grade(
    grd_name VARCHAR(20) NOT NULL PRIMARY KEY,
    teach_id INTEGER NOT NULL REFERENCES teacher(teach_id)
);
CREATE TABLE student(
    std_id INTEGER NOT NULL PRIMARY KEY,
    std_first_name VARCHAR(20) NOT NULL,
    std_last_name VARCHAR(20) NOT NULL,
    grd_name VARCHAR(20) REFERENCES grade(grd_name) ON UPDATE CASCADE ON DELETE SET NULL
);
CREATE TABLE course(
    crs_name VARCHAR(20) NOT NULL PRIMARY KEY,
    teach_id INTEGER NOT NULL REFERENCES teacher(teach_id),
    sub_abr CHAR(3) NOT NULL REFERENCES subject(sub_abr)
);
CREATE TABLE student_course(
    std_id INTEGER NOT NULL REFERENCES student(std_id) ON DELETE CASCADE,
    crs_name VARCHAR(20) NOT NULL REFERENCES course(crs_name) ON DELETE CASCADE,
    PRIMARY KEY (std_id, crs_name)
);