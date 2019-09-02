class Restaurant:
    def __init__(self, restaurant_id, name, address, category, wait_times):
        self.id = restaurant_id
        self.name = name
        self.address = address
        self.category = category
        self.wait_times = wait_times


def from_document(document):
    """
    Take a cursor object (document) and convert it to a Restaurant object
    :param document: Document found from collection
    :return: Restaurant object
    """
    values = document.values()
    values = list(values)
    return Restaurant(str(values[0]), values[1], values[2], values[3], values[4])
