from transformers import BlipProcessor, BlipForConditionalGeneration, DetrImageProcessor, DetrForObjectDetection
from PIL import Image
import requests
import torch


def get_image_caption(image_path):
    """
    Generation a short caption for the provided image.

    Args:
        image_path (str): The path to the image file.

    Returns:
        str: A string representing the caption for the image.
    """

    # Read image
    image = Image.open(image_path).convert("RGB")

    model_name = "Salesforce/blip-image-captioning-large"
    device = "cpu"

    processor = BlipProcessor.from_pretrained(model_name)
    model = BlipForConditionalGeneration.from_pretrained(model_name).to(device)

    inputs = processor(image, return_tensors='pt').to(device)
    output = model.generate(**inputs, max_new_tokens=20)

    caption = processor.decode(output[0], skip_special_tokens=True)

    return caption


def detect_objects(image_path):
    image = Image.open(image_path).convert("RGB")

    processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
    model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")

    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)

    # convert outputs (bounding boxes and class logits) to COCO API
    # let's only keep detections with score > 0.9
    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(
        outputs, target_sizes=target_sizes, threshold=0.9)[0]

    detections = ""
    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        detections += f'[{int(box[0])}, {int(box[1])}, {int(box[2])}, {int(box[3])}]'
        detections += f' {model.config.id2label[int(label)]}'
        detections += f' {float(score)}\n'
    return detections


if __name__ == '__main__':
    image_path = r'C:\Users\HP\Desktop\AI_project\project_details\chat_images\food.jpg'
    caption = get_image_caption(image_path)
    detections = detect_objects(image_path)
    print(detections)
