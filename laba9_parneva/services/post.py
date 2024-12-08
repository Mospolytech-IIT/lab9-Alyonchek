from sqlalchemy.orm import Session
from repositories.post import PostRepository
from schemas import PostCreate, PostUpdate
from models import Post


class PostService:
    def __init__(self, db: Session):
        self.repo = PostRepository(db)

    def create_post(self, post_data: PostCreate) -> Post:
        return self.repo.create_post(
            title=post_data.title,
            content=post_data.content,
            user_id=post_data.user_id
        )

    def get_post(self, post_id: int) -> Post | None:
        return self.repo.get_post_by_id(post_id)
    
    def get_posts_by_user(self, user_id: int) -> list[Post]:
        return self.repo.get_posts_by_user(user_id)

    def get_all_posts(self) -> list[Post]:
        return self.repo.get_all_posts()

    def update_post(self, post_id: int, post_data: dict) -> Post | None:
        post = self.repo.get_post_by_id(post_id)
        if post:
            return self.repo.update_post(post, **post_data) 
        return None

    def delete_post(self, post_id: int) -> bool:
        post = self.repo.get_post_by_id(post_id)
        if post:
            self.repo.delete_post(post)
            return True
        return False
