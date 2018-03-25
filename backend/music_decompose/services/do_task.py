"""
Wrapper to handle performing a task and its status
"""


def do_task(task, model, status_field, uuid):
    """
    The function
    """
    ### Initialise
    instance = model.objects.get(pk=uuid)
    setattr(instance, status_field, 'pending')
    instance.save()

    try:
        ### Perform the computations
        task(instance)

        ### End
        setattr(instance, status_field, 'done')
        instance.save()
    except Exception as error:
        setattr(instance, status_field, 'failed')
        instance.save()
        raise error
