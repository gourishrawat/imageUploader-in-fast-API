from fastapi import APIRouter, Depends, UploadFile, File, status, HTTPException
from .models import *
from slugify import slugify
from .pydantic_models import categoryitem
from datetime import datetime, timedelta
import os

router = APIRouter()


@router.post("/category/")
async def create_category(data: categoryitem = Depends(),
                          caregory_imag: UploadFile = File(...)):
    if await Category.exists(name=data.name):
        return {"status": False, "message": "category alerady exists"}
    else:
        slug = slugify(data.name)
        FILEPATH = 'static/image'

        if not os.path.isdir(FILEPATH):
            os.mkdir(FILEPATH)
        filename = caregory_imag.filename
        extension = filename.split(".")[1]
        imagename = filename.split(".")[0]

        if extension not in ["png", "jpg", "jpeg"]:
            return {"status": "error", "detail": "file extention not allowed"}

        dt = datetime.now()
        dt_timestamp = round(datetime.timestamp(dt))

        modified_image_name = imagename+"_"+str(dt_timestamp)+"."+extension
        genrated_name = FILEPATH+modified_image_name
        file_content = await caregory_imag.read()

        category_obj = await Category.create(
            category_image=genrated_name,
            description=data.description,
            name=data.name,
            slug=slug
        )
        return category_obj