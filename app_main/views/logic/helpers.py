from typing import Any
from typing import Optional

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
            marks_current_class[str(lid)] = request.POST.get(
                f"{student.name}{student.lastname}_lesson{lid}"
            )
            student.save()
    classroom.save()


def delete_lesson(
    request: http.HttpRequest, classroom: models.ClassRoom
) -> None:
    lid = request.POST.get("deletelesson")
    student_delete_lesson(classroom, lid)
    if lid:
        intlid = int(lid)
    classroom_delete_lesson(classroom, intlid)


def student_delete_lesson(
    classroom: models.ClassRoom, lid: Optional[str]
) -> None:
    students = get_students_profiles_queryset(classroom)

    for student in students:
        marks = student.marks
        marks_current_class = marks[classroom.name]
        for lesid in marks_current_class:
            if lesid == lid:
                del marks_current_class[lesid]
                break
        student.save()


def classroom_delete_lesson(
    classroom: models.ClassRoom, intlid: Optional[int]
) -> None:
    for lesson in classroom.lessons:
        if lesson["id"] == intlid:
            classroom.lessons.remove(lesson)
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
        if les["date"]:
            date: str = ".".join(les.get("date").split("-")[::-1])
        else:
            date = les["date"]
        lessons.append(
            {
                "id": les.get("id"),
                "title": les.get("title"),
                "date": date,
                "dateform": les.get("date"),
            }
        )
    return lessons, l_count


def get_user_profile(request: http.HttpRequest) -> models.Profile:
    upk = request.user.id
    uprof = models.Profile.objects.get(user_id=upk)  # type: ignore
    return uprof


def get_user_role(request: http.HttpRequest) -> Any:
    if request.user.is_superuser or request.user.is_staff:
        return "director"
    uprof = get_user_profile(request)
    role = uprof.role
    return role


def get_current_student(
    request: http.HttpRequest, classroom: models.ClassRoom
) -> Optional[dict]:
    user_profile = get_user_profile(request)

    if user_profile.role != "student":
        return None

    mks = {
        str(les["id"]): user_profile.marks.get(classroom.name, {}).get(
            str(les["id"])
        )
        for les in classroom.lessons
    }
    for lsn in mks:
        if mks[lsn] is None:
            mks[lsn] = "null"
    current_student = {
        "name": user_profile.__str__(),
        "identifier": user_profile.name + user_profile.lastname,
    } | mks
    return current_student
