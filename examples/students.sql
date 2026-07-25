CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, student_name TEXT NOT NULL, roll_number INTEGER NOT NULL UNIQUE, grade TEXT NOT NULL, gpa REAL NOT NULL);
INSERT OR IGNORE INTO students (student_name, roll_number, grade, gpa) VALUES ('Aarav Sharma', 101, 'A+', 3.90);
INSERT OR IGNORE INTO students (student_name, roll_number, grade, gpa) VALUES ('Diya Patel', 102, 'A', 3.80);
INSERT OR IGNORE INTO students (student_name, roll_number, grade, gpa) VALUES ('Kabir Verma', 103, 'O', 4.00);
INSERT OR IGNORE INTO students (student_name, roll_number, grade, gpa) VALUES ('Ananya Roy', 104, 'A', 3.75);
INSERT OR IGNORE INTO students (student_name, roll_number, grade, gpa) VALUES ('Rohan Gupta', 105, 'A+', 3.95);
SELECT * FROM students;
