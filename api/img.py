import json
from llama_index.core.multi_modal_llms.generic_utils import load_image_urls
from llama_index.core import SimpleDirectoryReader
from pydantic import BaseModel
from llama_index.multi_modal_llms.ollama import OllamaMultiModal
from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.llms.ollama import Ollama

class Image_struct(BaseModel):
    trackable: str

class Image_description(BaseModel):
    description: str

class Post(BaseModel):
    title: str
    post_text: str
    music_genre: str

class ImageProcessor():
    def __init__(self):
        self.llm = Ollama(model="llama3:instruct")
        self.mm_model = OllamaMultiModal(model="llava-llama3")
        self.parser1 = PydanticOutputParser(Image_struct)

    def load_uploaded_image(self, image_path):
        self.image_documents = [{"path": image_path}]

    def privacy_information(self):
        output = self.mm_model.complete(self.prompt_template_str, image_documents=self.image_documents)
        self.output_privacy_description = str(output)
        return {"trackable": self.output_privacy_description}

    def image_description(self):
        description_template = """20words make sure it is less than 20 words Provide a high-level description of the main subjects and objects in the image, focusing on their appearance, size, color, and arrangement. Describe any noticeable interactions or actions between these elements without focusing on fine details or written text. Include background elements and general atmosphere, but avoid extracting or describing any specific text from documents or screens. Aim for a broad description that conveys the overall context and mood of the scene"""
        output = self.mm_model.complete(description_template, image_documents=self.image_documents)
        self.output_image_description = str(output)
        return {"image_description": self.output_image_description}

    def music_genre(self, context):
        self.context = context
        music_prompt = f"""Based on the following scenario and context, choose the most fitting music genre from the list of genres: [blues, classical, country, disco, hiphop, jazz, metal, pop, reggae, rock]. Scenario: {self.output_image_description}. Context: {context}. Which genre fits this scenario the best? (one word)"""
        response = self.llm.complete(music_prompt)
        response = str(response)
        genre = self.music_genre_checker(response)
        if genre != None:
            return {"genre": genre}
        else:
            return {"genre": "genre not found"}

    def caption_genre_generator(self):
        prompt = f"""Based on the following scenario and context, generate a suitable caption for the image: - Image Description: {self.output_image_description} - Additional Context: {self.context} Provide a single caption that blends the visual elements of the image and the context."""
        response = self.llm.complete(prompt=prompt)
        caption = str(response)
        return {"caption": caption}

    def music_genre_checker(self, llm_response):
        self.labels = ["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock"]
        for label in self.labels:
            if label.lower() in llm_response.lower():
                return label
        return None

    def generate_image_analysis(self):
        description = self.image_description()
        privacy_warning = self.privacy_information()
        combined_result = {
            "image_description": description["image_description"],
            "trackable": privacy_warning["trackable"]
        }
        return json.dumps(combined_result, indent=4)

    def generate_image_caption_genre(self, context):
        self.image_description()
        genre = self.music_genre(context)
        caption = self.caption_genre_generator()
        combined_resut = {
            "Caption": caption["caption"],
            "genre": genre["genre"]
        }
        return json.dumps(combined_resut, indent=4)
