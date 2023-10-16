from fastapi import APIRouter
from fastapi import Body, Path, Query, Depends
from fastapi.responses import JSONResponse
from typing import List
from config.database import session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()


@movie_router.get('/movies', tags=['Movies'], response_model= List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def ger_movies() -> List[Movie]:
    db = session()
    #result = db.query(MovieModel).all()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get('/movies/{id}', tags=['Movies'], response_model=Movie)
def get_movie(id: int = Path(ge = 1, le=2000)) -> Movie:
    db = session()
    #result = db.query(MovieModel).filter(MovieModel.id == id).first()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': 'id no esta en la base de dato'})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get('/movies/', tags=['Movies'], response_model= List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
     db = session()
     #result = db.query(MovieModel).filter(MovieModel.category == category).all()
     result = MovieService(db).get_movies_by_category(category)
     if not result:
        return JSONResponse(status_code=404, content={'message': 'categoria no esta en la base de dato'})
     return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.post('/movies', tags=['Movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = session()
    #new_movie = MovieModel(title=movie.title, overview=movie.overview, year=movie.year, rating=movie.rating, category=movie.category)
    #new_movie = MovieModel(**movie.dict())
    #db.add(new_movie)
    #db.commit()
    #movies.append(movie)
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code=201, content={'message': 'Se registro la pelicula con exito'})

@movie_router.put('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
def update_movie(id:int, movie: Movie) -> dict:
        db = session()
        #result= db.query(MovieModel).filter(MovieModel.id==id).first()
        result= MovieService(db).get_movie(id)
        if not result:
            return JSONResponse(status_code=404, content={'message': 'id no esta en la base de dato'})
        #result.title  = movie.title
        #result.overview = movie.overview
        #result.year  = movie.year
        #result.rating  = movie.rating
        #result.category = movie.category
        #db.commit()
        MovieService(db).update_movie(id, movie)
        return JSONResponse(status_code=200, content={'message': 'Se actualizo la pelicula con exito'})

@movie_router.delete('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
def delete_movie(id:int) -> dict:
    db = session()
    #result= db.query(MovieModel).filter(MovieModel.id==id).first()
    result= MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': 'id no esta en la base de dato'})
    #db.delete(result)
    #db.commit()
    MovieService(db).delete_movie(id)
    return JSONResponse(status_code=200, content={'message': 'Se elimino la pelicula con exito'})