"""
Wrapper to handle performing a task and its status
"""


def do_task(task, model, uuid):
    """
    The function
    """
    ### Initialise
    instance = model.objects.get(pk=uuid)
    instance.processing_status = 'pending'
    instance.save()

    try:
        ### Perform the computations
        task(instance)

        ### End
        instance.processing_status = 'done'
        instance.save()
    except Exception as error:
        instance.processing_status = 'failed'
        instance.save()
        raise error
