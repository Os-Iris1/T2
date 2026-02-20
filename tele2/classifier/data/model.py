from django.db import models

class ChurnData(models.Model):
    state = models.CharField(max_length=2)
    account_length = models.IntegerField()
    area_code = models.IntegerField()
    international_plan = models.CharField(max_length=3)
    voice_mail_plan = models.CharField(max_length=3)
    number_vmail_messages = models.IntegerField()
    total_day_minutes = models.DecimalField(max_digits=10, decimal_places=2)
    total_day_calls = models.IntegerField()
    total_day_charge = models.DecimalField(max_digits=10, decimal_places=2)
    total_eve_minutes = models.DecimalField(max_digits=10, decimal_places=2)
    total_eve_calls = models.IntegerField()
    total_eve_charge = models.DecimalField(max_digits=10, decimal_places=2)
    total_night_minutes = models.DecimalField(max_digits=10, decimal_places=2)
    total_night_calls = models.IntegerField()
    total_night_charge = models.DecimalField(max_digits=10, decimal_places=2)
    total_intl_minutes = models.DecimalField(max_digits=10, decimal_places=2)
    total_intl_calls = models.IntegerField()
    total_intl_charge = models.DecimalField(max_digits=10, decimal_places=2)
    customer_service_calls = models.IntegerField()
    churn = models.BooleanField()

    class Meta:
        db_table = 'churn_data' 
        managed = False 