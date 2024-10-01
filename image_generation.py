!pip install gradio
!pip install transformers
!pip install diffusers
!pip install torch

import gradio as gr
from transformers import pipeline
from diffusers import StableDiffusionPipeline
import torch

# Define the device to use (either "cuda" for GPU or "cpu" for CPU)
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load the models
caption_image = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large", device=device)
sd_pipeline = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5").to(device)

# Load the translation model (English to Arabic)
translator = pipeline(
    task="translation",
    model="facebook/nllb-200-distilled-600M",
    torch_dtype=torch.bfloat16,
    device=device
)

!pip install wget # Installs the wget module

import wget # Import the module after successful installation.

# Download the image
url1 = "https://github.com/Shahad-b/Image-database/blob/main/sea.jpg?raw=true"
sea = wget.download(url1)

url2 = "https://github.com/Shahad-b/Image-database/blob/main/Cat.jpeg?raw=true"
Cat = wget.download(url2)

url3 = "https://github.com/Shahad-b/Image-database/blob/main/Car.jpeg?raw=true"
Car = wget.download(url3)

# Function to generate images based on the image's caption
def generate_image_and_translate(image, num_images=1):
    # Generate caption in English from the uploaded image
    caption_en = caption_image(image)[0]['generated_text']

    # Translate the English caption to Arabic
    caption_ar = translator(caption_en, src_lang="eng_Latn", tgt_lang="arb_Arab")[0]['translation_text']

    generated_images = []

    # Generate the specified number of images based on the English caption
    for _ in range(num_images):
        generated_image = sd_pipeline(prompt=caption_en).images[0]
        generated_images.append(generated_image)

    # Return the generated images along with both captions
    return generated_images, caption_en, caption_ar

# Set up the Gradio interface
interface = gr.Interface(
    fn=generate_image_and_translate,   # Function to call when processing input
    inputs=[
        gr.Image(type="pil", label="📤 Upload Image"), # Input for image upload
        gr.Slider(minimum=1, maximum=10, label="🔢 Number of Images", value=1, step=1) # Slider to select number of images
    ],
    outputs=[
        gr.Gallery(label="🖼️ Generated Images"),
        gr.Textbox(label="📝 Generated Caption (English)", interactive=False),
        gr.Textbox(label="🌍 Translated Caption (Arabic)", interactive=False)
    ],
    title="Image Generation and Captioning", # Title of the interface
    description="Upload an image to extract a caption and display it in both Arabic and English. Then, a new image will be generated based on that caption.",  # Description
    examples=[ # Example input
        ["sea.jpg", 3],
        ["Cat.jpeg", 4],
        ["Car.jpeg", 2]
    ],
    theme='freddyaboulton/dracula_revamped' # Determine theme
)

# Launch the Gradio application
interface.launch()
