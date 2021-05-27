from django.db import models
import re

class UserManager(models.Manager):
    def register_validator(self, session_data, post_data, emails_list):
        errors = {}
        EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
        if len(post_data["first_name"]) < 2:
            errors["first_name_length"] = "First name should be at least 2 characters"
        elif not post_data["first_name"].isalpha():
            errors["first_name_letters"] = "First name should only contain letters"
        else:
            session_data["first_name"] = post_data["first_name"]
        if len(post_data["last_name"]) < 2:
            errors["last_name_length"] = "Last name should be at least 2 characters"
        elif not post_data["last_name"].isalpha():
            errors["last_name_letters"] = "Last name should only contain letters"
        else:
            session_data["last_name"] = post_data["last_name"]
        if len(post_data["alias"]) < 2:
            errors["alias_length"] = "Alias should be at least 2 characters"
        else:
            session_data["alias"] = post_data["alias"]
        if not EMAIL_REGEX.match(post_data["email"]):
            errors["invalid_email"] = "Invalid email address!"
        elif post_data["email"] in emails_list:
            errors["existing_email"] = "This email already exists!"
        else:
            session_data["email"] = post_data["email"]
        if len(post_data["password"]) < 8:
            errors["password_length"] = "Password should be at least 8 characters"
        if post_data["password"] != post_data["confirm_password"]:
            errors["password_confirmation"] = "Password confirmation doesn't match the password"
        return errors

    def login_validator(self, session_data, post_data, emails_list):
        errors = {}
        if post_data["email_login"] not in emails_list:
            errors["non_existing_email"] = "Unknown email"
        else:
            session_data["email_login"] = post_data["email_login"]
        return errors

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    alias = models.CharField(max_length=20)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    objects = UserManager()
