import asyncio

from io import BytesIO
from fastapi import UploadFile
from PIL import Image
import aiofiles

from core.config import settings



def process_watermark(watermark_data: bytes, avatar_bytes: bytes) -> BytesIO:
    watermark = Image.open(BytesIO(watermark_data)).convert("RGBA")
    avatar_image = Image.open(BytesIO(avatar_bytes)).convert("RGBA")

    watermark_size = (avatar_image.width // 5, avatar_image.height // 5)
    watermark = watermark.resize(watermark_size, Image.Resampling.LANCZOS)

    avatar_image.paste(watermark, (0, 0), watermark)
    output = BytesIO()
    avatar_image.save(output, format="PNG")
    output.seek(0)
    return output




async def create_avatar(avatar_file: UploadFile) -> BytesIO:
    watermark_path: str = settings.api.watermark_path

    async with aiofiles.open(watermark_path, 'rb') as f:
        watermark_data = await f.read()

    avatar_image_bytes = await avatar_file.read()
    output = await asyncio.get_running_loop().run_in_executor(
        None,
        process_watermark,
        watermark_data,
        avatar_image_bytes
    )
    return output



async def save_avatar(email: str, avatar_file: UploadFile):
    avatar_path = f"avatars/{email}.png"

    avatar = await create_avatar(avatar_file=avatar_file)

    async with aiofiles.open(avatar_path, 'wb') as out_file:
        await out_file.write(avatar.read())