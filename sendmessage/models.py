from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Учетная запись отправителя")
    email = models.EmailField("Эл. почта получателя", max_length=100)
    message = models.TextField("Сообщение", max_length=200)
    status = models.BooleanField("Статус доставки", default=False)

    def __str__(self):
        return f"Сообщение от {self.user}"

    def loadtestsettings(self):
        import os
        import json
        settings_file = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/admin_emails_for_test.json'
        with open(settings_file) as emails_list:
            return json.load(emails_list)["admin_emails_list"]

    def setstatus(self, email):
        if email in self.loadtestsettings():
            self.status = True
