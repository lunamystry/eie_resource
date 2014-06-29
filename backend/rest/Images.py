from flask import request
from flask.ext.restful import Resource
from flask.ext.restful import abort
import os
import re
import logging
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
                               "imageUrl": os.path.join(root, filename),
                               "thumbUrl": os.path.join(root, "thumbs",
                                                        filename),
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
