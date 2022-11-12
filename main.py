import face_recognition
from flask import Flask, jsonify, request, redirect
 
# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
 
app = Flask(__name__)
 
 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
 
@app.route('/', methods=['GET', 'POST'])
def upload_image():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file1' not in request.files:
            return redirect(request.url)
 
        file1 = request.files['file1']
        file2 = request.files['file2']
 
        if file1.filename == '' or file2.filename == '' :
            return redirect(request.url)
 
        if file1 and allowed_file(file1.filename) and file2 and allowed_file(file2.filename):
            # The image file seems valid! Detect faces and return the result.
            return detect_faces_in_image(file1, file2)
 
    # If no valid image file was uploaded, show the file upload form:
    return '''
    <!doctype html>
    <title>Face比对</title>
    <h1>上传两张图片以对比是否为同一人</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file1">
      <input type="file" name="file2">
      <input type="submit" value="Upload">
    </form>
    '''
 

@app.route('/check', methods=['POST'])
def check():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
 
        file1 = request.files['file']
        with open("wujin.png", "r") as file2:
            if file1.filename == '' or file2.filename == '' :
                return redirect(request.url)
 
            if file1 and allowed_file(file1.filename) and file2 and allowed_file(file2.filename):
                # The image file seems valid! Detect faces and return the result.
                return detect_faces_in_image(file1, file2)
 
        # If no valid image file was uploaded, show the file upload form:
        response = {"sucess": False, "data": "no files in request"}
        return jsonify(response)


  
def detect_faces_in_image(file_stream1, file_stream2):
    face_found = False
    is_same_person = False
    # Return the result as json
    result = {
        "sucess": True,
        "face_found_in_image": face_found,
        "is_same_person": is_same_person
    }
    # Pre-calculated face encoding of Obama generated with face_recognition.face_encodings(img)
    try:
        code1 = face_recognition.face_encodings(face_recognition.load_image_file(file_stream1))[0]
        code2 = face_recognition.face_encodings(face_recognition.load_image_file(file_stream2))[0]
    except:
        return jsonify(result)

 
    if len(code1) > 0 and len(code2) > 0:
        face_found = True
        match_results = face_recognition.compare_faces([code1], code2)
        if match_results[0]:
            is_same_person = True
    
    result = {
        "sucess": True,
        "face_found_in_image": face_found,
        "is_same_person": is_same_person
    }
    
    return jsonify(result)
 
 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)