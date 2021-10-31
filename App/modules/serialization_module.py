def serializeList(itemList):
    return [item.toDict() for item in itemList] if itemList else []