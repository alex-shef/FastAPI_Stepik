from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

from sql_app import schemas, crud
from sql_app.auth import get_current_user
from sql_app.database import get_db

router = APIRouter()


@router.post("/users/items/", response_model=schemas.Item, tags=["admin", "user"])
async def create_item(current_user: Annotated[schemas.User, Depends(get_current_user)],
                      item_create: schemas.ItemCreate, db: Session = Depends(get_db)):
    if current_user.role not in ["admin", "user"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
    return await crud.create_item(user_id=current_user.id, item_create=item_create, db=db)


@router.get("/items/", response_model=list[schemas.Item])
async def get_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = await crud.get_items(skip=skip, limit=limit, db=db)
    return items


@router.get("/items/{item_id}", response_model=schemas.Item)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    db_item = await crud.get_item(item_id=item_id, db=db)
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return db_item


@router.put("/items/{item_id}", response_model=schemas.Item, tags=["admin", "user"])
async def update_item(current_user: Annotated[schemas.User, Depends(get_current_user)],
                      item_id: int, item_update: schemas.ItemUpdate, db: Session = Depends(get_db)):
    db_item = await crud.get_item(item_id=item_id, db=db)
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    if current_user.role != "admin" or db_item.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
    db_item = await crud.update_item(item_id=item_id, item_update=item_update, db=db)
    return db_item


@router.delete("/items/{item_id}", response_model=schemas.Item, tags=["admin", "user"])
async def delete_item(current_user: Annotated[schemas.User, Depends(get_current_user)],
                      item_id: int, db: Session = Depends(get_db)):
    db_item = await crud.get_item(item_id=item_id, db=db)
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    if current_user.role != "admin" or db_item.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
    db_item = await crud.delete_item(item_id=item_id, db=db)
    return db_item
