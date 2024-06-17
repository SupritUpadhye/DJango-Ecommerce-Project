# DJango-Ecommerce-Project
I've developed a robust Ecommerce application using the Django framework, incorporating a modern and responsive front end with HTML, CSS, JavaScript, and Bootstrap-5. The backend is powered by Python Django, ensuring seamless and efficient performance. For data management, I've utilized MySQL to maintain a secure and reliable database.

# E-commerce Platform

This is a comprehensive e-commerce platform built with Django. It features product listing, product details, cart management, checkout, order processing, payment integration with Razorpay, and user reviews.

## Features

- **Product Management**: List and view products with details and images.
- **Cart Management**: Add to cart, remove from cart, and update cart quantities.
- **Checkout Process**: Address management, order summary, and payment integration.
- **Order Processing**: Generate orders and manage order history.
- **Review System**: Submit and manage product reviews.
- **Responsive Design**: Mobile and desktop-friendly interfaces.
- **Payment Integration**: Razorpay integration for payment processing.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/e-commerce-platform.git
    cd e-commerce-platform
    ```

2. Set up a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:
    ```bash
    python manage.py migrate
    ```

5. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

6. Collect static files:
    ```bash
    python manage.py collectstatic
    ```

7. Run the development server:
    ```bash
    python manage.py runserver
    ```

8. Access the application at `http://127.0.0.1:8000/`.

## Configuration

### Environment Variables

Create a `.env` file in the root directory and add the following environment variables:

```plaintext
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost, 127.0.0.1

RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret

DATABASE_URL=your_database_url

