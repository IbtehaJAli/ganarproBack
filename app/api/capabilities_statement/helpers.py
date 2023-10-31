import cloudinary.uploader


def upload_to_cloudinary(file):
    try:
        cloudinary_upload = cloudinary.uploader.upload(file, public_id=file.name)
        return cloudinary_upload['secure_url']
    except:
        return None
