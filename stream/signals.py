from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from asgiref.sync import async_to_sync
import json
from channels.layers import get_channel_layer
from .models import ConsolidatedMSE
from django.forms.models import model_to_dict

from .models import Device, Measurement

@receiver(post_save, sender=Device)
def device_created(sender, instance, created, **kwargs):
    if created:
        # print("Device is created")
        # Device created signal
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"{instance.device_id}",
            {
                "type": "device.created",
                "device_id": instance.device_id,
                "p_id": instance.process.p_id,
                "completed": instance.completed
            }
        )
@receiver(post_save, sender = Device)
def device_completed(sender, instance, **kwargs):
    #iteration completed
    updated_fields = kwargs.get('update_fields')
    if instance.completed == True:
        channel_layer = get_channel_layer()
        cmse = ConsolidatedMSE.objects.get(device=instance, process=instance.process)
        async_to_sync(channel_layer.group_send)(
            f"{instance.device_id}",
            {
                "type": "device.completed",
                "device_id": instance.device_id,
                "p_id": instance.process.p_id,
                "completed": instance.completed,
                "cmse": cmse.mse_array,
            }
        )
        

@receiver(post_save, sender=Measurement)
def measurement_created(sender, instance, created, **kwargs):
    if created:
        # print("created Device data update", instance.device.device_id)
        # Measurement created signal
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"{instance.device.device_id}",
            {
                "type": "measurement.created",
                "device_id": instance.device.device_id,
                "iteration": instance.iteration,
                "mse": instance.mse,
            }
        )

@receiver(pre_delete, sender=Device)
def device_deleted(sender, instance, **kwargs):
    # Device deleted signal
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"{instance.device_id}",
        {
            "type": "device.deleted",
            "device_id": instance.device_id,
        }
    )