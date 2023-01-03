from typing import Optional
from fastapi import FastAPI , Response , status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published :bool = True
    rating: Optional[int] = None

my_posts = [
    {"title" : "title of post 1" , "content" : "Content of post 1" , "id" : 1 },{"title" : "fav food" , "content" : "pizza content" , "id" : 2 }]

def findPost(id):
    for post in my_posts:
        # print(post["id"])
        if(post['id'] == id):
            print("found")
            return post
    return False


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"]==id:
            return i
        return None


@app.get("/")
def root():
    return {"message" : "Hello there"}  



@app.get("/posts")
def get_post():
    return {"data" : my_posts}


#create new post
@app.post("/posts" , status_code=status.HTTP_201_CREATED)
def create_posts(post : Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0 , 100000000)
    my_posts.append(post_dict)
    return {"data" : post_dict}


@app.get("/posts/{id}")
def get_post(id:int):
    post = findPost(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id: {id} not found")
    return post


# delete post
@app.delete("/posts/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index = find_index_post(id)
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id: {id} not found")
    my_posts.pop(index)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
 

@app.put("/posts/{id}")
def update_post(id:int , post:Post):
    print(post)
    index = find_index_post(id)
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id: {id} not found")
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"data" :post_dict}