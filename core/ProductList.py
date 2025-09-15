# core/ProductList.py

import re
import google.generativeai as genai
from PIL import Image
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

# ==========================
# 1. Configure Gemini API
# ==========================
import os
GOOGLE_API_KEY = "AIzaSyCZ3hII3NJluBWUIX70akyG5vKX7KLKtdM"  # <-- your static API key
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# ==========================
# 2. API Endpoint
# ==========================
@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def analyze_product_image(request):
    """
    Upload an image → AI returns description + tags
    """
    if "image" not in request.FILES:
        return Response({"error": "No image uploaded"}, status=400)

    image_file = request.FILES["image"]

    try:
        pil_img = Image.open(image_file).convert("RGB")
    except Exception as e:
        return Response({"error": f"Invalid image: {str(e)}"}, status=400)

    # ==========================
    # 3. Prompt for Gemini
    # ==========================
    prompt = """
    You are an AI trained to analyze images.
    Look at the image and do the following:

    1. Provide a detailed description of the image in about 35 words.
       - Mention important visual elements, colors, shapes, and context.

    2. Suggest 8–12 relevant tags/keywords that describe the image’s content, style, and theme.
       - Prefix each tag with either # or @.
       - Keep them short, lowercase, and easy to use.
    """

    response = model.generate_content([prompt, pil_img])

    description = response.text.strip()
    tags = re.findall(r"(?:[#@]\w+)", description)
    clean_tags = [t.strip("#@").lower() for t in tags]

    return Response({
        "description": description,
        "tags": clean_tags
    })
