from sqlalchemy.orm import Session
from models import Post


class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_post(self, title: str, content: str, user_id: int) -> Post:
        post = Post(title=title, content=content, user_id=user_id)
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post
    
    def get_posts_by_user(self, user_id: int) -> list[Post]:
        return self.db.query(Post).filter(Post.user_id == user_id).all()

    def get_post_by_id(self, post_id: int) -> Post | None:
        return self.db.query(Post).filter(Post.id == post_id).first()

    def get_all_posts(self) -> list[Post]:
        return self.db.query(Post).all()

    def update_post(self, post: Post, **kwargs) -> Post:
        for key, value in kwargs.items():
            if value is not None:
                setattr(post, key, value)  
        self.db.commit()
        self.db.refresh(post)
        return post

    def delete_post(self, post: Post):
        self.db.delete(post)
        self.db.commit()
