"""
Celery tasks: functions runnable on separate async worker
"""
from celery import shared_task


@shared_task
def async_process_and_save(processor_uuid, processor_class_name):
    """
    Execute process_and_save in the background
    """
    from music_decompose.models import Processor
    ### Initialise
    processor_classes = Processor.__subclasses__()
    processor_names = [model.__name__ for model in processor_classes]
    processor_class = processor_classes[processor_names.index(processor_class_name)]
    processor = processor_class.objects.get(pk=processor_uuid)

    processor.processing_status = 'pending'
    processor.save()

    try:
        ### Perform the computations
        processor.process_and_save()

        ### End
        processor.processing_status = 'done'
        processor.save()
    except Exception as error:
        processor.processing_status = 'failed'
        processor.save()
        raise error
