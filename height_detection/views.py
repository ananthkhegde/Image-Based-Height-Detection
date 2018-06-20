from rest_framework import views
from rest_framework.response import Response
from .height_detection_final import DetectHeight
from rest_framework.parsers import FormParser, MultiPartParser
from django.utils.datastructures import MultiValueDictKeyError
import base64

class Detect(views.APIView):
    parser_classes = (FormParser, MultiPartParser)

    def post(self, request):
            try:
                if type(request.data['file']) == str:
                    # If file received is a base64 encoded string (Android)
                    file_obj = base64.b64decode(request.data['file'])
                else:
                    file_obj = request.data['file']

                height = DetectHeight().getHeight(file_obj)
                return Response(height)
            except MultiValueDictKeyError:
                return Response("Error Code: 400, Description: Bad Request")
            except:
                return Response("Error Code: 500, Description: Internal Server Error")