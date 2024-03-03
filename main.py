from pymongo import MongoClient


client = MongoClient("mongodb://mongo:example@mongo")
db = client['mydb']


def create_collection(collection_name):
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)
        print("Коллекція '{}' створена.".format(collection_name))
    else:
        print("Коллекція '{}' уже існує.".format(collection_name))


collection_name = 'test_collection'
create_collection(collection_name)
collection = db[collection_name]


def create_document(name, age, features):
    document = {
        "name": name,
        "age": age,
        "features": features
    }
    result = collection.insert_one(document)
    print("Document inserted with ID:", result.inserted_id)

    return result.inserted_id


def read_collection():
    documents = collection.find()
    print("Виведення всіх документів колекції:")
    for document in documents:
        print(document)


def find_document_by_cat_name(cat_name):
    document = collection.find_one({"name": cat_name})
    if document:
        print("Документ знайдений:")
        print(document)
    else:
        print("Документ з даним іменем кота не знайдено.")


def update_cat_age_by_name(cat_name, new_age):
    result = collection.update_one({"name": cat_name}, {"$set": {"age": new_age}})
    if result.modified_count > 0:
        print("Вік кота оновлено.")
    else:
        print("Документ з даним іменем кота не знайдено.")


def add_feature_to_cat(name, new_feature):
    result = collection.update_one({"name": name}, {"$push": {"features": new_feature}})
    if result.modified_count > 0:
        print("Фіча додана.")
    else:
        print("Документ з даним іменем кота не знайдено.") 


def delete_cat_by_name(cat_name):
    result = collection.delete_one({"name": cat_name})
    if result.deleted_count > 0:
        print("Документ видалено.")
    else:
        print("Документ з даним іменем кота не знайдено.")


def delete_all():
    result = collection.delete_many({})
    print("Кількість видалених документів: ", result.deleted_count)


def main():
    create_document("barsik", 3, ["ходить в капці", "дає себе гладити", "рудий"])
    create_document("murchyk", 4, ["чоний", "дряпає диван", "пушистий"])
    create_document("tom", 7, ["ловить мишей", "сірий"])
    create_document("petro", 2, ["любить велер'яну", "кусається", "білий"])
    read_collection()

    while True:
        print("Пошук кота за іменем.")
        cat_name = input("Введіть ім'я кота: ")
        if not cat_name:
            print("Помилка введення.")
            continue
        find_document_by_cat_name(cat_name)
        break

    while True:
        print("Змінення віку кота.")
        cat_name = input("Введіть ім'я кота: ")
        new_age = input("Введіть новий вік кота: ")
        if not cat_name or not new_age.isdigit():
            print("Помилка введення.")
            continue
        update_cat_age_by_name(cat_name, int(new_age))
        break


    while True:
        print("Додавання нової фічі коту.")
        cat_name = input("Введіть ім'я кота: ")
        new_feature = input("Введіть нову фічу кота: ")
        if not cat_name or not new_feature:
            print("Помилка введення.")
            continue
        add_feature_to_cat(cat_name, new_feature)
        break


    while True:
        print("Видалення кота по імені.")
        cat_name = input("Введіть ім'я кота: ")
        if not cat_name:
            print("Помилка введення.")
            continue
        delete_cat_by_name(cat_name)
        break


    read_collection()
    print("Видалення всіх документів.")
    delete_all()


if __name__ == "__main__":
    main()
