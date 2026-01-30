import os
from flask import Flask, flash, render_template, url_for, redirect, request,send_file
from werkzeug.utils import secure_filename
import Back.big
import Back.j

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
app = Flask(__name__)
path = r"static/uploads/"
if not os.path.exists(path):
    os.makedirs(path)
app.config['UPLOAD_FOLDER'] = path
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = "therearenoneinexistance"



def allowed_file(filename):
    return '.' in filename and filename.split('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def hello():
    return render_template('upload_proceed.html')


@app.route('/', methods=['POST'])
def upload_image():
    print(request.files)
    print(request.values)
    print(request.form)
    if "persistent_img" in request.form:
        filename = request.form['persistent_img']
        if "Check-File" in request.form:
            flash('приблезительное число автосредств на автостоянке:')
            res = (Back.big.neuro_proceed(f"{os.curdir}/{app.config['UPLOAD_FOLDER']}{filename}"))
            return render_template('upload_proceed.html', filename=f"{filename.partition('.')[0]}_aug.jpg", otchet = res)
        elif "Img-Report" in request.form:
            flash('Это будет делать отчёт по изображению')

            return_report_user = Back.j.gen(f"{os.curdir}/{app.config['UPLOAD_FOLDER']}{filename}", Back.big.neuro_proceed(f"{os.curdir}/{app.config['UPLOAD_FOLDER']}{filename}"))

            if return_report_user != "":
                return send_file(f"{return_report_user}", as_attachment=True)


    if 'file' not in request.files:
        flash('Выберите новый или старый файл и обработка начнётся заново')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        if "Submit-File" in request.form:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        elif "Check-File" in request.form:
            flash('Это будет считать автосредства, но пока изображение не загружено, обработки не будет')

        elif "Img-Report" in request.form:
            flash('Это будет делать отчёт по изображению, но сначала надо его загрузить и обработать')

        flash('Image uploaded and displayed below')
        return render_template('upload_proceed.html', filename=filename)

    else:
        flash('Allowed image types are png, jpeg, jpg')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == '__main__':
    app.run(debug=True)
