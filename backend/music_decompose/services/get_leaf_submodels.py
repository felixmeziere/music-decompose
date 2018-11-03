"""
Recursively get all leaf submodels of a class.
These are submodels of the class that aren't abstract
"""


def get_leaf_submodels(model):
    """
    Recursively get all leaf submodels of a model
    """
    all_submodels = []
    for submodel in model.__subclasses__():
        if not hasattr(submodel, '_meta') or submodel._meta.abstract is False:
            all_submodels.append(submodel)
        all_submodels.extend(get_leaf_submodels(submodel))
    return all_submodels
