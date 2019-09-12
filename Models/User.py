class User:
    def __init__(self, user_id, email, password, role, favorite_food):
        self.id = user_id
        self.email = email
        self.password = password
        self.role = role
        self.favorite_food = favorite_food

def from_document(document):
    """
    Take a cursor object (document) and convert it to a User object
    :param document: Document found from collection
    :return: Restaurant object
    """
    values = document.values()
    values = list(values)

    return User(str(values[0]), values[1], values[2], values[3], values[4])
