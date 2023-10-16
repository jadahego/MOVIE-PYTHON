from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, base
from middlewares.error_handler import ErrorHandler
from routers.move import movie_router
from routers.login import login_router

app = FastAPI()
app.title = 'Mi aplicacion con FastAPI'
app.version = '0.0.1'

app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(login_router)

base.metadata.create_all(bind=engine)


        
movies = [
    {
		"id": 1,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	},
    {
		"id": 2,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	}
]

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>hola mundo</h1>')



