import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.status import HTTP_401_UNAUTHORIZED

app = FastAPI()

secret_user: str = "stanley"
secret_password: str = "whodis?"

basic = HTTPBasic()


@app.get("/who")
def get_user(creds: HTTPBasicCredentials = Depends(basic)) -> dict:
    if creds.username == secret_user and creds.password == secret_password:
        return {"username": creds.username, "password": creds.password}

    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized")


if __name__ == "__main__":
    uvicorn.run("auth:app", reload=True)
