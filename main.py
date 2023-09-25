import os
from pymongo import MongoClient
from server import retrieve_image, read_message, validate_product_image, authenticate_user, create_user_account,secure_filename
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, Length
from flask import Flask, render_template, session, redirect, url_for, Response, request

MONGODB_URL = "mongodb+srv://demo:UHd7EzjhREZFkq8d@cluster0.06gzzsk.mongodb.net/?retryWrites=true&w=majority"
app = Flask(__name__)
app.secret_key = "any-string-you-want-just-keep-it-secret"


# Create a directory to store uploaded images
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)



class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email(message='Invalid email address')])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8,
                                                                                  message='Password must be at least 8 characters long')])
    submit = SubmitField(label="Log In")


@app.before_request
def before_request():
    if 'cart' not in session:
        session['cart'] = []


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        print(login_form.email.data)
    return render_template('login.html', form=login_form)


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        if 'image' in request.files:
            uploaded_image = request.files['image']
            product_name = request.form.get('product_name')
            product_id = request.form.get('product_id')
            product_price = request.form.get('product_price')
            product_description = request.form.get('product_description')

            product_details = {'product_name': product_name,
                               'product_id': product_id,
                               'product_price': product_price,
                               'product_description': product_description
                               }

            result = validate_product_image(uploaded_image, product_details=product_details)
            if result == True:
                return f'Image Uploaded and Processed Successfully.'
            else:
                return 'Invalid Image Format. Allowed formats are: jpg, jpeg, png'
        else:
            return 'No Image Uploaded'


@app.route('/image/<filename>')
def get_image(filename):
    get_image = retrieve_image(filename)

    if get_image:
        # Return the image data as a binary response
        return Response(get_image['retrieved_image'], content_type=get_image['format'])



@app.route('/items')
def show_items():

    # Establish a connection to MongoDB
    client = MongoClient(MONGODB_URL)
    db = client['E_coms_logic']

    # Create a collection to store images
    image_collection = db['images']

    # Retrieve a list of image documents from MongoDB
    product_documents = image_collection.find()

    # Render an HTML template with image tags for each retrieved image
    return render_template('item.html', product_documents=product_documents)


@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    # Establish a connection to MongoDB
    client = MongoClient(MONGODB_URL)
    db = client['E_coms_logic']

    # Create a collection to store images
    image_collection = db['images']

    # Retrieve a list of image documents from MongoDB
    product_documents = image_collection.find()

    product = next((p for p in product_documents if p['product_details']['product_id'] == product_id), None)
    if product:
        cart = session['cart']
        if product not in cart:
            cart.append(product)
            session['cart'] = cart
    return redirect(url_for('show_items'))


@app.route('/cart')
def view_cart():
    cart = session['cart']
    total_price = sum(item['price'] for item in cart)
    return render_template('cart.html', cart=cart, total_price=total_price)


@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session['cart']
    for item in cart:
        if item['id'] == product_id:
            cart.remove(item)
            session['cart'] = cart
            break
    return redirect(url_for('view_cart'))


if __name__ == '__main__':
    app.run(debug=True)
