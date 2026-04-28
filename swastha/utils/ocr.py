# utils/ocr.py
# eita lab report image theke text extract korar utility
# pytesseract use kore OCR kora hocche
# jodi pytesseract install na thake, sample text return kore (fallback)

import os

# pytesseract optional dependency — install na thakleo app cholbe
try:
    import pytesseract          # OCR engine wrapper
    from PIL import Image       # image open korar jonno Pillow library
    OCR_AVAILABLE = True
    print("[OCR] pytesseract successfully loaded!")
except ImportError:
    OCR_AVAILABLE = False
    print("[OCR WARNING] pytesseract ba Pillow install nai — OCR feature limited thakbe.")


# Windows e Tesseract executable er path set kora laghe
# Linux/Mac e usually auto detect hoy
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

if OCR_AVAILABLE and os.name == "nt":  # Windows check
    if os.path.exists(TESSERACT_PATH):
        pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
    else:
        print(
            "[OCR WARNING] Tesseract executable pawa jacche na Windows e.\n"
            "Download: https://github.com/UB-Mannheim/tesseract/wiki"
        )


def extract_text_from_image(image_path: str) -> str:
    """
    Image file er path niye OCR diye text extract kore return kore.
    jodi OCR available na thake, sample lab report text return kore testing er jonno.
    """
    if not OCR_AVAILABLE:
        # OCR nai, fake/sample lab data return koro testing er jonno
        print("[OCR] pytesseract nai — sample data use kora hocche")
        return _get_sample_lab_text()

    if not os.path.exists(image_path):
        return f"[ERROR] File pawa jacche na: {image_path}"

    try:
        # image open kore OCR run kora hocche
        img = Image.open(image_path)

        # image preprocess — better OCR accuracy er jonno
        img = img.convert("L")  # grayscale convert — noise kom kore

        # tesseract diye text extract kora hocche
        extracted_text = pytesseract.image_to_string(img, lang="eng")

        if extracted_text.strip():
            return extracted_text
        else:
            return "[OCR] Image theke text extract kora jacchilo na. Clear image upload korun."

    except Exception as e:
        print(f"[OCR ERROR] {e}")
        return f"[OCR ERROR] Text extract korte samashya: {e}"


def _get_sample_lab_text() -> str:
    """
    Testing er jonno ekটা sample lab report text return kore.
    Real OCR nai hole eita use hobe UI demo er jonno.
    """
    return """
    PATHOLOGY LABORATORY REPORT
    Patient: John Doe | Age: 45 | Date: 2024-01-15

    COMPLETE BLOOD COUNT (CBC)
    ---------------------------------
    Hemoglobin (HGB)    : 11.2 g/dL
    WBC                 : 12.5 x10^9/L
    RBC                 : 4.8 x10^12/L
    Platelets           : 145 x10^9/L

    BLOOD CHEMISTRY
    ---------------------------------
    Glucose             : 125 mg/dL
    Cholesterol         : 215 mg/dL
    LDL                 : 140 mg/dL
    HDL                 : 38 mg/dL
    Triglycerides       : 180 mg/dL
    Creatinine          : 1.4 mg/dL
    Urea                : 28 mg/dL
    SGPT (ALT)          : 65 U/L
    SGOT (AST)          : 45 U/L
    Bilirubin           : 0.9 mg/dL

    THYROID FUNCTION
    ---------------------------------
    TSH                 : 5.2 mIU/L
    T3                  : 95 ng/dL
    T4                  : 6.8 μg/dL

    *** Report ends ***
    """