class Book(object):

    def __init__(self, id: int, score: int):
        self.id = id
        self.score = score

    def __repr__(self):
        return f'\n<Book {str(self.id)}: {str(self.score)}>'


class Library(object):

    def __init__(self, id: int, signup_time: int, books_day: int, books: {Book}):
        self.id = id
        self.signup_time = signup_time
        self.books_day = books_day
        self.books = books

    def __repr__(self):
        return f'[Library {str(self.id)}: Books: {self.books}]'
