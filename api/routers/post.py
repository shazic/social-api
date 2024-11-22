from fastapi import APIRouter, HTTPException
from models.post import Comment, CommentIn, UserPost, UserPostIn, UserPostWithComments

router = APIRouter()


post_table = {}
comments_table = {}


def find_post(post_id: int):
    return post_table.get(post_id)


@router.post("/post", response_model=UserPost)
async def create_post(post: UserPostIn):
    data = post.dict()
    last_record_id = len(post_table)
    new_post = {**data, "id": last_record_id}
    post_table[last_record_id] = new_post
    return new_post


@router.get("/post", response_model=list[UserPost])
async def get_posts():
    return list(post_table.values())
    return list(post_table.values())


@router.post("/comment", response_model=Comment)
async def create_comment(comment: CommentIn):
    post = find_post(comment.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    data = comment.dict()
    last_record_id = len(comments_table)
    new_comment = {**data, "id": last_record_id}
    comments_table[last_record_id] = new_comment
    return new_comment


@router.get("/post/{post_id}/comment", response_model=list[Comment])
async def get_comments_on_post(post_id: int):
    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return [
        comment for comment in comments_table.values() if comment["post_id"] == post_id
    ]


@router.get("/post/{post_id}", response_model=UserPostWithComments)
async def post_with_comments(post_id: int):
    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {
        "post": post,
        "comments": await get_comments_on_post(post_id),
    }
