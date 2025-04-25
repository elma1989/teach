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
    std_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    std_first_name VARCHAR(20) NOT NULL,
    std_last_name VARCHAR(20) NOT NULL,
    std_birth_date DATE NOT NULL,
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
CREATE TABLE lesson(
    crs_name VARCHAR(20) NOT NULL REFERENCES course(crs_name) ON DELETE CASCADE,
    les_time DATETIME NOT NULL,
    les_topic TEXT,
    PRIMARY KEY (crs_name, les_time)
);
CREATE TABLE lesson_homework(
    crs_name VARCHAR(20) NOT NULL,
    les_time DATETIME NOT NULL,
    les_homework TEXT NOT NULL,
    PRIMARY KEY (crs_name, les_time, les_homework),
    FOREIGN KEY (crs_name, les_time) REFERENCES lesson(crs_name, les_time)
);
CREATE TABLE lesson_student(
    crs_name VARCHAR(20) NOT NULL,
    les_time DATETIME NOT NULL,
    std_id INTEGER NOT NULL REFERENCES student (std_id),
    les_student_present BOOLEAN NOT NULL DEFAULT false,
    PRIMARY KEY (crs_name, les_time, std_id),
    FOREIGN KEY (crs_name, les_time) REFERENCES lesson(crs_name, les_time)
);