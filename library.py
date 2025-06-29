import datetime

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Date
)
from sqlalchemy.orm import (
    declarative_base,
    relationship,
    sessionmaker
)

# Create a declarative base
Base = declarative_base()


# define the user model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # Establish a relationship
    books = relationship("Book", back_populates="borrower")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    due_date = Column(Date, nullable=True)  # ← NEW FIELD

    user_id = Column(Integer, ForeignKey("users.id"))  # ForeignKey("<__tablename__.field>
    borrower = relationship("User", back_populates="books")


def create_database():
    """Create the database and tables, and add initial data."""
    engine = create_engine('sqlite:///library.db', echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    print(f'Session instance created')
    return session


def add_book(title, session):
    book = Book(title=title)
    session.add(book)
    session.commit()
    print(f'Book added: {title}')


def add_user(name, session):
    user = User(name=name)
    session.add(user)
    session.commit()
    print(f'User added: {name}')


def show_books(session, only_borrowed=False):
    query = session.query(Book)

    if only_borrowed:
        query = query.filter(Book.user_id is None)

    books = query.all()
    print('Books:')
    print(f'{"ID":<4} {"Title":<12} {"Borrower":<12}    {"Due Date"}')
    print('-' * 50)
    for book in books:
        borrower_name = book.borrower.name if book.borrower else ""
        print(f'{book.id:<4} {book.title[:12]:<12}   {borrower_name[:12]:<12}    {book.due_date}')
    print()


def show_users(session):
    users = session.query(User).all()
    print('Users:')
    print(f'{"ID":<4} {"Name":<12}   {"Books Borrowed"}')
    print('-' * 50)
    for user in users:
        books_borrowed = ', '.join(b.title[:12] for b in user.books)
        print(f'{user.id:<4} {user.name[:12]:<12}   {books_borrowed}')
    print()


def borrow_book(username, title, due_days, session):
    show_users(session)
    user = session.query(User).filter_by(name=username).first()

    show_books(session, only_borrowed=True)
    book_added_flag = False

    if title.lower() in ('q', 'quit'):
        if book_added_flag:
            print("Committing books before exiting ...")
            session.commit()
        return

    book = session.query(Book).filter_by(title=title).first()
    if not book:
        print(f'Book: "{title}" does not exist')
        return

    if book.borrower:
        print(f'Book: "{title}" is already borrowed. Retrying...')
        return

    # Set due date
    book.due_date = datetime.date.today() + datetime.timedelta(days=due_days)

    book.borrower = user
    session.commit()
    print(f'User "{user.name}" has borrowed "{title}" ')


def get_users(session):
    return [
        {
            "id": user.id,
            "name": user.name,
            "borrowed": [book.title for book in user.books] if user.books else None
        }
        for user in session.query(User).all()
    ]


def get_books(session):
    return [
        {
            "id": book.id,
            "title": book.title,
            "borrower": book.borrower.name if book.borrower else None
        }
        for book in session.query(Book).all()
    ]


def reset_database():
    """Drop all tables and recreate them cleanly."""
    engine = create_engine('sqlite:///library.db', echo=False)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def seed_sample_data(session):
    for book in ['english', 'tamil', '1984', 'Mystery Islands', 'Heart Beat', 'Heart Beat 2',
                 'office', 'Kerala']:
        add_book(book, session)

    for user in ['swadhi', 'usha', 'sangamithra', 'reva', 'krithika', 'suji']:
        add_user(user, session)

    for user, book, days in [
        ('revan', 'Kerala', 10),
        ('swadhi', 'Heart Beat 2', 15),
        ('kirth', '1984', 13),
        ('swadhi', 'english', 5)
    ]:
        borrow_book(user, book, days, session)


def add_dummy_user(session):
    add_user('dummy_user', session)


def seed_overdue_books(session):
    dummy_user = 'dummy_user'
    books = session.query(Book).all()

    for book in books:
        if book.borrower is None:
            borrow_book(dummy_user, book.title, -100, session)

    print(f"Dummy over due dates set for user: {dummy_user}")

if __name__ == '__main__':
    # db_session = reset_database()
    db_session = create_database()
    # seed_overdue_books(db_session)
    # seed_sample_data(db_session)
    show_books(db_session)
    show_users(db_session)
