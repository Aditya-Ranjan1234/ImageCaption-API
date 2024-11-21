from img import ImageProcessor

image_processor = ImageProcessor()
image_processor.load_uploaded_image(r'path.jpg')

image_analysis_output = image_processor.generate_image_analysis()
print("Image Analysis Output:")
print(image_analysis_output)

context = "A sunny beach scene"
caption_genre_output = image_processor.generate_image_caption_genre(context)
print("Caption and Genre Output:")
print(caption_genre_output)
