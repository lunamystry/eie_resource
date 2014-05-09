from flask import request
from flask import jsonify
from flask.ext.restful import Resource
from flask.ext.restful import abort
import os
import glob
from resource import app


class ClassPhoto(Resource):
    def get(self, category, class_photo_name):
        cwd = os.path.dirname(__file__)
        local_filename = cwd + "/static/img/gallery/" + category + '/' + class_photo_name
        filename = 'img/gallery/' + category + '/' + class_photo_name
        try:
            with open(local_filename): pass
        except IOError:
            abort(404)
        class_photo = url_for('static', filename=filename)
        return class_photo

    def delete(self, category, class_photo_name):
        cwd = os.path.dirname(__file__)
        local_filename = cwd + "/static/img/gallery/" + category + '/' + class_photo_name
        os.remove(local_filename)
        return "", 204


class ClassPhotos(Resource):
    def get(self):
        cwd = os.path.dirname(__file__)
        directory = app.config['CLASS_PHOTOS_FOLDER']
        paths = glob.glob(directory + "/*")
        class_photo_list = []
        for class_photo_path in paths:
            class_photo_name = os.path.basename(class_photo_path)
            url = "static/images/" + class_photo_name
            class_photo = {'name': class_photo_name[:-4], 'url': url}
            class_photo_list.append(class_photo)
        return jsonify({"result": class_photo_list})

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
