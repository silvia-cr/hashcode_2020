from models import Book, Library

filenames = [
    'examples/a_example.txt',
    'examples/b_read_on.txt',
    'examples/c_incunabula.txt',
    'examples/d_tough_choices.txt',
    'examples/e_so_many_books.txt',
    'examples/f_libraries_of_the_world.txt',
]


def build_books(scores_book: [int]):
    books = list()

    for idx, score_book in enumerate(scores_book):
        books.append(Book(idx, score_book))

    return books


def search_books_by_id(books, library_books_ids):
    library_books = list()

    for book_idx in library_books_ids:
        library_books.append(books[int(book_idx)])

    # sort books by book.score descendant
    library_books.sort(key=lambda book: book.score, reverse=True)
    return library_books


def read_input(lines: [str]):
    idx = 0
    libraries = list()
    while idx < len(lines):
        if len(lines[idx]) > 0:
            if idx == 0:
                elements = lines[idx].split()
                n_books = elements[0]
                n_libraries = elements[1]
                days = int(elements[2])

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
                libraries.append(library)

                if int(library_n_books) != len(library_books):
                    raise Exception('Input data is not consistent')

                idx += 2

    if int(n_books) != len(books) or int(n_libraries) != len(libraries):
        raise Exception('Input data is not consistent')

    # sort books by book.score descendant
    books.sort(key=lambda book: book.score, reverse=True)

    # sort libraries by library.signup_time ascendant
    libraries.sort(key=lambda library: library.signup_time, reverse=False)

    return books, libraries, days


def check_is_current_open_process(libraries, current_day):
    for library in libraries:
        if library.is_signing_up(current_day):
            return True

    return False


def start_sign_up_process(libraries, current_day):
    not_signed_up_libraries = [library for library in libraries if library.is_not_signed_up()]

    if not_signed_up_libraries:
        library_to_start_sign_up = not_signed_up_libraries[0]
        library_to_start_sign_up.start_sign_up(current_day)
        return library_to_start_sign_up

    return None


def get_daily_work(current_day, libraries):
    """
    Calculate the process per day per library.
    Return a list of tuple and the total points from this day.
    The list contains a tuple with each library that works this day (signing up or scanning)
    and the set of books scanned this day. If the scanned book list is empty, this day is the
    signing up process.

    :param current_day:
    :param libraries:
    :param books:
    :param all_daily_work:
    :return: [Tuple(Library, {Books})], int
    """
    signing_up_process = check_is_current_open_process(libraries=libraries, current_day=current_day)
    daily_points = 0

    daily = list()
    if not signing_up_process:
        library = start_sign_up_process(libraries=libraries, current_day=current_day)
        if library:
            daily.append((library, None))

    libraries_ready_to_scan = {library_ready for library_ready in libraries if library_ready.is_signed_up(current_day)}
    for library_ready in libraries_ready_to_scan:
        new_scanned_books, points = library_ready.scan_books()

        if new_scanned_books:
            daily.append((library_ready, new_scanned_books))
            daily_points += points

    return daily, daily_points


def get_selected_libraries(all_daily_work):
    tuple_list = []
    for daily_work in all_daily_work:
        tuple_list += daily_work

    return list({library for library, _ in tuple_list})


def write_library(library):
    output = f'{library.id} {len(library.scanned_books)}\n'
    output += f"{' '.join([str(book.id) for book in library.scanned_books])}\n"
    return output


def build_output(all_daily_work, filename):
    selected_libraries = get_selected_libraries(all_daily_work)

    output = f'{len(selected_libraries)}\n'
    for library in selected_libraries:
        output += write_library(library)

    with open(filename[:-4] + '_output.txt', 'w') as file:
        file.write(output)


if __name__ == '__main__':
    total = 0
    for filename in filenames:
        print(f'{filename}')

        with open(filename, 'r') as file:
            lines = file.readlines()

        books, libraries, days = read_input(lines)

        current_day = 0
        points = 0
        all_daily_work = list()
        while current_day < days:

            daily_work, daily_points = get_daily_work(current_day, libraries)

            all_daily_work.append(daily_work)
            points += daily_points
            current_day += 1
            
        build_output(all_daily_work=all_daily_work, filename=filename)

        print(f'{filename}: {points}')
        total += points

    print('Total: ' + str(total))
