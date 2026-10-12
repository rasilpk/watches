# Watches - Luxury & Classic Timepieces E-Commerce Store

A modern Django-powered e-commerce web application for luxury, chronograph, classic, and sport watches.

## Features
- **Curated Watch Showcase**: Browse luxury timepieces with high-resolution imagery and specifications.
- **Cart & Checkout**: Intuitive cart management and order checkout flow.
- **Order Tracking**: Real-time order lookup and status tracking.
- **Admin Portal**: Integrated management portal for catalog updates and order processing.
- **Customer Reviews**: Rating and feedback system for individual timepieces.

## Getting Started

### Prerequisites
- Python 3.10+
- pip

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/rasilpk/watches.git
   cd watches
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**:
   ```bash
   python manage.py migrate
   ```

5. **(Optional) Seed product catalog**:
   ```bash
   python seed_products.py
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```
   Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.
