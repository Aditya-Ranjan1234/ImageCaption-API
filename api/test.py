from img import ImageProcessor
import os

image_dir = r".........."

print("Files in images directory:", os.listdir(image_dir))

image_processor = ImageProcessor()

def test_image_analysis(image_path):
    if not os.path.exists(image_path):
        print(f"Image path {image_path} does not exist!")
        return
    image_processor.load_uploaded_image(image_path)
    image_analysis_output = image_processor.generate_image_analysis()
    print("Image Analysis Output:")
    print(image_analysis_output)

def test_caption_and_genre(image_path, context):
    if not os.path.exists(image_path):
        print(f"Image path {image_path} does not exist!")
        return
    image_processor.load_uploaded_image(image_path)
    caption_genre_output = image_processor.generate_image_caption_genre(context)
    print("Caption and Genre Output:")
    print(caption_genre_output)

image_path = r'......'
context = "......"

test_image_analysis(image_path)
test_caption_and_genre(image_path, context)
