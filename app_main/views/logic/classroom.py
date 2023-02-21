import datetime
from typing import Any

from django import forms
from django import http
from django import shortcuts
from django import views
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from django.views import generic

from app_main import models
from app_main.forms import NewClassRoomForm
from app_main.helpers import get_all_teachers_as_choices
from app_main.helpers import marks
from app_main.mixins import LRMixin
from app_main.mixins import RoleUPTMixin

User = get_user_model()


class ClassesView(LRMixin, generic.ListView):
    model = models.ClassRoom
    template_name = "app_main/classeslist.html"

    def get_context_data(  # type: ignore
        self, *, object_list=None, **kwargs: dict
    ) -> dict:
        ctx = super().get_context_data()
        from app_main.views.logic import helpers

        u_role = helpers.get_user_role(self.request)
        ctx["user_role"] = u_role
        return ctx

    def get_queryset(self) -> QuerySet:
        profile = models.Profile.objects.get(  # type: ignore
            user_id=self.request.user.pk
        )
        user = User.objects.get(id=self.request.user.pk)  # type: ignore
        if profile.role == "director" or user.is_superuser or user.is_staff:
            return super().get_queryset()  # type: ignore
        from app_main.views.logic.helpers import get_user_classrooms

        return get_user_classrooms(self.request, "self")  # type: ignore


class ClassRoomView(LRMixin, generic.DetailView):
    def get(
        self, request: http.HttpRequest, *args: Any, **kwargs: dict
    ) -> http.HttpResponse:
        from app_main.views.logic import helpers

        user_role = helpers.get_user_role(request)

        classroom = models.ClassRoom.objects.get(slug=kwargs.get("slug"))

        if user_role == "student":
            permitted_rooms = helpers.get_user_classrooms(request, "self")
            if classroom not in permitted_rooms:  # type: ignore
                return super().handle_no_permission("permission")

        students = helpers.get_students_to_response(classroom)

        lessons, l_count = helpers.get_lessons_and_newlesid(classroom)

        current_student = helpers.get_current_student(
            request, classroom, "self"
        )

        response = shortcuts.render(
            self.request,
            "app_main/teacherclassroom.html",
            {
                "classroom": classroom,
                "students": students,
                "lessons": lessons,
                "marks": marks,
                "newles_title": "lesson" + str(l_count),
                "today": datetime.date.today().strftime("%Y-%m-%d"),
                "user_role": user_role,
                "current_student": current_student,
            },
        )
        return response


class ClassRoomEdit(LRMixin, RoleUPTMixin, views.View):
    role_required = "teacher"

    def post(
        self, request: http.HttpRequest, *args: Any, **kwargs: dict
    ) -> http.HttpResponseRedirect:
        classroom = models.ClassRoom.objects.get(slug=kwargs.get("slug"))
        from app_main.views.logic import helpers

        user_role = helpers.get_user_role(request)

        if request.POST.get("newlesson"):
            helpers.add_new_lesson(request, classroom)

        elif user_role != "director":
            self.handle_no_permission("permission")
            return shortcuts.redirect(f"/classes/{kwargs.get('slug')}")

        if request.POST.get("commitchanges"):
            helpers.edit_classroom(request, classroom)

        if request.POST.get("deletelesson"):
            helpers.delete_lesson(request, classroom)

        return shortcuts.redirect(f"/classes/{kwargs.get('slug')}")


class AddNewClassRoom(LRMixin, RoleUPTMixin, generic.FormView):
    role_required = "director"
    template_name = "app_main/classroom_form.html"
    form_class = NewClassRoomForm
    success_url = "/classes/"

    def form_valid(self, form: forms.Form) -> http.HttpResponse:
        response = super().form_valid(form)
        name = form.data["name"]
        try:
            _ = models.ClassRoom.objects.get(name=name)
            messages.warning(
                self.request,
                "this classroom name already exists",
            )
            return self.form_invalid(form)
        except ObjectDoesNotExist:
            pass
        teacher_id = form.data["teacher"]
        obj = models.ClassRoom(
            name=name,
            slug=name,
            teacher_id=teacher_id,
        )
        obj.save()
        students_id = self.request.POST.getlist("students_id")
        for sid in students_id:
            stud = User.objects.get(id=sid)
            stud.classroom_set.add(obj)
            stud.save()
        return response

    def get_context_data(self, **kwargs: dict) -> dict:
        ctx = super(AddNewClassRoom, self).get_context_data()
        ctx["students"] = User.objects.filter(profile__role="student")
        return ctx


class EditClassroomNameOrTeacher(LRMixin, RoleUPTMixin, generic.FormView):
    role_required = "director"
    success_url = "/classes/"
    template_name = "app_main/classroom_edit_form.html"
    form_class = forms.Form

    def form_valid(self, form: forms.Form) -> http.HttpResponse:
        classroom = models.ClassRoom.objects.get(slug=form.data["slug"])
        old_classroom_name = classroom.name[:]
        name = form.data["name"]
        try:
            _ = models.ClassRoom.objects.get(name=name)
            messages.warning(
                self.request,
                "this classroom name already exists",
            )
            return super().form_invalid(form)
        except ObjectDoesNotExist:
            pass
        teacher_id = form.data["teacher"]
        classroom.name = name
        classroom.slug = name
        classroom.teacher_id = teacher_id
        classroom.save()
        from app_main.views.logic.helpers import rename_students_classroom

        rename_students_classroom(classroom, old_classroom_name)
        self.success_url = f"/classes/{classroom.slug}/"
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> dict:
        ctx = super().get_context_data()
        slug = self.request.resolver_match.kwargs["slug"]  # type: ignore
        classroom = models.ClassRoom.objects.get(slug=slug)
        teacher = classroom.teacher.id, classroom.teacher.username
        teachers = get_all_teachers_as_choices()
        ctx.update(
            {
                "slug": slug,
                "teacher": teacher,
                "teachers": teachers,
            }
        )
        return ctx


class DeleteClassroom(  # type: ignore
    LRMixin, RoleUPTMixin, generic.DeleteView
):
    role_required = "director"
    success_url = "/classes/"
    model = models.ClassRoom

    def form_valid(self, form: forms.Form) -> http.HttpResponse:
        from app_main.views.logic.helpers import remove_students_classroom

        remove_students_classroom(self.object)
        return super().form_valid(form)
