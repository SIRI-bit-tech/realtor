# 🏡 Nuvana Realty Platform

![License MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Django 4.x](https://img.shields.io/badge/Django-4.x-green.svg)
![Status Active](https://img.shields.io/badge/status-active-green.svg)
![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Bootstrap 5](https://img.shields.io/badge/Bootstrap-5.0-purple.svg)

## 📋 Table of Contents

- [🌟 Overview](#-overview)
- [✨ Features](#-features)
- [🛠️ Technology Stack](#️-technology-stack)
- [📁 Project Structure](#-project-structure)
- [🚀 Installation](#-installation)
- [💻 Usage](#-usage)
- [🎯 Key Functionality](#-key-functionality)
- [📱 User Roles](#-user-roles)
- [🎨 Frontend Features](#-frontend-features)
- [🔧 Backend Architecture](#-backend-architecture)
- [📊 Analytics & Tracking](#-analytics--tracking)
- [🛡️ Security Features](#️-security-features)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [🚀 Deploying to Render](#-deploying-to-render)

## 🌟 Overview

**Nuvana Realty Platform** is a comprehensive, full-stack real estate platform built with Django 4.x that connects property buyers, sellers, and real estate agents in a seamless digital environment. This modern, scalable platform features advanced search, agent and property management, messaging, analytics, and more—all with a professional, branded design system for Nuvana Realty.

## ✨ Features

### 🏠 Property Management
- **Advanced Property Listings** with detailed information, high-quality image galleries, and virtual tours
- **Smart Search & Filtering** by location, price range, property type, bedrooms, bathrooms, and custom criteria
- **Interactive Maps** with property markers and neighborhood information
- **Favorites System** allowing users to save and organize preferred properties
- **Property Analytics** tracking views, favorites, and engagement metrics

### 👥 User Management
- **Multi-Role System** supporting Buyers, Sellers, Agents, and Administrators
- **Comprehensive User Profiles** with customizable preferences and contact information
- **Personalized Dashboards** showing saved properties, search history, and account analytics
- **Advanced Authentication** with secure login, registration, and password management

### 🏢 Agent & Agency System
- **Professional Agent Profiles** showcasing experience, specializations, and client reviews
- **Agency Management** with team structures and company branding
- **Performance Analytics** tracking sales, listings, and client interactions
- **Review & Rating System** for transparent agent evaluation

### 💬 Communication & Messaging
- **Integrated Messaging System** connecting buyers with agents
- **Contact Forms** for property inquiries and general communication
- **Automated Notifications** for new listings, price changes, and saved search alerts

### 📊 Analytics & Insights
- **Real-time Analytics Dashboard** for administrators and agents
- **Property Performance Tracking** with view counts, engagement metrics, and market trends
- **User Behavior Analysis** including search patterns and browsing history
- **Custom Reports** for business intelligence and decision making

## 🛠️ Technology Stack

### Backend Technologies
- **Django 4.x** - Robust Python web framework
- **PostgreSQL** - Advanced relational database
- **Redis** - High-performance caching and session storage
- **Celery** - Asynchronous task processing
- **Django REST Framework** - API development
- **Pillow** - Advanced image processing

### Frontend Technologies
- **HTML5 & CSS3** - Modern semantic markup and styling
- **Bootstrap 5** - Responsive UI framework
- **JavaScript (ES6+)** - Interactive client-side functionality
- **HTMX** - Dynamic content loading without page refreshes
- **Chart.js** - Beautiful data visualizations and analytics

### Development Tools
- **Docker & Docker Compose** - Containerized development environment
- **Git** - Version control and collaboration
- **Whitenoise** - Static file serving for production
- **Django Debug Toolbar** - Development debugging tools

## 📁 Project Structure

```
realtor_project/
├── 📁 apps/                          # Django applications
│   ├── 📁 core/                      # Core functionality and home pages
│   ├── 📁 properties/                # Property listings and management
│   ├── 📁 users/                     # User profiles and authentication
│   ├── 📁 agents/                    # Agent and agency management
│   ├── 📁 accounts/                  # Authentication system
│   ├── 📁 search/                    # Advanced search functionality
│   ├── 📁 messaging/                 # Communication system
│   └── 📁 analytics/                 # Data analytics and tracking
├── 📁 templates/                     # HTML templates
│   ├── 📁 pages/                     # Static pages (home, about, contact)
│   ├── 📁 properties/                # Property-related templates
│   ├── 📁 users/                     # User dashboard templates
│   ├── 📁 agents/                    # Agent profile templates
│   ├── 📁 accounts/                  # Authentication templates
│   └── 📁 partials/                  # Reusable template components
├── 📁 static/                        # Static assets
│   ├── 📁 css/                       # Stylesheets
│   ├── 📁 js/                        # JavaScript files
│   └── 📁 images/                    # Static images
├── 📁 media/                         # User-uploaded content
├── 📁 realtor_project/               # Django project settings
│   ├── 📁 settings/                  # Environment-specific settings
│   │   ├── base.py                   # Common settings
│   │   ├── development.py            # Development configuration
│   │   └── production.py             # Production configuration
│   ├── urls.py                       # URL routing
│   └── wsgi.py                       # WSGI configuration
├── 📄 requirements.txt               # Python dependencies
├── 📄 docker-compose.yml             # Docker services configuration
├── 📄 Dockerfile                     # Container definition
└── 📄 manage.py                      # Django management script
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- PostgreSQL 12+
- Redis server
- Git

### Quick Start

1. **Clone the repository**
\`\`\`bash
git clone https://github.com/SIRI-bit-tech/realtor
cd django-realtor-website
\`\`\`

2. **Create virtual environment**
\`\`\`bash
python -m venv realtor_env
source realtor_env/bin/activate  # On Windows: realtor_env\Scripts\activate
\`\`\`

3. **Install dependencies**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

4. **Environment setup**
\`\`\`bash
cp .env.example .env
# Edit .env with your database and configuration settings
\`\`\`

5. **Database setup**
\`\`\`bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
\`\`\`

6. **Load sample data (optional)**
\`\`\`bash
python manage.py loaddata fixtures/sample_data.json
\`\`\`

7. **Run development server**
\`\`\`bash
python manage.py runserver
\`\`\`

Visit `http://localhost:8000` to see the application.

### Docker Installation

\`\`\`bash
# Clone and navigate to project
git clone https://github.com/SIRI-bit-tech/realtor
cd django-realtor-website

# Build and run with Docker Compose
docker-compose up --build

# Create superuser
docker-compose exec web python manage.py createsuperuser
\`\`\`

## 💻 Usage

### For Property Buyers
1. **Browse Properties** - Search and filter properties by location, price, and features
2. **Save Favorites** - Create a personal list of preferred properties
3. **Contact Agents** - Directly message listing agents for inquiries
4. **Track Searches** - Save search criteria for automatic notifications
5. **View Analytics** - See your browsing history and saved properties

### For Real Estate Agents
1. **Manage Listings** - Add, edit, and update property information
2. **Track Performance** - Monitor property views, inquiries, and engagement
3. **Client Communication** - Respond to buyer inquiries and messages
4. **Profile Management** - Showcase expertise, certifications, and client reviews
5. **Analytics Dashboard** - Access detailed performance metrics and insights

### For Administrators
1. **User Management** - Oversee user accounts, agents, and agencies
2. **Content Moderation** - Review and approve property listings
3. **System Analytics** - Monitor platform usage and performance metrics
4. **Configuration** - Manage site settings, property types, and locations

## 🎯 Key Functionality

### Advanced Search System
- **Geolocation-based Search** with radius filtering
- **Multi-criteria Filtering** including price range, property features, and amenities
- **Smart Autocomplete** with real-time suggestions
- **Saved Search Alerts** with email notifications
- **Map-based Property Discovery** with interactive markers

### Property Management
- **Comprehensive Property Profiles** with detailed descriptions and specifications
- **Professional Photography** with optimized image galleries
- **Virtual Tour Integration** for immersive property viewing
- **Price History Tracking** and market analysis
- **Automatic MLS Integration** capabilities

### User Experience
- **Responsive Design** optimized for all devices and screen sizes
- **Progressive Web App** features for mobile users
- **Fast Loading Times** with optimized caching and CDN integration
- **Accessibility Compliance** following WCAG 2.1 guidelines
- **SEO Optimization** for maximum search engine visibility

## 📱 User Roles

### 🏠 Buyers
- Browse and search property listings
- Save favorite properties and create watchlists
- Contact agents and schedule viewings
- Track viewing history and preferences
- Receive notifications for new matching properties

### 🏢 Sellers
- List properties with comprehensive details
- Upload high-quality photos and virtual tours
- Track property performance and viewer analytics
- Manage pricing and availability
- Communicate with potential buyers

### 👨‍💼 Agents
- Manage multiple property listings
- Access detailed client and property analytics
- Handle client communications and inquiries
- Showcase professional credentials and reviews
- Generate performance reports and market insights

### 🛡️ Administrators
- Oversee platform operations and user management
- Monitor system performance and analytics
- Manage content moderation and quality control
- Configure platform settings and features
- Access comprehensive business intelligence reports

## 🎨 Frontend Features

### Modern User Interface
- **Clean, Professional Design** with intuitive navigation
- **Dark/Light Theme Support** for user preference
- **Smooth Animations** and interactive elements
- **Mobile-First Responsive Design** ensuring optimal experience across devices
- **Accessibility Features** including screen reader support and keyboard navigation

### Interactive Elements
- **HTMX-Powered** dynamic content loading without page refreshes
- **Real-time Search** with instant results and filtering
- **Interactive Property Maps** with clustering and detailed markers
- **Image Galleries** with lightbox viewing and zoom capabilities
- **Form Validation** with real-time feedback and error handling

## 🔧 Backend Architecture

### Database Design
- **Optimized PostgreSQL Schema** with proper indexing and relationships
- **Scalable Data Models** supporting complex property and user relationships
- **Efficient Querying** with select_related and prefetch_related optimizations
- **Data Integrity** with proper constraints and validation
- **Migration Management** for seamless database updates

### API Architecture
- **RESTful API Design** following industry best practices
- **Authentication & Authorization** with JWT token support
- **Rate Limiting** for API protection and fair usage
- **Comprehensive Documentation** with automatic API docs generation
- **Versioning Support** for backward compatibility

### Performance Optimization
- **Redis Caching** for frequently accessed data
- **Database Query Optimization** with efficient ORM usage
- **Static File Optimization** with compression and CDN support
- **Background Task Processing** with Celery for heavy operations
- **Monitoring & Logging** for performance tracking and debugging

## 📊 Analytics & Tracking

### User Analytics
- **Page View Tracking** with detailed user journey mapping
- **Search Behavior Analysis** including popular searches and filters
- **Property Engagement Metrics** tracking favorites, views, and inquiries
- **User Retention Analysis** with cohort tracking and engagement metrics
- **Conversion Tracking** from property views to contact submissions

### Business Intelligence
- **Property Performance Dashboards** with visual analytics
- **Agent Performance Metrics** including listing success rates
- **Market Trend Analysis** with pricing and demand insights
- **Geographic Analytics** showing popular locations and neighborhoods
- **Revenue Tracking** and commission management tools

## 🛡️ Security Features

### Data Protection
- **HTTPS Enforcement** with SSL/TLS encryption
- **CSRF Protection** on all forms and sensitive operations
- **SQL Injection Prevention** through Django ORM usage
- **XSS Protection** with proper input sanitization
- **Secure File Uploads** with type validation and scanning

### User Security
- **Strong Password Requirements** with complexity validation
- **Two-Factor Authentication** support for enhanced security
- **Session Management** with secure cookie configuration
- **Account Lockout Protection** against brute force attacks
- **Privacy Controls** with granular data sharing settings

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Getting Started
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Guidelines
- Follow PEP 8 Python style guidelines
- Write comprehensive tests for new features
- Update documentation for any API changes
- Ensure responsive design for frontend modifications
- Test across multiple browsers and devices

### Reporting Issues
- Use the GitHub issue tracker for bug reports
- Provide detailed reproduction steps
- Include system information and error logs
- Search existing issues before creating new ones

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Django Community** for the excellent web framework
- **Bootstrap Team** for the responsive UI components
- **Contributors** who have helped improve this project
- **Real Estate Professionals** who provided industry insights

---

**Made with ❤️ by SiriDev**

*For questions, support, or collaboration opportunities, please contact us at [siritech001@gmail.com](mailto:siritech001@gmail.com).*

&copy; 2024 Nuvana Realty. All rights reserved.

## 🚀 Deploying to Render

1. **Set Environment Variables in Render Dashboard:**
   - `DJANGO_SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS=.onrender.com`
   - `CLOUDINARY_CLOUD_NAME`
   - `CLOUDINARY_API_KEY`
   - `CLOUDINARY_API_SECRET`
   - `POSTGRES_DB`
   - `POSTGRES_USER`
   - `POSTGRES_PASSWORD`
   - `POSTGRES_HOST`
   - `POSTGRES_PORT`

2. **Build Command:**
   ```sh
   pip install -r requirements.txt
   python manage.py collectstatic --noinput
   python manage.py migrate
   ```

3. **Start Command:**
   ```sh
   gunicorn realtor_project.wsgi:application --bind 0.0.0.0:10000
   ```

4. **Static & Media Files:**
   - Static files are served by Whitenoise.
   - Media files are served from Cloudinary.

5. **Database:**
   - Use Render's PostgreSQL add-on or your own Postgres instance.

6. **Cloudinary:**
   - All media uploads go to Cloudinary automatically.

---
