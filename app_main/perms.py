from django.db import models


class Student(models.Model):
    class Meta:
        permissions = [
            ("view_self", "Can view self marks"),
        ]


class Teacher(models.Model):
    class Meta:
        permissions = [
            ("view_self_class", "Can view self class"),
            ("add_marks", "Can add marks to students"),
        ]


class Director(models.Model):
    class Meta:
        permissions = [
            ("view_classes", "Can view all classes"),
            ("view_class", "Can view any class"),
            ("edit_marks", "Can edit marks"),
            ("edit_user", "Can edit any user"),
            ("create_user", "Can create new users"),
            ("delete user", "Can delete new users"),
            ("view_students", "Can view all students"),
        ]
