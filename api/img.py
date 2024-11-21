import json
from llama_index.core.multi_modal_llms.generic_utils import load_image_urls
from llama_index.core import SimpleDirectoryReader
from pydantic import BaseModel
from llama_index.core.output_parsers import PydanticOutputParser
import Ollama
from llama_index.core import SimpleDirectoryReader

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
        self.image_documents = SimpleDirectoryReader("images").load_data()
        print("Image directory located")
        self.llm = Ollama(model="llama3:instruct")
        self.prompt_template_str = """\
        {query_str}

        ""20words make sure it is less than 20 words Analyze the image for any potential privacy or security risks, focusing on identifying sensitive or personal information based on visual elements such as documents, screens, or personal items. Avoid returning any specific text present in the image. Instead, provide a brief, general warning if anything could compromise privacy or security. Do not describe or extract any written content also keep the analysis small within 20words make sure it is less than 20 words ."""
        self.mm_model = OllamaMultiModal(model="llava-llama3")
        self.parser1 = PydanticOutputParser(Image_struct)
        print("The class was initialized")

    def privacy_information(self):
        output = self.mm_model.complete(self.prompt_template_str , image_documents=self.image_documents)
        self.output_privacy_description = str(output)
        print("trackable was complete")
        return {"trackable": self.output_privacy_description}
    
    def image_description(self):
        description_template = """20words make sure it is less than 20 words Provide a high-level description of the main subjects and objects in the image, focusing on their appearance, size, color, and arrangement. Describe any noticeable interactions or actions between these elements without focusing on fine details or written text. Include background elements and general atmosphere, but avoid extracting or describing any specific text from documents or screens. Aim for a broad description that conveys the overall context and mood of the scene"""
        output = self.mm_model.complete(description_template, image_documents=self.image_documents)
        self.output_image_description = str(output)
        print("image description was completed")
        return {"image_description":self.output_image_description}
    
    def music_genre(self, context):
        self.context = context
        music_prompt = f"""Based on the following scenario and context, choose the most fitting music genre from the list of genres: [blues, classical, country, disco, hiphop, jazz, metal, pop, reggae, rock].
        Scenario: {self.output_image_description}.
        Context: {context}.
        Which genre fits this scenario the best? (one word)"""
        response = self.llm.complete(music_prompt)
        response = str(response)
        genre = self.music_genre_checker(response)
        print("the image genre was generated")
        if genre != None:
            return {"genre": genre}
        else:
            return {"genre": "genre not found"}
    
    def caption_genre_generator(self):
        prompt = f"""
        Based on the following scenario and context, generate a suitable caption for the image:

        - Image Description: {self.output_image_description}
        - Additional Context: {self.context}

        Provide a single caption that blends the visual elements of the image and the context.
        """
        response = self.llm.complete(prompt= prompt)
        caption = str(response)
        print("The caption was generated")
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
        print("The complete jsom was dumped")
        return json.dumps(combined_result, indent=4)

            
    def generate_image_caption_genre(self,context):
        self.image_description()
        genre = self.music_genre(context)
        caption = self.caption_genre_generator()
        combined_resut = {
            "Caption": caption["caption"],
            "genre": genre["genre"]
                
        }
        print("Image caption and genre was dumped")
        return json.dumps(combined_resut , indent=4)
