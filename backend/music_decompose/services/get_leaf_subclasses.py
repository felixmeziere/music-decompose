def get_leaf_subclasses(cls):
    """
    Recursively get all leaf subclasses of a class
    """

    all_subclasses = []
    for subclass in cls.__subclasses__():
        if not subclass.__subclasses__():
            all_subclasses.append(subclass)
        all_subclasses.extend(get_leaf_subclasses(subclass))
    return all_subclasses
