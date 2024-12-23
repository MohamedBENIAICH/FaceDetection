# consumers.py

import json
import base64
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.files.base import ContentFile
import io
from PIL import Image
import numpy as np
import cv2

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
            image_data = data['image']
            # Decode base64 image data
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))

            # Convert to a NumPy array for OpenCV processing
            np_image = np.array(image)
            frame = cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR)

            print("Received an image frame")

            # Optionally, send a response back to the client
            await self.send(text_data=json.dumps({
                'message': 'Image processed successfully'
            }))