import json


def preprocess_text(ocr_text):
    import re

    def clean_text(text):
        text = text.lower()
        text = re.sub(r"^.*?ingredients:", "", text, flags=re.IGNORECASE).strip()
        text = re.sub(r"ingredients:", "", text, flags=re.IGNORECASE)
        text = re.sub(r"[^a-zA-Z, ]", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def split_ingredients(text):
        ingredients = text.split(",")
        ingredients = [ing.strip() for ing in ingredients if ing.strip()]
        return ingredients

    cleaned_text = clean_text(ocr_text)
    ingredients_list = split_ingredients(cleaned_text)
    return ingredients_list


# Vercel Python API handler
def handler(request):
    try:
        body = request.get_json()
        ocr_text = body.get("ocr_text", "")
        result = preprocess_text(ocr_text)
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"ingredients": result}),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)}),
        }
