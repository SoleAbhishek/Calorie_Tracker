# from flask import Flask, render_template, request
# import tempfile

# from calorie_counter import get_calories_from_image

# app = Flask(__name__)

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/upload", methods=["POST"])
# def upload():
#     image = request.files["image"]

#     if image.filename == "":
#         return {
#             "error": "No image uploaded",
#         }, 400

#     temp_file = tempfile.NamedTemporaryFile()
#     image.save(temp_file.name)

#     calories = get_calories_from_image(temp_file.name)
#     temp_file.close()

#     return {
#         "calories": calories,
#     }

# if __name__ == "__main__":
#     app.run(debug=True)
from flask import Flask, render_template, request, jsonify
import os
import tempfile

from calorie_counter import get_calories_from_image

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    image = request.files["image"]

    if image.filename == "":
        return jsonify({"error": "No image uploaded"}), 400

    # Create a temporary file with delete=False
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        temp_path = temp_file.name  # Get the file path
        image.save(temp_path)  # Save the image

    try:
        # Process the image using your function
        calories = get_calories_from_image(temp_path)
        return jsonify({"calories": calories})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Clean up the temporary file after processing
        os.remove(temp_path)

if __name__ == "__main__":
    app.run(debug=True)
