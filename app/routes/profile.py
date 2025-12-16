# from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
# from sqlalchemy.orm import Session
# from ..database import get_db
# from ..auth.jwt import get_current_user
# from ..models.users import User
# import os
# import uuid

# router = APIRouter(
#     prefix="/profile",
#     tags=["Profile"]
# )

# UPLOAD_DIR = "uploads/profile_pics"
# os.makedirs(UPLOAD_DIR, exist_ok=True)


# @router.post("/upload-picture")
# def upload_profile_picture(
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):

    
#     if not file.content_type.startswith("image/"):
#         raise HTTPException(
#             status_code=400,
#             detail="Invalid file type. Only images are allowed."
#         )

    
#     ext = file.filename.split(".")[-1]
#     filename = f"{uuid.uuid4()}.{ext}"
#     file_path = os.path.join(UPLOAD_DIR, filename)

    
#     with open(file_path, "wb") as buffer:
#         buffer.write(file.file.read())

    
#     if current_user.profile_picture:
#         old_path = os.path.join(UPLOAD_DIR, current_user.profile_picture)
#         if os.path.exists(old_path):
#             os.remove(old_path)

#     # Update user record
#     current_user.profile_picture = filename
#     db.commit()
#     db.refresh(current_user)

#     return {
#         "status": "success",
#         "message": "Profile picture uploaded successfully.",
#         "profile_picture_url": f"/uploads/profile_pics/{filename}"
#     }

# @router.get("/me")
# def get_my_profile(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     return {
#         "id": current_user.id,
#         "email": current_user.email,
#         "profile_picture_url":
#             f"/uploads/profile_pics/{current_user.profile_picture}"
#             if current_user.profile_picture else None
#     }
