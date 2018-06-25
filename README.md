# Image-Based-Height-Detection
Recognize height from Image

## About project
 * There are 2 API's developed as a part of this project
 * API (/encodeface/) - to train person face. Input to this API is individual facial photo of a person.It extract facial feature and        computes the face encoding and stores it in database for matching purpose

## Installation

Requirements:
* python 3+
* numpy
* scipy
* imutils
* django
* django rest framework
* coreapi (for api documentation)
* opencv-contrib-python

## Instruction to run project

* Save project to local directory
* Go to project folder i.e cd Image-Based-Height-Detection and execute below command
* python manage.py runserver 0.0.0.0:8001


## Guide to installing and running Rest service through API Client

* Install rest api client
https://www.google.co.in/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&ved=0ahUKEwiDzOrtmM_VAhWMo48KHYfyC9UQFgglMAA&url=https%3A%2F%2Fchrome.google.com%2Fwebstore%2Fdetail%2Fpostman%2Ffhbjgbiflinjbdggehcddcbncdddomop%3Fhl%3Den&usg=AFQjCNE_Yq59TT1ZExzJ68FTldg4ho_lGw

### Rest API
#### Training the faces(image encoding)
![alt text](https://github.com/ananthkhegde/Image-Based-Height-Detection/blob/master/assets/restexample.png)
* POST /detectheight/
 * Returns height in cms from image
   * Request:
      * Request Type -- multipart/form-data
      * parameters (key value pair)
         *  key = file , value = link to your file,type = file
    * Response:
         ```
         <heightincm>
         ```

