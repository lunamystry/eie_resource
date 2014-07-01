from flask import request
from flask.ext.restful import Resource
from flask.ext.restful import abort
import os
import re
import logging
# import PIL
from backend import app

logger = logging.getLogger("backend.admin.rest.Images")


class Image(Resource):
    def get(self, category, image_name):
        cwd = os.path.dirname(__file__)
        local_filename = cwd + "/static/img/gallery/" + category + '/' + image_name
        filename = 'img/gallery/' + category + '/' + image_name
        try:
            with open(local_filename):
                pass
        except IOError:
            abort(404)
        image = url_for('static', filename=filename)
        return image

    def delete(self, category, image_name):
        cwd = os.path.dirname(__file__)
        local_filename = cwd + "/static/img/gallery/" + category + '/' + image_name
        os.remove(local_filename)
        return "", 204


class Images(Resource):
    def get(self):
        image_dir = app.config['GALLERY_FOLDER']
        gallery_url = app.config['GALLERY_URL']
        image_list = []
        if not os.path.isdir(image_dir):
            logger.error("directory {} does not exist".format(image_dir))
            abort(500)
        for root, dirs, files in os.walk(image_dir):
            if files:
                for filename in files:
                    if re.search(r'([^\s]+(\.(?i)(jpg|jpeg|png|gif|bmp))$)',
                                 filename):
                        img = {"name": filename,
                               "imageUrl": gallery_url+filename,
                               "thumbUrl": gallery_url+"thumbs/"+filename,
                               "directory": root}
                        image_list.append(img)
        return image_list

    def post(self):
        # This will need some more testing
        file = request.files['file']
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return args, 201
        else:
            return "class photo could not be uploaded " + str(args), 500

    def allowed_file(filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    def validate(self, data):
        errors = {}
        validators = {"description": [required,
                                      functools.partial(length, max=15, message='description too long')]}
        # make sure all value keys are there
        for key in validators.keys():
            try:
                value = data[key]
            except KeyError:
                data[key] = None
        # validate
        for key in validators.keys():
            value = data[key]
            field_errors = []
            for validator in validators[key]:
                try:
                    validator(value)
                except ValidationError as e:
                    field_errors.append(e.message)
            if field_errors:
                errors[key] = field_errors
        return data, errors


# def resize_and_crop(img_path, modified_path, size, crop_type='top'):
#     """
#     FROM: https://gist.github.com/sigilioso/2957026
#     Resize and crop an image to fit the specified size.
# 
#     args:
#       img_path: path for the image to resize.
#       modified_path: path to store the modified image.
#       size: `(width, height)` tuple.
#       crop_type: can be 'top', 'middle' or 'bottom', depending on this
#         value, the image will cropped getting the 'top/left', 'middle' or
#         'bottom/right' of the image to fit the size.
#     raises:
#       Exception: if can not open the file in img_path of there is problems
#         to save the image.
#       ValueError: if an invalid `crop_type` is provided.
#     """
#     # If height is higher we resize vertically, if not we resize horizontally
#     img = PIL.Image.open(img_path)
#     # Get current and desired ratio for the images
#     img_ratio = img.size[0] / float(img.size[1])
#     ratio = size[0] / float(size[1])
#     if ratio > img_ratio:
#         img = img.resize((size[0],
#                           int(round(size[0] * img.size[1] / img.size[0]))),
#                          PIL.Image.ANTIALIAS)
#         # Crop in the top, middle or bottom
#         if crop_type == 'top':
#             box = (0, 0, img.size[0], size[1])
#         elif crop_type == 'middle':
#             box = (0, int(round((img.size[1] - size[1]) / 2)), img.size[0],
#                    int(round((img.size[1] + size[1]) / 2)))
#         elif crop_type == 'bottom':
#             box = (0, img.size[1] - size[1], img.size[0], img.size[1])
#         else:
#             raise ValueError('invalid value for crop_type')
#         img = img.crop(box)
#     elif ratio < img_ratio:
#         img = img.resize((int(round(size[1] * img.size[0] / img.size[1])),
#                           size[1]),
#                          PIL.Image.ANTIALIAS)
#         # Crop in the top, middle or bottom
#         if crop_type == 'top':
#             box = (0, 0, size[0], img.size[1])
#         elif crop_type == 'middle':
#             box = (int(round((img.size[0] - size[0]) / 2)), 0,
#                    int(round((img.size[0] + size[0]) / 2)), img.size[1])
#         elif crop_type == 'bottom':
#             box = (img.size[0] - size[0], 0, img.size[0], img.size[1])
#         else:
#             raise ValueError('invalid value for crop_type')
#         img = img.crop(box)
#     else:
#         img = img.resize((size[0], size[1]),
#                          PIL.Image.ANTIALIAS)
#     img.save(modified_path)
