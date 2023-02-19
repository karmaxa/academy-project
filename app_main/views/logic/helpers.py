from django import http

from app_main import models


def get_students_profiles_queryset(classroom: models.ClassRoom) -> list:
    students: list = []
    student_users_raw = classroom.student.all()

    for stud in student_users_raw:
        prf = models.Profile.objects.get(user_id=stud.id)
        students.append(prf)

    return students


def add_new_lesson(
    request: http.HttpRequest, classroom: models.ClassRoom
) -> None:
    students = get_students_profiles_queryset(classroom)

    newles_title = request.POST.get("newlesson_title")
    list_id = [les["id"] for les in classroom.lessons]
    newles_id = len(classroom.lessons)

    while newles_id in list_id:
        newles_id += 1
    classroom.lessons.append(
        {
            "id": newles_id,
            "title": newles_title,
            "date": request.POST.get("newlesson_date"),
        }
    )
    classroom.save()

    for student in students:
        marks = student.marks
        try:
            marks_current_class = marks[classroom.name]
        except KeyError:
            student.marks[classroom.name] = {}
            marks_current_class = marks.get(classroom.name)
        marks_current_class[newles_id] = request.POST.get(
            f"{student.name}{student.lastname}_newlesson"
        )
        student.save()


def edit_classroom(
    request: http.HttpRequest, classroom: models.ClassRoom
) -> None:
    students = get_students_profiles_queryset(classroom)

    for lesson in classroom.lessons:
        lid = lesson["id"]
        ltitle = lesson["title"]
        newltitle = request.POST.get(f"{ltitle}_title")
        lesson["title"] = newltitle
        lesson["date"] = request.POST.get(f"{ltitle}_date")
        for student in students:
            marks = student.marks
            marks_current_class = marks.get(classroom.name)
            marks_current_class[lesson["id"]] = request.POST.get(
                f"{student.name}{student.lastname}_lesson{lid}"
            )
            student.save()
    classroom.save()


def get_students_to_response(classroom: models.ClassRoom) -> list:
    profile_students = get_students_profiles_queryset(classroom)

    students: list = []

    for stud in profile_students:
        mks = {
            str(les["id"]): stud.marks.get(classroom.name, {}).get(
                str(les["id"])
            )
            for les in classroom.lessons
        }
        for lsn in mks:
            if mks[lsn] is None:
                mks[lsn] = "null"
        students.append(
            {
                "name": stud.__str__(),
                "identifier": stud.name + stud.lastname,
            }
            | mks
        )
    return students


def get_lessons_and_newlesid(classroom: models.ClassRoom) -> tuple[list, int]:
    lessons: list = []
    l_count: int = 1

    for les in classroom.lessons:
        l_count += 1
        date: str = ".".join(les.get("date").split("-")[::-1])
        lessons.append(
            {
                "id": les.get("id"),
                "title": les.get("title"),
                "date": date,
                "dateform": les.get("date"),
            }
        )
    return lessons, l_count
