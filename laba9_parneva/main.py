from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from db import get_db, Base, engine
from schemas import UserCreate, UserUpdate, PostCreate, PostUpdate
from services.user import UserService
from services.post import PostService

app = FastAPI()

templates = Jinja2Templates(directory="pages")
app.mount("/static", StaticFiles(directory="static"), name="static")

Base.metadata.create_all(bind=engine)

#Пользователи (API) 
@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.create_user(user)


@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_all_users()


@app.put("/users/{user_id}")
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    service = UserService(db)
    user = service.update_user(user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    success = service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": f"User with ID {user_id} deleted"}

# Пользователи (Веб) 
@app.get("/users/web/")
def list_users(request: Request, db: Session = Depends(get_db)):
    service = UserService(db)
    users = service.get_all_users()
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get("/users/web/new")
def new_user_form(request: Request):
    return templates.TemplateResponse("user_form.html", {"request": request})


@app.post("/users/web/")
def create_user_via_form(
    username: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)
):
    service = UserService(db)
    service.create_user(UserCreate(username=username, email=email, password=password))
    return RedirectResponse(url="/users/web/", status_code=303)


@app.get("/users/web/edit/{user_id}")
def edit_user_form(user_id: int, request: Request, db: Session = Depends(get_db)):
    service = UserService(db)
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("user_edit_form.html", {"request": request, "user": user})


@app.post("/users/web/edit/{user_id}")
def update_user_via_form(
    user_id: int, username: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)
):
    service = UserService(db)
    service.update_user(user_id, {"username": username, "email": email, "password": password})
    return RedirectResponse(url="/users/web/", status_code=303)


@app.get("/users/web/delete/{user_id}")
def delete_user_via_form(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    service.delete_user(user_id)
    return RedirectResponse(url="/users/web/", status_code=303)

# Посты (API) 
@app.post("/posts/")
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    service = PostService(db)
    return service.create_post(post)


@app.get("/posts/")
def read_posts(db: Session = Depends(get_db)):
    service = PostService(db)
    return service.get_all_posts()


@app.put("/posts/{post_id}")
def update_post(post_id: int, post_update: PostUpdate, db: Session = Depends(get_db)):
    service = PostService(db)
    post = service.update_post(post_id, post_update)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    service = PostService(db)
    success = service.delete_post(post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": f"Post with ID {post_id} deleted"}

# Посты (Веб)
@app.get("/posts/web/")
def list_posts(request: Request, db: Session = Depends(get_db)):
    service = PostService(db)
    posts = service.get_all_posts()
    return templates.TemplateResponse("posts.html", {"request": request, "posts": posts})


@app.get("/posts/web/new")
def new_post_form(request: Request, db: Session = Depends(get_db)):
    service = UserService(db)
    users = service.get_all_users()
    return templates.TemplateResponse("post_form.html", {"request": request, "users": users})


@app.post("/posts/web/")
def create_post_via_form(
    title: str = Form(...), content: str = Form(...), user_id: int = Form(...), db: Session = Depends(get_db)
):
    service = PostService(db)
    service.create_post(PostCreate(title=title, content=content, user_id=user_id))
    return RedirectResponse(url="/posts/web/", status_code=303)


@app.get("/posts/web/edit/{post_id}")
def edit_post_form(post_id: int, request: Request, db: Session = Depends(get_db)):
    service = PostService(db)
    post = service.get_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse("post_edit_form.html", {"request": request, "post": post})


@app.post("/posts/web/edit/{post_id}")
def update_post_via_form(
    post_id: int, title: str = Form(...), content: str = Form(...), db: Session = Depends(get_db)
):
    service = PostService(db)
    service.update_post(post_id, {"title": title, "content": content})  
    return RedirectResponse(url="/posts/web/", status_code=303)


@app.get("/posts/web/delete/{post_id}")
def delete_post_via_form(post_id: int, db: Session = Depends(get_db)):
    service = PostService(db)
    service.delete_post(post_id)
    return RedirectResponse(url="/posts/web/", status_code=303)
