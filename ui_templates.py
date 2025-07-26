"""

"""

from jinja2 import Environment, FileSystemLoader, select_autoescape
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

# Initialize Jinja2 environment
templates = Jinja2Templates(directory="templates")

# Base HTML template with stunning design
BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}PayShield Voice-Lock - Stop Invoice Fraud{% endblock %}</title>
    
    <!-- Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Source+Sans+Pro:wght@400;600&display=swap" rel="stylesheet">
    
    <!-- Icons -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    
    <!-- HTMX for live updates -->
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    
    <style>
        :root {
            --primary: #1a365d;
            --accent: #00d4aa;
            --success: #38a169;
            --danger: #e53e3e;
            --warning: #ed8936;
            --background: #f7fafc;
            --card-bg: #ffffff;
            --text: #2d3748;
            --text-light: #718096;
            --border: #e2e8f0;
            --shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            --gradient: linear-gradient(135deg, #1a365d 0%, #2d5a87 100%);
            --accent-gradient: linear-gradient(135deg, #00d4aa 0%, #00b894 100%);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            background: var(--background);
            color: var(--text);
            line-height: 1.6;
            overflow-x: hidden;
        }

        /* Animated background */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, #f0f9ff, #e0f7fa, #f7fafc);
            z-index: -1;
            animation: backgroundShift 20s ease-in-out infinite;
        }

        @keyframes backgroundShift {
            0%, 100% { transform: translateX(0) translateY(0); }
            25% { transform: translateX(-2%) translateY(-1%); }
            50% { transform: translateX(2%) translateY(1%); }
            75% { transform: translateX(-1%) translateY(2%); }
        }

        /* Header */
        .header {
            background: var(--gradient);
            padding: 1rem 0;
            box-shadow: var(--shadow);
            position: relative;
            overflow: hidden;
        }

        .header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="0.5"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
            opacity: 0.3;
        }

        .nav-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: relative;
            z-index: 1;
        }

        .logo {
            display: flex;
            align-items: center;
            font-size: 1.8rem;
            font-weight: 700;
            color: white;
            text-decoration: none;
            transition: transform 0.3s ease;
        }

        .logo:hover {
            transform: scale(1.05);
        }

        .logo i {
            margin-right: 0.5rem;
            font-size: 2rem;
            background: var(--accent-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: pulse 2s ease-in-out infinite;
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }

        .nav-items {
            display: flex;
            gap: 2rem;
            align-items: center;
        }

        .nav-link {
            color: white;
            text-decoration: none;
            font-weight: 500;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            transition: all 0.3s ease;
            position: relative;
        }

        .nav-link:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateY(-2px);
        }

        .btn-primary {
            background: var(--accent-gradient);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 12px;
            font-weight: 600;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 212, 170, 0.3);
        }

        .btn-primary:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0, 212, 170, 0.4);
        }

        /* Main content container */
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }

        /* Hero section */
        .hero {
            padding: 4rem 0;
            text-align: center;
            position: relative;
        }

        .hero-title {
            font-size: 3.5rem;
            font-weight: 700;
            background: var(--gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
            line-height: 1.2;
        }

        .hero-subtitle {
            font-size: 1.3rem;
            color: var(--text-light);
            margin-bottom: 2rem;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }

        .hero-stats {
            display: flex;
            justify-content: center;
            gap: 3rem;
            margin: 3rem 0;
            flex-wrap: wrap;
        }

        .stat-item {
            text-align: center;
            padding: 1.5rem;
            background: var(--card-bg);
            border-radius: 16px;
            box-shadow: var(--shadow);
            min-width: 200px;
            transition: transform 0.3s ease;
        }

        .stat-item:hover {
            transform: translateY(-5px);
        }

        .stat-number {
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--danger);
            display: block;
        }

        .stat-label {
            color: var(--text-light);
            font-weight: 500;
            margin-top: 0.5rem;
        }

        /* Card styles */
        .card {
            background: var(--card-bg);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: var(--shadow);
            margin: 2rem 0;
            transition: all 0.3s ease;
            border: 1px solid var(--border);
            position: relative;
            overflow: hidden;
        }

        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: var(--accent-gradient);
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
        }

        .card-header {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1.5rem;
        }

        .card-icon {
            width: 50px;
            height: 50px;
            border-radius: 12px;
            background: var(--accent-gradient);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.5rem;
        }

        .card-title {
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--text);
        }

        /* Feature grid */
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin: 3rem 0;
        }

        .feature-card {
            background: var(--card-bg);
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
            box-shadow: var(--shadow);
            transition: all 0.3s ease;
            border: 1px solid var(--border);
        }

        .feature-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
        }

        .feature-icon {
            width: 80px;
            height: 80px;
            margin: 0 auto 1.5rem;
            border-radius: 20px;
            background: var(--accent-gradient);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 2rem;
        }

        .feature-title {
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: var(--text);
        }

        .feature-desc {
            color: var(--text-light);
            line-height: 1.6;
        }

        /* Status indicators */
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            border-radius: 50px;
            font-weight: 500;
            font-size: 0.9rem;
        }

        .status-verified {
            background: rgba(56, 161, 105, 0.1);
            color: var(--success);
            border: 1px solid rgba(56, 161, 105, 0.2);
        }

        .status-pending {
            background: rgba(237, 137, 54, 0.1);
            color: var(--warning);
            border: 1px solid rgba(237, 137, 54, 0.2);
        }

        .status-fraud {
            background: rgba(229, 62, 62, 0.1);
            color: var(--danger);
            border: 1px solid rgba(229, 62, 62, 0.2);
        }

        /* Loading animation */
        .loading {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }

        .spinner {
            width: 20px;
            height: 20px;
            border: 2px solid var(--border);
            border-top: 2px solid var(--accent);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* Responsive design */
        @media (max-width: 768px) {
            .hero-title {
                font-size: 2.5rem;
            }
            
            .nav-container {
                padding: 0 1rem;
            }
            
            .container {
                padding: 0 1rem;
            }
            
            .hero-stats {
                gap: 1rem;
            }
            
            .features-grid {
                grid-template-columns: 1fr;
            }
        }

        /* Smooth animations */
        .fade-in {
            animation: fadeIn 0.8s ease-in-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .slide-in-left {
            animation: slideInLeft 0.8s ease-out;
        }

        @keyframes slideInLeft {
            from { opacity: 0; transform: translateX(-50px); }
            to { opacity: 1; transform: translateX(0); }
        }

        .slide-in-right {
            animation: slideInRight 0.8s ease-out;
        }

        @keyframes slideInRight {
            from { opacity: 0; transform: translateX(50px); }
            to { opacity: 1; transform: translateX(0); }
        }
    </style>
</head>
<body>
    <!-- Header -->
    <header class="header">
        <nav class="nav-container">
            <a href="/" class="logo">
                <i class="fas fa-shield-alt"></i>
                PayShield
            </a>
            <div class="nav-items">
                <a href="#features" class="nav-link">Features</a>
                <a href="#security" class="nav-link">Security</a>
                <a href="#pricing" class="nav-link">Pricing</a>
                <a href="/login" class="btn-primary">
                    <i class="fab fa-google"></i>
                    Sign In with Google
                </a>
            </div>
        </nav>
    </header>

    <!-- Main content -->
    <main>
        {% block content %}{% endblock %}
    </main>

    <!-- HTMX configuration -->
    <script>
        // Configure HTMX for smooth updates
        document.body.addEventListener('htmx:beforeSwap', function(evt) {
            if (evt.detail.xhr.status === 422) {
                evt.detail.shouldSwap = true;
                evt.detail.isError = false;
            }
        });

        // Add loading states
        document.body.addEventListener('htmx:beforeRequest', function(evt) {
            evt.target.classList.add('loading');
        });

        document.body.addEventListener('htmx:afterRequest', function(evt) {
            evt.target.classList.remove('loading');
        });
    </script>
</body>
</html>
"""

# Home page template
HOME_TEMPLATE = """
{% extends "base.html" %}

{% block content %}
<div class="container">
    <!-- Hero Section -->
    <section class="hero fade-in">
        <h1 class="hero-title">Stop Invoice Fraud in Real-Time</h1>
        <p class="hero-subtitle">
            Verify vendor voice authenticity in 300ms. Protect your business from 
            $2.4 billion daily email redirect fraud with military-grade voice verification.
        </p>
        
        <div class="hero-stats">
            <div class="stat-item slide-in-left">
                <span class="stat-number">$2.4B</span>
                <span class="stat-label">Prevents Daily to Fraud</span>
            </div>
            <div class="stat-item fade-in" style="animation-delay: 0.2s">
                <span class="stat-number">300ms</span>
                <span class="stat-label">Voice Verification</span>
            </div>
            <div class="stat-item slide-in-right">
                <span class="stat-number">99.5%</span>
                <span class="stat-label">Fraud Detection</span>
            </div>
        </div>

        <a href="/dashboard" class="btn-primary" style="font-size: 1.1rem; padding: 1rem 2rem;">
            <i class="fas fa-rocket"></i>
            Start Protecting Your Business
        </a>
    </section>

    <!-- Features Grid -->
    <section id="features" class="features-grid">
        <div class="feature-card fade-in" style="animation-delay: 0.1s">
            <div class="feature-icon">
                <i class="fas fa-microphone"></i>
            </div>
            <h3 class="feature-title">Real-Time Voice Verification</h3>
            <p class="feature-desc">
                AssemblyAI Universal-Streaming processes voice in 300ms. 
                Impossible to fake in real-time.
            </p>
        </div>

        <div class="feature-card fade-in" style="animation-delay: 0.2s">
            <div class="feature-icon">
                <i class="fas fa-lock"></i>
            </div>
            <h3 class="feature-title">Zero Data Exposure</h3>
            <p class="feature-desc">
                We never see your invoice contents, amounts, or details. 
                Complete privacy protection.
            </p>
        </div>

        <div class="feature-card fade-in" style="animation-delay: 0.3s">
            <div class="feature-icon">
                <i class="fas fa-envelope"></i>
            </div>
            <h3 class="feature-title">Gmail Integration</h3>
            <p class="feature-desc">
                Works seamlessly with your existing Gmail workflow. 
                No new software to learn.
            </p>
        </div>

        <div class="feature-card fade-in" style="animation-delay: 0.4s">
            <div class="feature-icon">
                <i class="fas fa-certificate"></i>
            </div>
            <h3 class="feature-title">Cryptographic Badges</h3>
            <p class="feature-desc">
                RSA-signed JWT badges provide permanent, verifiable 
                proof of voice authentication.
            </p>
        </div>

        <div class="feature-card fade-in" style="animation-delay: 0.5s">
            <div class="feature-icon">
                <i class="fas fa-mobile-alt"></i>
            </div>
            <h3 class="feature-title">Mobile Friendly</h3>
            <p class="feature-desc">
                Vendors can verify from any device. 
                Works perfectly on smartphones and tablets.
            </p>
        </div>

        <div class="feature-card fade-in" style="animation-delay: 0.6s">
            <div class="feature-icon">
                <i class="fas fa-chart-line"></i>
            </div>
            <h3 class="feature-title">Enterprise Scale</h3>
            <p class="feature-desc">
                Handles thousands of verifications per minute. 
                Built for Fortune 500 companies.
            </p>
        </div>
    </section>
</div>
{% endblock %}
"""

# Dashboard template
DASHBOARD_TEMPLATE = """
{% extends "base.html" %}

{% block title %}PayShield Dashboard - Voice-Protected Payments{% endblock %}

{% block content %}
<div class="container">
    <div class="card fade-in">
        <div class="card-header">
            <div class="card-icon">
                <i class="fas fa-search"></i>
            </div>
            <div>
                <h2 class="card-title">Gmail Thread Search</h2>
                <p style="color: var(--text-light); margin: 0;">Find and verify suspicious payment change requests</p>
            </div>
        </div>

        <!-- Search Box -->
        <div style="margin-bottom: 2rem;">
            <input 
                type="text" 
                placeholder="Search Gmail threads (e.g., 'invoice', 'payment', 'bank details')"
                style="width: 100%; padding: 1rem; border: 2px solid var(--border); border-radius: 12px; font-size: 1rem; transition: all 0.3s ease;"
                hx-post="/search-threads"
                hx-target="#thread-results"
                hx-trigger="keyup changed delay:500ms"
                name="search_query"
            >
        </div>

        <!-- Results -->
        <div id="thread-results" class="fade-in">
            <div style="text-align: center; padding: 3rem; color: var(--text-light);">
                <i class="fas fa-envelope" style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.5;"></i>
                <p>Start typing to search your Gmail threads</p>
            </div>
        </div>
    </div>

    <!-- Quick Actions -->
    <div class="features-grid" style="margin-top: 2rem;">
        <div class="card">
            <div class="card-header">
                <div class="card-icon">
                    <i class="fas fa-user-plus"></i>
                </div>
                <h3 class="card-title">Enroll Vendor</h3>
            </div>
            <p style="color: var(--text-light); margin-bottom: 1.5rem;">
                Register a new vendor's voice for future verification
            </p>
            <a href="/enroll" class="btn-primary">
                <i class="fas fa-microphone"></i>
                Start Enrollment
            </a>
        </div>

        <div class="card">
            <div class="card-header">
                <div class="card-icon">
                    <i class="fas fa-shield-alt"></i>
                </div>
                <h3 class="card-title">Verify Payment</h3>
            </div>
            <p style="color: var(--text-light); margin-bottom: 1.5rem;">
                Challenge a vendor's voice for payment authorization
            </p>
            <a href="/verify" class="btn-primary">
                <i class="fas fa-phone"></i>
                Start Verification
            </a>
        </div>

        <div class="card">
            <div class="card-header">
                <div class="card-icon">
                    <i class="fas fa-history"></i>
                </div>
                <h3 class="card-title">Audit Trail</h3>
            </div>
            <p style="color: var(--text-light); margin-bottom: 1.5rem;">
                View all verification attempts and JWT badges
            </p>
            <a href="/audit" class="btn-primary">
                <i class="fas fa-list"></i>
                View History
            </a>
        </div>
    </div>
</div>
{% endblock %}
"""

# Thread results template (for HTMX updates)
THREAD_RESULTS_TEMPLATE = """
{% for thread in threads %}
<div class="card" style="margin-bottom: 1rem; animation: slideInLeft 0.5s ease-out;">
    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
        <div style="flex: 1;">
            <h4 style="margin-bottom: 0.5rem; color: var(--text);">{{ thread.subject }}</h4>
            <p style="color: var(--text-light); margin-bottom: 0.5rem;">
                <i class="fas fa-user"></i> {{ thread.sender }}
            </p>
            <p style="color: var(--text-light); font-size: 0.9rem;">
                <i class="fas fa-clock"></i> {{ thread.date }}
            </p>
            
            {% if thread.has_bank_change %}
            <div class="status-badge status-pending" style="margin-top: 1rem;">
                <i class="fas fa-exclamation-triangle"></i>
                Bank Details Changed
            </div>
            {% endif %}
        </div>
        
        <div style="margin-left: 2rem;">
            {% if thread.verified %}
            <div class="status-badge status-verified">
                <i class="fas fa-check-circle"></i>
                Voice Verified
            </div>
            {% else %}
            <button 
                class="btn-primary"
                hx-post="/verify-thread/{{ thread.id }}"
                hx-target="#verification-modal"
                hx-swap="innerHTML"
                style="background: var(--warning); box-shadow: 0 4px 15px rgba(237, 137, 54, 0.3);"
            >
                <i class="fas fa-microphone"></i>
                Verify Now
            </button>
            {% endif %}
        </div>
    </div>
</div>
{% endfor %}

{% if not threads %}
<div style="text-align: center; padding: 2rem; color: var(--text-light);">
    <i class="fas fa-search" style="font-size: 2rem; margin-bottom: 1rem; opacity: 0.5;"></i>
    <p>No threads found matching your search</p>
</div>
{% endif %}
"""

def setup_templates():
    """Setup Jinja2 template environment"""
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    
    # Add custom filters
    env.filters['datetime'] = lambda x: x.strftime('%Y-%m-%d %H:%M:%S')
    
    return env

def render_template(template_name: str, **context):
    """Render template with context"""
    env = setup_templates()
    template = env.get_template(template_name)
    return template.render(**context)

# Template registry
TEMPLATES = {
    'base.html': BASE_TEMPLATE,
    'home.html': HOME_TEMPLATE,
    'dashboard.html': DASHBOARD_TEMPLATE,
    'thread_results.html': THREAD_RESULTS_TEMPLATE,
}

def save_templates():
    """Save all templates to files"""
    os.makedirs('templates', exist_ok=True)
    
    for filename, content in TEMPLATES.items():
        with open(f'templates/{filename}', 'w', encoding='utf-8') as f:
            f.write(content)
    
    print("✅ All templates saved to /templates/ directory")

if __name__ == "__main__":
    save_templates()