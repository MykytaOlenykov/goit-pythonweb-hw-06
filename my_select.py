from sqlalchemy import select, func, and_
from tabulate import tabulate

from connect import session
from models import Student, Subject, StudentGrade, Group, Teacher


def select_1():
    student_columns = [Student.id, Student.first_name, Student.last_name]

    stmt = (
        select(
            *student_columns,
            func.avg(StudentGrade.grade).label("grade_avg"),
        )
        .join(Student)
        .group_by(*student_columns)
        .order_by(func.avg(StudentGrade.grade).desc())
        .limit(5)
    )
    return session.execute(stmt).mappings().all()


def select_2(subject: Subject):
    student_columns = [Student.id, Student.first_name, Student.last_name]

    stmt = (
        select(
            *student_columns,
            func.avg(StudentGrade.grade).label("grade_avg"),
        )
        .join(Student)
        .where(StudentGrade.subject_id == subject.id)
        .group_by(*student_columns)
        .order_by(func.avg(StudentGrade.grade).desc())
        .limit(1)
    )
    return session.execute(stmt).mappings().all()


def select_3(subject: Subject):
    stmt = (
        select(
            Group.id,
            Group.name,
            func.avg(StudentGrade.grade).label("grade_avg"),
        )
        .join(Group.students)
        .join(Student.grades)
        .where(StudentGrade.subject_id == subject.id)
        .group_by(Group.id)
        .order_by(Group.id)
    )
    return session.execute(stmt).mappings().all()


def select_4():
    stmt = select(
        func.avg(StudentGrade.grade).label("grade_avg"),
    )
    return session.execute(stmt).mappings().all()


def select_5(teacher: Teacher):
    stmt = select(Subject.id, Subject.name).where(Subject.teacher_id == teacher.id)
    return session.execute(stmt).mappings().all()


def select_6(group: Group):
    stmt = select(
        Student.id,
        Student.first_name,
        Student.last_name,
    ).where(Student.group_id == group.id)
    return session.execute(stmt).mappings().all()


def select_7(group: Group, subject: Subject):
    stmt = (
        select(
            Student.first_name,
            Student.last_name,
            StudentGrade.grade,
        )
        .join(Student)
        .join(Subject)
        .where(
            and_(
                Student.group_id == group.id,
                StudentGrade.subject_id == subject.id,
            )
        )
    )
    return session.execute(stmt).mappings().all()


def select_8(teacher: Teacher):
    teacher_columns = [Teacher.id, Teacher.first_name, Teacher.last_name]

    stmt = (
        select(
            *teacher_columns,
            func.avg(StudentGrade.grade).label("grade_avg"),
        )
        .join(Teacher)
        .where(StudentGrade.teacher_id == teacher.id)
        .group_by(*teacher_columns)
    )
    return session.execute(stmt).mappings().all()


def select_9(student: Student):
    subject_columns = [Subject.id, Subject.name]

    stmt = (
        select(*subject_columns)
        .join(StudentGrade)
        .where(StudentGrade.student_id == student.id)
        .group_by(*subject_columns)
        .order_by(Subject.id)
    )
    return session.execute(stmt).mappings().all()


def select_10(student: Student, teacher: Teacher):
    subject_columns = [Subject.id, Subject.name]

    stmt = (
        select(*subject_columns)
        .join(StudentGrade)
        .where(
            and_(
                StudentGrade.student_id == student.id,
                StudentGrade.teacher_id == teacher.id,
            )
        )
        .group_by(*subject_columns)
        .order_by(Subject.id)
    )
    return session.execute(stmt).mappings().all()


def print_list_data(data: list, title: str | None = None):
    if not data:
        return "Empty"

    headers = {k: k for k in data[0].keys()}

    print("\n")
    if title:
        print(title)
    print(tabulate(data, headers=headers, tablefmt="grid"))


if __name__ == "__main__":
    print_list_data(
        select_1(),
        title="1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.",
    )

    subject = session.get(Subject, 1)
    print_list_data(
        select_2(subject),
        title="2. Знайти студента із найвищим середнім балом з певного предмета.",
    )

    print_list_data(
        select_3(subject), title="3. Знайти середній бал у групах з певного предмета."
    )

    print_list_data(
        select_4(), title="4. Знайти середній бал на потоці (по всій таблиці оцінок)."
    )

    teacher = session.get(Teacher, 1)
    print_list_data(
        select_5(teacher), title="5. Знайти які курси читає певний викладач."
    )

    group = session.get(Group, 1)
    print_list_data(
        select_6(group),
        title="6. Знайти список студентів у певній групі.",
    )

    print_list_data(
        select_7(group, subject),
        title="7. Знайти оцінки студентів у окремій групі з певного предмета.",
    )

    print_list_data(
        select_8(teacher),
        title="8. Знайти середній бал, який ставить певний викладач зі своїх предметів.",
    )

    student = session.get(Student, 1)
    print_list_data(
        select_9(student),
        title="9. Знайти список курсів, які відвідує певний студент.",
    )

    print_list_data(
        select_10(student, teacher),
        title="10. Список курсів, які певному студенту читає певний викладач.",
    )
