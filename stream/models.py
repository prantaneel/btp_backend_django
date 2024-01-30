from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Process(models.Model):
    p_id = models.CharField(max_length=20, unique=True)
    strategy = models.CharField(max_length=20, unique=False)

class Device(BaseModel):
    device_id = models.CharField(max_length=100)
    # Add other device properties
    process = models.ForeignKey(Process, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    def __str__(self):
        return self.device_id


class Measurement(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    #will be used for process id
    process = models.ForeignKey(Process, on_delete=models.CASCADE)
    iteration = models.FloatField()
    high_cost_data = models.FloatField(null=True)
    low_cost_data = models.JSONField()
    w_iter = models.JSONField()
    mse = models.FloatField(default=0)
    # Add other measurement properties

class ConsolidatedMSE(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    process = models.ForeignKey(Process, on_delete=models.CASCADE)
    iteration = models.FloatField()
    mse_array = models.JSONField()
