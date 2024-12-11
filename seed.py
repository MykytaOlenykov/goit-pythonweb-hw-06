import random

from faker import Faker

from connect import session
from models import Group, Teacher, Subject, Student, StudentGrade


def generate_group_name(fake: Faker):
    return f"{fake.word().capitalize()}-{random.randint(100, 999)}"


if __name__ == "__main__":
    fake = Faker()

    try:
        groups = [Group(name=generate_group_name(fake)) for _ in range(3)]
        session.add_all(groups)

        teachers = [
            Teacher(first_name=fake.first_name(), last_name=fake.last_name())
            for _ in range(5)
        ]
        session.add_all(teachers)

        subjects = [
            Subject(
                name=name,
                teacher=random.choice(teachers),
            )
            for name in [
                "Mathematics",
                "Physics",
                "Chemistry",
                "Biology",
                "Geography",
                "Literature",
                "Music",
                "Computer Science",
            ]
        ]
        session.add_all(subjects)

        students = [
            Student(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                group=random.choice(groups),
            )
            for _ in range(50)
        ]
        session.add_all(students)

        student_grades = []

        for student in students:
            for subject in subjects:
                grades_count = random.randint(1, 20)
                for _ in range(grades_count):
                    student_grades.append(
                        StudentGrade(
                            student=student,
                            subject=subject,
                            teacher=subject.teacher,
                            grade=random.randint(1, 100),
                            received_date=fake.date_this_year(),
                        )
                    )

        session.add_all(student_grades)

        session.commit()
    except Exception as er:
        session.rollback()
        raise er
