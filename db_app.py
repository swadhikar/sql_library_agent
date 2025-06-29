# Imports
from typing import Union
import os.path

from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.exc import IntegrityError

# Create database
engine = create_engine("sqlite:///tasks.db", echo=False)

# Create global variables
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
DB_CREATED = os.path.exists('misc/tasks.db')


# Define Models/Tasks
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    # Foreign key
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")  # user table


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    description = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    due_date = Column(Date, nullable=True)

    # Foreign key
    user = relationship("User", back_populates="tasks")  # tasks table


# Create database, session and tables
def create_database():
    # Create tables
    if not DB_CREATED:
        Base.metadata.create_all(engine)
        print(f"Database created")
    else:
        print(f"Database already exists!")


# Important utility functions
def get_user_by_email(email: str) -> Union[User, None]:
    """
    The function returns a User object given an email address

    Args:
        email: unique email address of the user

    Returns:
        User instance if email exists, else None
    """
    return session.query(User).filter_by(email=email).first()


def confirm_action(prompt: str) -> bool:
    return input(f"{prompt} (yes/no): ").lower() in ('yes', 'y')


# CRUD Operations
def add_user():
    """
    Gets the user's name and email from input prompt to create a record in users tables

    Returns:
        True if successful, False otherwise
    """
    name, email = input("Enter user name: "), input("Enter the email address: ")

    if email.strip() == '':
        print("No email provided. Not creating user!\n")
        return

    if get_user_by_email(email):
        print(f"User already exists: {name}\n")
        return

    try:
        new_user = User(name=name, email=email)
        session.add(new_user)
        session.commit()
        print(f"User created successfully: {name}\n")
    except IntegrityError as e:
        print(f"Failed to create user. Error: {e}\n")


def query_users():
    users = session.query(User).all()

    print("Users:")

    for user in users:
        print(f'User ID: {user.id}, Name: {user.name}, Email: {user.email}')


def add_tasks():
    email = input(f"Enter the email of the user to add task: ")

    if email.strip() == '':
        print("No email provided. Not adding tasks!\n")
        return

    user = get_user_by_email(email)

    if not user:
        print(f"No user found with email: {email}\n")
        return

    while True:
        try:
            title, desc = input("Enter title: "), input("Enter Description: ")
            new_task = Task(title=title, description=desc, user=user)
            session.add(new_task)
            session.commit()
            print(f"Task added successfully!\n")

            if not confirm_action('Do you wish to add more tasks?'):
                break

        except IntegrityError as e:
            print(f"Failed to create user. Error: {e}")
            return


def query_tasks():
    email = input(f"Enter the email of the user to list tasks: ")

    if email.strip() == '':
        print("No email provided. Not querying tasks!\n")
        return

    user = get_user_by_email(email)

    if not user:
        print(f"No user found with email: {email}")
        return

    tasks = session.query(Task).filter_by(user_id=user.id)

    for task in tasks:
        print(f"Task ID: {task.id}, Title: {task.title}, Desc: {task.description}")


def main():
    create_database()
    add_user()
    query_users()
    add_tasks()
    query_tasks()


if __name__ == '__main__':
    main()
