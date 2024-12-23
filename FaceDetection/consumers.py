import json
import base64
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.files.base import ContentFile
import io
from PIL import Image
import numpy as np
import cv2
import os
from skimage.metrics import structural_similarity as ssim

class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        self.room_group_name = "video_channel"
        await self.accept()

    async def disconnect(self, close_code):
        # Close the WebSocket connection
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(f"Received data: {data}")  # Log incoming data to check its structure

        if data['type'] == 'imageFrame':
            # Step 1: Decode base64 image data
            image_data = data['image']
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))

            # Step 2: Save the image as PNG or JPG
            saved_image_path = self.save_image(image)

            # Step 3: Compare the saved image with training images
            present_students, absent_students = self.identify_students(saved_image_path)

            # Step 4: Send the attendance result back to the client
            await self.send(text_data=json.dumps({
                'type': 'attendanceResults',
                'presentStudents': present_students,
                'absentStudents': absent_students,
            }))

    def save_image(self, image):
        # Define the path to save the image
        save_dir = "received_images/"
        os.makedirs(save_dir, exist_ok=True)  # Create the directory if it doesn't exist
        saved_image_path = os.path.join(save_dir, "received_image.jpg")

        # Save the image as JPG
        image.save(saved_image_path, format="JPEG")
        print(f"Image saved at: {saved_image_path}")

        return saved_image_path

    def identify_students(self, saved_image_path):
        # Load the received image
        received_image = cv2.imread(saved_image_path)

        # Directory containing training images
        training_dir = "training_images/"

        # Lists to store attendance results
        present_students = []
        all_students = [os.path.splitext(file_name)[0] for file_name in os.listdir(training_dir) if file_name.endswith(('.jpg', '.png'))]

        # Perform comparison for each training image
        for file_name in os.listdir(training_dir):
            if file_name.endswith(".jpg") or file_name.endswith(".png"):
                student_name = os.path.splitext(file_name)[0]  # Extract the student name from the file name
                training_image_path = os.path.join(training_dir, file_name)
                training_image = cv2.imread(training_image_path)

                # Calculate similarity
                similarity = self.calculate_similarity(received_image, training_image)
                threshold = 0.8  # Define your similarity threshold

                if similarity >= threshold:
                    present_students.append(student_name)

        # Identify absent students
        absent_students = list(set(all_students) - set(present_students))

        return present_students, absent_students

    def calculate_similarity(self, img1, img2):
        # Ensure the images are the same size for comparison
        img1 = cv2.resize(img1, (256, 256))
        img2 = cv2.resize(img2, (256, 256))

        # Convert images to grayscale
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        # Compute Structural Similarity Index (SSIM)
        similarity, _ = ssim(gray1, gray2, full=True)

        return similarity