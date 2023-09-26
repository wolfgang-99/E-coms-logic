from flask import Flask, request, render_template, Response
from pymongo import MongoClient
from werkzeug.utils import secure_filename  # Import secure_filename
import os

app = Flask(__name__)

# Create a directory to store uploaded images
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

MONGODB_URL = "mongodb+srv://demo:UHd7EzjhREZFkq8d@cluster0.06gzzsk.mongodb.net/?retryWrites=true&w=majority"

#
# def upload_img_to_mongodb(image_file_path, image_format, product_details):
#     # Establish a connection to MongoDB
#     client = MongoClient(MONGODB_URL)
#     db = client['E_coms_logic']
#
#     # Create a collection to store images
#     image_collection = db['images']
#
#     # Read the image binary data
#     with open(image_file_path, 'rb') as image_file:
#         image_binary = image_file.read()
#
#     # Get image file information
#     image_filename = os.path.basename(image_file_path)
#     image_size_bytes = os.path.getsize(image_file_path)
#
#     # Convert the size to kilobytes (KB)
#     image_size_kb = image_size_bytes / 1024
#
#     # Convert the size to megabytes (MB)
#     image_size_mb = image_size_kb / 1024
#
#     image_format = image_format  # You can determine the format using libraries like 'python-magic'
#
#     # Store image metadata along with the binary data
#     image_document = {
#         'filename': image_filename,
#         'format': image_format,
#         'size': f'{image_size_mb:.2f} MB',
#         'data': image_binary,
#         'product_details': product_details
#     }
#
#     # Insert the image document into MongoDB
#     image_collection.insert_one(image_document)
#
#     client.close()
#
#
# def validate_product_image(uploaded_image, product_details):
#     image_format = uploaded_image.content_type
#     print(image_format)
#
#     # Check if the file is an allowed image format (e.g., JPEG, PNG)
#     allowed_extensions = {'jpg', 'jpeg', 'png', 'gif'}
#     if '.' in uploaded_image.filename and \
#             uploaded_image.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
#         print(f'this the file name {uploaded_image.filename} ')
#
#         # Generate a secure filename for the uploaded file
#         filename = secure_filename(uploaded_image.filename)
#         print(f'this the secure filename {filename}')
#
#         # Save the image with a unique name in the uploads folder
#         full_path = os.path.join(UPLOAD_FOLDER, filename)
#         uploaded_image.save(full_path)
#         print(f'this is the the full path with securefilename {full_path}')
#
#         # call the upload image function
#         upload_img_to_mongodb(image_file_path=full_path, image_format=image_format, product_details=product_details)
#
#         return True
#     else:
#         return "invalid file format"
#
#
# def retrieve_image(filename):
#     # Establish a connection to MongoDB
#     client = MongoClient(MONGODB_URL)
#     db = client['E_coms_logic']
#
#     # Create a collection to store images
#     image_collection = db['images']
#
#     retrieved_image = image_collection.find_one({'filename': filename})
#     if retrieved_image:
#         # with open('retrieved_image.jpg', 'wb') as output_image_file:
#         #     output_image = output_image_file.write(retrieved_image['data'])
#
#             client.close()
#             image_data = {'retrieved_image': retrieved_image['data'],
#                           'format': retrieved_image['format']
#                           }
#             return image_data
#     else:
#         return "image retrival failed "
#
#
# @app.route('/')
# def index():
#     return render_template('admin.html')
#
#
# @app.route('/upload', methods=['POST'])
# def upload():
#     if request.method == 'POST':
#         if 'image' in request.files:
#             uploaded_image = request.files['image']
#             product_name = request.form.get('product_name')
#             product_id = request.form.get('product_id')
#             product_price = request.form.get('product_price')
#             product_description = request.form.get('product_description')
#
#             product_details = {'product_name': product_name,
#                                'product_id': product_id,
#                                'product_price': product_price,
#                                'product_description': product_description
#                                }
#
#             result = validate_product_image(uploaded_image, product_details=product_details)
#             if result:
#                 return f'Image Uploaded and Processed Successfully.'
#             else:
#                 return 'Invalid Image Format. Allowed formats are: jpg, jpeg, png, gif'
#         else:
#             return 'No Image Uploaded'
#
#
# @app.route('/image/<filename>')
# def get_image(filename):
#     get_image = retrieve_image(filename)
#
#     if get_image:
#         # Return the image data as a binary response
#         return Response(get_image['retrieved_image'], content_type=get_image['format'])
#
#
# @app.route('/images')
# def show_images():
#     # Establish a connection to MongoDB
#     client = MongoClient(MONGODB_URL)
#     db = client['E_coms_logic']
#
#     # Create a collection to store images
#     image_collection = db['images']
#
#     # Retrieve a list of image documents from MongoDB
#     product_documents = image_collection.find()
#
#     # Render an HTML template with image tags for each retrieved image
#     return render_template('test.html', product_documents=product_documents)
#
# if __name__ == '__main__':
#     app.run(debug=True)


# Establish a connection to MongoDB
client = MongoClient(MONGODB_URL)
db = client['E_coms_logic']

# Create a collection to store images
image_collection = db['images']

 # Retrieve a list of image documents from MongoDB
product_documents = image_collection.find()

product = next((p for p in product_documents if p['product_details']['product_id'] == "ph23"), None)

print(product)