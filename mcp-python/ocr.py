from PIL import Image
import pytesseract

#for Windows
pytesseract.pytesseract.tesseract_cmd = r"C:/Users/AV/AppData/Local/Programs/Tesseract-OCR/tesseract.exe"

#Load Image
image = Image.open("download.png")

#extract text
text = pytesseract.image_to_string(image)

print(text)