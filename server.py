import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from werkzeug.utils import secure_filename
import os

MONGODB_URL = "mongodb+srv://demo:UHd7EzjhREZFkq8d@cluster0.06gzzsk.mongodb.net/?retryWrites=true&w=majority"

# Create a directory to store uploaded images
UPLOAD_FOLDER = 'product images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def authenticate_user(username, password):
    try:
        # Connect to mongodb
        client = MongoClient(MONGODB_URL)
        db = client['demo']
        collection = db['login_details']

        # Define the criteria for the username and password
        input_username = username
        input_password = password

        # Find the user by username
        user_document = collection.find_one({"email": input_username})
        if user_document:
            stored_password = user_document["password"]

            # Check if the provided password matches the stored hash
            if stored_password == input_password:
                return "Login Successful"
            else:
                return "Login Failed: Incorrect Password"
        else:
            return "Login Failed: User not found"
    except Exception as e:
        return "An error occurred: " + str(e)


def create_user_account(username, email, number, password):
    try:
        # Connect to mongodb
        client = MongoClient(MONGODB_URL, server_api=ServerApi('1'))
        db = client['demo']
        collection = db['login_details']

        submission = {'username': username,
                      'email': email,
                      'number': number,
                      'password': password
                      }
        collection.insert_one(submission)
        print(f"data has been recoreded")
        return True

    except Exception as e:
        return "An error occurred: " + str(e)


def send_email_with_image(sender_email, sender_password, receiver_email, subject, paragraphs, image_path):
    # Create a multipart message container
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Create the HTML content of the email
    html = f'''
       <html>
           <body>
               <p>Congratulations on receiving your golden ticket for 
               "The Next Big Thing" blockchain event in Africa! Organized by BFA</p>
               <p><img src="cid:image"></p>
               {''.join(f"<p>{p}</p>" for p in paragraphs)}
           </body>
       </html>
       '''

    # Attach the HTML content to the email
    msg.attach(MIMEText(html, 'html'))

    image_path = 'static/assets/images/logo.png'

    # Open the image file
    with open(image_path, 'rb') as image_file:
        # Create a MIME image object
        image = MIMEImage(image_file.read())

        # Define the image ID
        image.add_header('Content-ID', '<image>')
        image.add_header('Content-Disposition', 'inline', filename=image_path)

        # Attach the image to the email
        msg.attach(image)

    # Establish a secure connection with the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    # Login to the sender's email account
    server.login(sender_email, sender_password)

    # Send the email
    server.send_message(msg)

    # Clean up the connection
    server.quit()

    return True


def read_message(file_path, register_name):
    with open(file_path, 'r') as email_text:
        message = email_text.read()
        message = message.replace("[Name]", register_name)
        paragraphs = message.split('\n\n')  # Assuming paragraphs are separated by two newline characters
    return paragraphs


def submit_email_details(register_email, register_name):
    if register_email:
        sender_email = 'kristaspace0@gmail.com'
        sender_password = 'pkhmlmmqhpcwjhob'
        subject = 'Welcome to WOW MATIC - Your Ultimate Destination for Outstanding Service!'
        image_path = 'static/assets/images/logo.png'
        file_path = "Email_text.txt"

        paragraphs = read_message(file_path, register_name)
        Email_sent = send_email_with_image(sender_email=sender_email, sender_password=sender_password,
                                           receiver_email=register_email, subject=subject, paragraphs=paragraphs,
                                           image_path=image_path)

        if Email_sent:
            print('email sent')
            return 'email sent '


def upload_img_to_mongodb(image_file_path, image_format, product_details):
    # Establish a connection to MongoDB
    client = MongoClient(MONGODB_URL)
    db = client['E_coms_logic']

    # Create a collection to store images
    image_collection = db['images']

    # Read the image binary data
    with open(image_file_path, 'rb') as image_file:
        image_binary = image_file.read()

    # Get image file information
    image_filename = os.path.basename(image_file_path)
    image_size_bytes = os.path.getsize(image_file_path)

    # Convert the size to kilobytes (KB)
    image_size_kb = image_size_bytes / 1024

    # Convert the size to megabytes (MB)
    image_size_mb = image_size_kb / 1024

    image_format = image_format  # You can determine the format using libraries like 'python-magic'

    # Store image metadata along with the binary data
    image_document = {
        'filename': image_filename,
        'format': image_format,
        'size': f'{image_size_mb:.2f} MB',
        'data': image_binary,
        'product_details': product_details
    }

    # Insert the image document into MongoDB
    image_collection.insert_one(image_document)

    client.close()


def validate_product_image(uploaded_image, product_details):
    image_format = uploaded_image.content_type
    print(image_format)

    # Check if the file is an allowed image format (e.g., JPEG, PNG)
    allowed_extensions = {'jpg', 'jpeg', 'png', 'gif'}
    if '.' in uploaded_image.filename and \
            uploaded_image.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
        print(f'this the file name {uploaded_image.filename} ')

        # Generate a secure filename for the uploaded file
        filename = secure_filename(uploaded_image.filename)
        print(f'this the secure filename {filename}')

        # Save the image with a unique name in the uploads folder
        full_path = os.path.join(UPLOAD_FOLDER, filename)
        uploaded_image.save(full_path)
        print(f'this is the the full path with securefilename {full_path}')

        # call the upload image function
        upload_img_to_mongodb(image_file_path=full_path, image_format=image_format, product_details=product_details)

        return True
    else:
        return "invalid file format"


def retrieve_image(filename):
    # Establish a connection to MongoDB
    client = MongoClient(MONGODB_URL)
    db = client['E_coms_logic']

    # Create a collection to store images
    image_collection = db['images']

    retrieved_image = image_collection.find_one({'filename': filename})
    if retrieved_image:
        with open('retrieved_image.jpg', 'wb') as output_image_file:
            output_image = output_image_file.write(retrieved_image['data'])

            client.close()
            image_data = {'retrieved_image': retrieved_image['data'],
                          'format': retrieved_image['format']
                          }
            client.close()
            return image_data
    else:
        return "image retrival failed "


def get_product(product_id):
    """ this get a product using the product_id given it """

    # Establish a connection to MongoDB
    client = MongoClient(MONGODB_URL)
    db = client['E_coms_logic']

    # Create a collection to store images
    image_collection = db['images']

    # Find the selected product in the database by product_id
    product = image_collection.find_one({'product_details.product_id': product_id})

    return product
