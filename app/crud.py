from sqlalchemy.orm import Session
from . import models, schemas


def create_user(db: Session, username: str, hashed_password: str):
    user = models.User(username=username, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_movie(db: Session, movie: schemas.MovieCreate):
    db_movie = models.Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def get_movies(db: Session):
    return db.query(models.Movie).all()


def get_movie(db: Session, movie_id: int):
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()


def update_movie(db: Session, movie_id: int, movie: schemas.MovieUpdate):
    db_movie = get_movie(db, movie_id)
    if db_movie:
        for key, value in movie.dict().items():
            setattr(db_movie, key, value)
        db.commit()
        db.refresh(db_movie)
    return db_movie


def delete_movie(db: Session, movie_id: int):
    db_movie = get_movie(db, movie_id)
    if db_movie:
        db.delete(db_movie)
        db.commit()
    return db_movie