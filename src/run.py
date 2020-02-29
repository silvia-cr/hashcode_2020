from models import Book, Library

filenames = [
    'examples/a_example.txt',
    # 'examples/b_read_ontxt',
    # 'examples/c_incunabula.txt',
    # 'examples/d_tough_choices.txt',
    # 'examples/e_so_many_books.txt',
    # 'examples/f_libraries_of_the_world.txt',
]


def build_books(scores_book: [int]):
    books = list()

    for idx, score_book in enumerate(scores_book):
        books.append(Book(idx, score_book))

    return books


def search_books_by_id(books, library_books_ids):
    library_books = set()

    for book_idx in library_books_ids:
        library_books.add(books[int(book_idx)])

    return library_books


def read_input(lines: [str]):
    idx = 0
    libraries = set()
    while idx < len(lines):
        if idx == 0:
            elements = lines[idx].split()
            n_books = elements[0]
            n_libraries = elements[1]
            days = elements[2]

            idx += 1
        elif idx == 1:
            books = build_books(lines[idx].split())

            idx += 1
        elif idx % 2 == 0:
            first_line_elements = lines[idx].split()
            second_line_elements = lines[idx+1].split()

            library_n_books = first_line_elements[0]
            library_signup = first_line_elements[1]
            library_books_day = first_line_elements[2]

            library_books = search_books_by_id(books, second_line_elements)

            library = Library(id=idx//2-1, signup_time=library_signup, books_day=library_books_day, books=library_books)
            libraries.add(library)

            if int(library_n_books) != len(library_books):
                raise Exception('Input data is not consistent')

            idx += 2

    if int(n_books) != len(books) or int(n_libraries) != len(libraries):
        raise Exception('Input data is not consistent')

    return books, libraries, days


if __name__ == '__main__':
    total = 0
    for filename in filenames:

        with open(filename, 'r') as file:
            lines = file.readlines()

        books, libraries, days = read_input(lines)

        # total += points

    print('Total: ' + str(total))
