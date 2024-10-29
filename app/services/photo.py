from io import BytesIO
from fastapi import UploadFile
from PIL import Image
import aiofiles

from core.config import settings

async def add_watermark(avatar_file: UploadFile) -> BytesIO:
    watermark_path: str = settings.api.watermark_path

    async with aiofiles.open(watermark_path, 'rb') as f:
        watermark_data = await f.read()

    watermark = Image.open(BytesIO(watermark_data)).convert("RGBA")
    avatar_image_bytes = await avatar_file.read()
    avatar_image = Image.open(BytesIO(avatar_image_bytes)).convert("RGBA")

    watermark_size = (avatar_image.width // 5, avatar_image.height // 5)
    watermark = watermark.resize(watermark_size, Image.Resampling.LANCZOS)

    avatar_image.paste(watermark, (0, 0), watermark)
    output = BytesIO()
    avatar_image.save(output, format="PNG")
    output.seek(0)

    return output



async def save_avatar(email: str, avatar: BytesIO):
    avatar_path = f"avatars/{email}.png"

    async with aiofiles.open(avatar_path, 'wb') as out_file:
        await out_file.write(avatar.read())