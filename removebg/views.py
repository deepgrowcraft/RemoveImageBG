import io

from django.http import HttpResponse
from PIL import Image, ImageEnhance, ImageFilter
from rembg import new_session, remove
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .secret import (
    require_client_secret,
)  # Assuming the decorator is in a module named `authentication_decorators`

# Create a session with the U2Net model, you can try different models for accuracy vs speed trade-off
session = new_session(
    "u2net"
)  # You can also use "u2net_human_seg" if you are working with human images.


@api_view(["POST"])
@require_client_secret
def remove_background(request):
    if "image" not in request.FILES:
        return Response(
            {"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    uploaded_image = request.FILES["image"]

    # Open the uploaded image and determine its format
    img = Image.open(uploaded_image)
    img_format = img.format

    # Resize large images moderately for performance, but not overly aggressive to avoid blur
    max_dimension = max(img.size)
    if max_dimension > 1500:  # Resize only if larger than 1500px
        resize_factor = 1500 / max_dimension
        new_size = (int(img.width * resize_factor), int(img.height * resize_factor))
        img = img.resize(new_size, Image.Resampling.LANCZOS)

    # Convert the image to bytes and process with rembg
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format=img_format)

    # Remove background using the rembg model session
    result = remove(img_byte_arr.getvalue(), session=session)

    # Convert the result back to an image, keeping transparency
    img_result = Image.open(io.BytesIO(result))

    # Apply Image Enhancements to improve quality, but without making it blurry

    # Apply light sharpening to enhance edges without overdoing it
    img_result = img_result.filter(
        ImageFilter.UnsharpMask(radius=1, percent=125, threshold=3)
    )

    # Enhance contrast slightly to avoid over-processing
    enhancer = ImageEnhance.Contrast(img_result)
    img_result = enhancer.enhance(1.2)  # Adjust contrast, but keep it moderate

    # Enhance brightness slightly, but don't over-brighten
    enhancer = ImageEnhance.Brightness(img_result)
    img_result = enhancer.enhance(
        1.05
    )  # Small brightness boost to maintain natural look

    # Optionally enhance color saturation slightly to make the image more vivid
    enhancer = ImageEnhance.Color(img_result)
    img_result = enhancer.enhance(1.1)  # Small color boost for natural tones

    # Convert the processed image to bytes and prepare the response
    img_io = io.BytesIO()

    # Ensure we save it in a format that supports transparency like PNG
    img_result.save(img_io, format="PNG")
    img_io.seek(0)

    # Send the processed image back as a response
    response = HttpResponse(img_io, content_type="image/png")
    response["Content-Disposition"] = 'attachment; filename="image_without_bg.png"'

    return response
