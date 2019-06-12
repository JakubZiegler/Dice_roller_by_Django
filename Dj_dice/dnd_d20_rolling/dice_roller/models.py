from django.db import models


# Create your models here.
class roll(models.Model):
    d_amount = models.IntegerField()
    d_type = models.IntegerField()
    attack_bonus = models.IntegerField()
    dmg_bonus = models.IntegerField()
    advatage_bonus = models.NullBooleanField()
    critic_bonus = models.NullBooleanField()
    attack_result = models.IntegerField()
    dmg_result = models.IntegerField()
