from io import BytesIO
from fastapi import UploadFile
from PIL import Image
import aiofiles

from core.config import settings

async def add_watermark(avatar_file: UploadFile) -> BytesIO:
    watermark_path: str = settings.api.watermark_path

    async with aiofiles.open(watermark_path, 'rb') as f:
        watermark_data = await f.read()

    watermark = Image.open(BytesIO(watermark_data))

    avatar_image = Image.open(await avatar_file.read()).convert("RGBA")
    watermark = watermark.resize((avatar_image.width // 5, avatar_image.height // 5), Image.ANTIALIAS)

    avatar_image.paste(watermark, (0, 0), watermark)
    output = BytesIO()
    avatar_image.save(output, format="PNG")
    output.seek(0)
    return output



async def save_avatar(email: str, avatar: BytesIO):
    avatar_path = f"avatars/{email}.png"

    async with aiofiles.open(avatar_path, 'wb') as out_file:
        await out_file.write(avatar.read())