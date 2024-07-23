import json


class Book:
    def __init__(self, id, title, author, year, status):
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.status = status


class Library:
    def __init__(self, data_file):
        self.data_file = data_file
        self.books = self.load_data()

    def load_data(self):
        try:
            with open(self.data_file, 'r', encoding='utf-8') as file:
                books_data = json.load(file)
                books = [Book(book['id'], book['title'], book['author'], book['year'], book['status']) for book in books_data]
                return books
        except FileNotFoundError:
            return []

    def save_data(self):
        books_data = [{'id': book.id, 'title': book.title, 'author': book.author, 'year': book.year, 'status': book.status} for book in self.books]
        with open(self.data_file, 'w', encoding='utf-8') as file:
            json.dump(books_data, file, ensure_ascii=False, indent=4)

    def add_book(self, title, author, year):
        book_id = len(self.books) + 1
        book = Book(book_id, title, author, year, "в наличии")
        self.books.append(book)
        self.save_data()
        print(f"Книга добавлена: {book.title} (id: {book.id})")

    def remove_book(self, book_id):
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.save_data()
                print(f"Книга с id {book_id} удалена.")
                return
        print(f"Книга с id {book_id} не найдена.")

    def find_books(self, keyword):
        found_books = []
        for book in self.books:
            if keyword.lower() in book.title.lower() or \
               keyword.lower() in book.author.lower() or \
               keyword == str(book.year):
                found_books.append(book)
        return found_books

    def display_all_books(self):
        if not self.books:
            print("В библиотеке нет книг.")
        else:
            print("Список книг в библиотеке:")
            for book in self.books:
                print(f"ID: {book.id}, Название: {book.title}, Автор: {book.author}, Год: {book.year}, Статус: {book.status}")

    def change_status(self, book_id, new_status):
        for book in self.books:
            if book.id == book_id:
                if new_status in ["в наличии", "выдана"]:
                    book.status = new_status
                    self.save_data()
                    print(f"Статус книги с id {book_id} изменен на '{new_status}'.")
                else:
                    print("Некорректный статус. Допустимые значения: 'в наличии' или 'выдана'.")
                return
        print(f"Книга с id {book_id} не найдена.")


# Функция для чтения целого числа с проверкой на корректность ввода
def read_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Пожалуйста, введите целое число.")


# Основная программа
def main():
    data_file = "library_data.json"
    library = Library(data_file)

    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")

        choice = read_int("Выберите действие (1-6): ")

        if choice == 1:
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = read_int("Введите год издания: ")
            library.add_book(title, author, year)

        elif choice == 2:
            book_id = read_int("Введите ID книги для удаления: ")
            library.remove_book(book_id)

        elif choice == 3:
            keyword = input("Введите название, автора или год издания для поиска: ")
            found_books = library.find_books(keyword)
            if found_books:
                print("Найденные книги:")
                for book in found_books:
                    print(f"ID: {book.id}, Название: {book.title}, Автор: {book.author}, Год: {book.year}, Статус: {book.status}")
            else:
                print("Книги по вашему запросу не найдены.")

        elif choice == 4:
            library.display_all_books()

        elif choice == 5:
            book_id = read_int("Введите ID книги для изменения статуса: ")
            new_status = input("Введите новый статус ('в наличии' или 'выдана'): ")
            library.change_status(book_id, new_status)

        elif choice == 6:
            print("Завершение работы.")
            break

        else:
            print("Некорректный ввод. Пожалуйста, выберите число от 1 до 6.")


if __name__ == "__main__":
    main()