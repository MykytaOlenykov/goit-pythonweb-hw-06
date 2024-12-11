from datetime import date

from sqlalchemy import Integer, String, Date, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id", ondelete="RESTRICT"))

    group: Mapped["Group"] = relationship(back_populates="students")
    grades: Mapped[list["StudentGrade"]] = relationship(back_populates="student")


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

    students: Mapped[list["Student"]] = relationship(back_populates="group")


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))

    subjects: Mapped[list["Subject"]] = relationship(back_populates="teacher")
    student_grades: Mapped[list["StudentGrade"]] = relationship(
        back_populates="teacher"
    )


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    teacher_id: Mapped[int | None] = mapped_column(
        ForeignKey("teachers.id", ondelete="RESTRICT"),
        nullable=True,
        default=None,
    )

    teacher: Mapped["Teacher | None"] = relationship(back_populates="subjects")
    student_grades: Mapped[list["StudentGrade"]] = relationship(
        back_populates="subject"
    )


class StudentGrade(Base):
    __tablename__ = "student_grades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("students.id", ondelete="RESTRICT"),
    )
    subject_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("subjects.id", ondelete="RESTRICT"),
    )
    teacher_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("teachers.id", ondelete="RESTRICT"),
    )
    grade: Mapped[int] = mapped_column(Integer)
    received_date: Mapped[date] = mapped_column(Date)

    student: Mapped["Student"] = relationship(back_populates="grades")
    subject: Mapped["Subject"] = relationship(back_populates="student_grades")
    teacher: Mapped["Teacher"] = relationship(back_populates="student_grades")
