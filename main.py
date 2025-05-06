from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from api.auth_routes import router as auth_router
from api.file_routes import router as file_router


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(file_router, prefix="/files", tags=["File Management"])


@app.get("/")
def root():
    return {"message": "service is running"}
