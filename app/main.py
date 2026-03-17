from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from . import models, schemas, crud, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Movie Database API")


@app.get("/")
def root():
    return {"message": "Movie Database API is running"}


@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = auth.hash_password(user.password)
    new_user = crud.create_user(db, user.username, hashed_password)
    return {"message": f"User {new_user.username} created successfully"}


@app.post("/login", response_model=schemas.TokenResponse)
def login(user: schemas.LoginRequest, db: Session = Depends(get_db)):
    authenticated_user = auth.authenticate_user(db, user.username, user.password)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = auth.create_access_token(data={"sub": authenticated_user.username})
    return {"access_token": token, "token_type": "bearer"}


@app.post("/movies", response_model=schemas.MovieResponse)
def create_movie(
    movie: schemas.MovieCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    return crud.create_movie(db, movie)


@app.get("/movies", response_model=list[schemas.MovieResponse])
def read_movies(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    return crud.get_movies(db)


@app.get("/movies/{movie_id}", response_model=schemas.MovieResponse)
def read_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    movie = crud.get_movie(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@app.put("/movies/{movie_id}", response_model=schemas.MovieResponse)
def update_movie(
    movie_id: int,
    movie: schemas.MovieUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    updated_movie = crud.update_movie(db, movie_id, movie)
    if not updated_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return updated_movie


@app.delete("/movies/{movie_id}")
def delete_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    deleted_movie = crud.delete_movie(db, movie_id)
    if not deleted_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": "Movie deleted successfully"}