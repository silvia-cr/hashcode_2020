class Book(object):

    def __init__(self, id: int, score: int):
        self.id = int(id)
        self.score = int(score)
        self.scanned = False

    def scan(self):
        self.scanned = True

    def can_scan(self):
        return not self.scanned

    def __repr__(self):
        # return f'\n(Book {str(self.id)}: {str(self.score)})'
        return f'B{self.id}'


class Library(object):

    def __init__(self, id: int, signup_time: int, books_day: int, books: [Book]):
        self.id = int(id)
        self.signup_time = int(signup_time)
        self.books_day = int(books_day)
        self.books = books
        self.signed_up_start_day = -1

    def start_sign_up(self, current_day):
        self.signed_up_start_day = current_day

    def is_not_signed_up(self):
        return self.signed_up_start_day < 0

    def is_signing_up(self, current_day):
        return self.signed_up_start_day > -1 and current_day < self.signed_up_start_day + self.signup_time

    def is_signed_up(self, current_day):
        return self.signed_up_start_day > -1 and current_day >= self.signed_up_start_day + self.signup_time

    def scan_books(self):
        pending_books = [pending_book for pending_book in self.books if pending_book.can_scan()]
        scanned_books = set()
        books_to_scan = []
        points = 0

        if pending_books and len(pending_books) >= self.books_day:
            books_to_scan = pending_books[:self.books_day]
        elif pending_books:
            books_to_scan = pending_books

        for book in books_to_scan:
            book.scan()
            scanned_books.add(book)
            points += book.score

        return scanned_books, points

    def __repr__(self):
        # return f'\n[Library {str(self.id)}: Books: {self.books}]'
        return f'L{self.id}'
