"""
PayShield UI Templates - Enhanced Landing Page and Dashboard
Beautiful, responsive templates with improved colors and mobile experience
"""

from jinja2 import Environment, FileSystemLoader, select_autoescape
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

# Initialize Jinja2 environment
templates = Jinja2Templates(directory="templates")

# Base HTML template with enhanced design
BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}PayShield Voice-Lock - Stop Invoice Fraud{% endblock %}</title>
    
    <!-- Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Source+Sans+Pro:wght@400;600&display=swap" rel="stylesheet">
    
    <!-- Icons -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    
    <!-- HTMX for live updates -->
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    
    <style>
        :root {
            /* Enhanced Color Palette */
            --primary: #0f172a;
            --primary-light: #1e293b;
            --accent: #00d4aa;
            --accent-light: #26e5c7;
            --accent-dark: #00b894;
            --success: #22c55e;
            --danger: #ef4444;
            --warning: #f59e0b;
            --info: #3b82f6;
            
            /* Sophisticated Background */
            --background: #f8fafc;
            --background-alt: #f1f5f9;
            --card-bg: #ffffff;
            --card-hover: #fefefe;
            
            /* Enhanced Text Colors */
            --text: #1e293b;
            --text-light: #64748b;
            --text-lighter: #94a3b8;
            --text-white: #ffffff;
            
            /* Modern Borders */
            --border: #e2e8f0;
            --border-light: #f1f5f9;
            --border-focus: #00d4aa;
            
            /* Enhanced Shadows */
            --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            --shadow-glow: 0 0 20px rgba(0, 212, 170, 0.15);
            
            /* Premium Gradients */
            --gradient: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
            --accent-gradient: linear-gradient(135deg, #00d4aa 0%, #26e5c7 50%, #40e0d0 100%);
            --card-gradient: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
            --hero-gradient: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
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
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }

        /* Enhanced animated background */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 80%, rgba(0, 212, 170, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(59, 130, 246, 0.06) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(139, 92, 246, 0.04) 0%, transparent 50%);
            z-index: -1;
            animation: backgroundShift 25s ease-in-out infinite;
        }

        @keyframes backgroundShift {
            0%, 100% { transform: translateX(0) translateY(0) scale(1); }
            25% { transform: translateX(-1%) translateY(-0.5%) scale(1.01); }
            50% { transform: translateX(1%) translateY(0.5%) scale(0.99); }
            75% { transform: translateX(-0.5%) translateY(1%) scale(1.01); }
        }

        /* Enhanced Header */
        .header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px) saturate(180%);
            border-bottom: 1px solid var(--border);
            padding: 1rem 0;
            box-shadow: var(--shadow);
            position: sticky;
            top: 0;
            z-index: 1000;
            transition: all 0.3s ease;
        }

        .header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0, 212, 170, 0.02), transparent);
            opacity: 0.5;
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
            font-weight: 800;
            color: var(--text);
            text-decoration: none;
            transition: all 0.3s ease;
            letter-spacing: -0.02em;
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
            animation: logoGlow 3s ease-in-out infinite;
        }

        @keyframes logoGlow {
            0%, 100% { filter: brightness(1); }
            50% { filter: brightness(1.2) drop-shadow(0 0 8px rgba(0, 212, 170, 0.3)); }
        }

        .nav-items {
            display: flex;
            gap: 2rem;
            align-items: center;
        }

        .nav-link {
            color: var(--text-light);
            text-decoration: none;
            font-weight: 500;
            padding: 0.5rem 1rem;
            border-radius: 12px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .nav-link::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: var(--accent-gradient);
            transition: left 0.3s ease;
            z-index: -1;
        }

        .nav-link:hover {
            color: var(--text-white);
            transform: translateY(-2px);
        }

        .nav-link:hover::before {
            left: 0;
        }

        /* Enhanced Button System */
        .btn-primary {
            background: var(--accent-gradient);
            color: var(--text-white);
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 12px;
            font-weight: 600;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            transition: all 0.3s ease;
            box-shadow: var(--shadow-glow);
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }

        .btn-primary::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.6s ease;
        }

        .btn-primary:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 8px 25px rgba(0, 212, 170, 0.3), var(--shadow-lg);
        }

        .btn-primary:hover::before {
            left: 100%;
        }

        /* Enhanced Container */
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }

        /* Enhanced Hero Section */
        .hero {
            padding: 5rem 0;
            text-align: center;
            position: relative;
            background: var(--hero-gradient);
            border-radius: 0 0 3rem 3rem;
            margin-bottom: 3rem;
        }

        .hero-title {
            font-size: clamp(2.5rem, 5vw, 4rem);
            font-weight: 800;
            background: var(--gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1.5rem;
            line-height: 1.1;
            letter-spacing: -0.02em;
        }

        .hero-subtitle {
            font-size: clamp(1.1rem, 2.5vw, 1.4rem);
            color: var(--text-light);
            margin-bottom: 3rem;
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
            line-height: 1.6;
        }

        .hero-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin: 4rem 0;
            max-width: 900px;
            margin-left: auto;
            margin-right: auto;
        }

        .stat-item {
            text-align: center;
            padding: 2rem;
            background: var(--card-gradient);
            border-radius: 20px;
            box-shadow: var(--shadow-lg);
            border: 1px solid var(--border);
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
        }

        .stat-item::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: var(--accent-gradient);
            transform: scaleX(0);
            transition: transform 0.4s ease;
        }

        .stat-item:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: var(--shadow-xl);
            background: var(--card-hover);
        }

        .stat-item:hover::before {
            transform: scaleX(1);
        }

        .stat-number {
            font-size: clamp(2rem, 4vw, 3rem);
            font-weight: 900;
            color: var(--accent);
            display: block;
            margin-bottom: 0.5rem;
        }

        .stat-label {
            color: var(--text-light);
            font-weight: 600;
            font-size: 1rem;
        }

        /* Enhanced Card System */
        .card {
            background: var(--card-gradient);
            border-radius: 24px;
            padding: 2.5rem;
            box-shadow: var(--shadow-lg);
            margin: 2rem 0;
            transition: all 0.4s ease;
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
            transform: scaleX(0);
            transform-origin: left;
            transition: transform 0.4s ease;
        }

        .card:hover {
            transform: translateY(-8px) scale(1.01);
            box-shadow: var(--shadow-xl);
            background: var(--card-hover);
        }

        .card:hover::before {
            transform: scaleX(1);
        }

        .card-header {
            display: flex;
            align-items: center;
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        .card-icon {
            width: 60px;
            height: 60px;
            border-radius: 16px;
            background: var(--accent-gradient);
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-white);
            font-size: 1.5rem;
            box-shadow: var(--shadow);
            animation: iconFloat 3s ease-in-out infinite;
        }

        @keyframes iconFloat {
            0%, 100% { transform: translateY(0) rotate(0deg); }
            50% { transform: translateY(-4px) rotate(2deg); }
        }

        .card-title {
            font-size: 1.6rem;
            font-weight: 700;
            color: var(--text);
            letter-spacing: -0.01em;
        }

        /* Enhanced Feature Grid */
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 2rem;
            margin: 4rem 0;
        }

        .feature-card {
            background: var(--card-gradient);
            border-radius: 20px;
            padding: 2.5rem;
            text-align: center;
            box-shadow: var(--shadow-lg);
            transition: all 0.4s ease;
            border: 1px solid var(--border);
            position: relative;
            overflow: hidden;
        }

        .feature-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: var(--accent-gradient);
            transform: scaleX(0);
            transition: transform 0.4s ease;
        }

        .feature-card:hover {
            transform: translateY(-12px) scale(1.02);
            box-shadow: var(--shadow-xl);
        }

        .feature-card:hover::before {
            transform: scaleX(1);
        }

        .feature-icon {
            width: 90px;
            height: 90px;
            margin: 0 auto 2rem;
            border-radius: 24px;
            background: var(--accent-gradient);
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-white);
            font-size: 2.2rem;
            box-shadow: var(--shadow-lg);
            transition: all 0.3s ease;
        }

        .feature-card:hover .feature-icon {
            transform: scale(1.1) rotate(5deg);
            box-shadow: var(--shadow-xl);
        }

        .feature-title {
            font-size: 1.4rem;
            font-weight: 700;
            margin-bottom: 1rem;
            color: var(--text);
            letter-spacing: -0.01em;
        }

        .feature-desc {
            color: var(--text-light);
            line-height: 1.7;
            font-size: 1rem;
        }

        /* Enhanced Status Badges */
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.6rem 1.2rem;
            border-radius: 50px;
            font-weight: 600;
            font-size: 0.9rem;
            transition: all 0.3s ease;
        }

        .status-verified {
            background: rgba(34, 197, 94, 0.1);
            color: var(--success);
            border: 1px solid rgba(34, 197, 94, 0.2);
        }

        .status-verified:hover {
            background: rgba(34, 197, 94, 0.15);
            transform: scale(1.05);
        }

        .status-pending {
            background: rgba(245, 158, 11, 0.1);
            color: var(--warning);
            border: 1px solid rgba(245, 158, 11, 0.2);
        }

        .status-pending:hover {
            background: rgba(245, 158, 11, 0.15);
            transform: scale(1.05);
        }

        .status-fraud {
            background: rgba(239, 68, 68, 0.1);
            color: var(--danger);
            border: 1px solid rgba(239, 68, 68, 0.2);
        }

        /* Enhanced Form Elements */
        .form-input {
            width: 100%;
            padding: 1.2rem 1.5rem;
            border: 2px solid var(--border);
            border-radius: 16px;
            font-size: 1rem;
            transition: all 0.3s ease;
            font-family: inherit;
            background: var(--card-bg);
            box-shadow: var(--shadow);
        }

        .form-input:focus {
            outline: none;
            border-color: var(--border-focus);
            box-shadow: 0 0 0 4px rgba(0, 212, 170, 0.1), var(--shadow-lg);
            background: var(--card-hover);
        }

        .form-input::placeholder {
            color: var(--text-lighter);
        }

        /* Enhanced Loading Animation */
        .loading {
            display: inline-flex;
            align-items: center;
            gap: 0.75rem;
            color: var(--text-light);
        }

        .spinner {
            width: 24px;
            height: 24px;
            border: 3px solid var(--border);
            border-top: 3px solid var(--accent);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* Enhanced Responsive Design */
        @media (max-width: 1024px) {
            .nav-container {
                padding: 0 1.5rem;
            }
            
            .container {
                padding: 0 1.5rem;
            }
            
            .features-grid {
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 1.5rem;
            }
        }

        @media (max-width: 768px) {
            .nav-container {
                padding: 0 1rem;
                flex-direction: column;
                gap: 1rem;
            }
            
            .nav-items {
                gap: 1rem;
                flex-wrap: wrap;
                justify-content: center;
            }
            
            .container {
                padding: 0 1rem;
            }
            
            .hero {
                padding: 3rem 0;
                border-radius: 0 0 2rem 2rem;
            }
            
            .hero-stats {
                grid-template-columns: 1fr;
                gap: 1.5rem;
                margin: 2rem 0;
            }
            
            .features-grid {
                grid-template-columns: 1fr;
                gap: 1.5rem;
                margin: 2rem 0;
            }
            
            .card {
                padding: 1.5rem;
                border-radius: 16px;
            }
            
            .card-header {
                flex-direction: column;
                text-align: center;
                gap: 1rem;
            }
        }

        @media (max-width: 480px) {
            .nav-container {
                padding: 0 0.5rem;
            }
            
            .container {
                padding: 0 0.5rem;
            }
            
            .hero {
                padding: 2rem 0;
            }
            
            .stat-item {
                padding: 1.5rem;
            }
            
            .feature-card {
                padding: 1.5rem;
            }
            
            .feature-icon {
                width: 70px;
                height: 70px;
                font-size: 1.8rem;
            }
        }

        /* Enhanced Smooth Animations */
        .fade-in {
            animation: fadeIn 0.8s ease-in-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(30px); }
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

        /* Accessibility Improvements */
        @media (prefers-reduced-motion: reduce) {
            *,
            *::before,
            *::after {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
        }

        /* Focus Styles for Accessibility */
        .btn-primary:focus,
        .nav-link:focus,
        .form-input:focus {
            outline: 2px solid var(--accent);
            outline-offset: 2px;
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
                <a href="/dashboard" class="btn-primary">
                    <i class="fas fa-tachometer-alt"></i>
                    Dashboard
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

        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // Enhanced scroll effects
        window.addEventListener('scroll', () => {
            const header = document.querySelector('.header');
            if (window.scrollY > 100) {
                header.style.background = 'rgba(255, 255, 255, 0.98)';
                header.style.backdropFilter = 'blur(25px) saturate(200%)';
            } else {
                header.style.background = 'rgba(255, 255, 255, 0.95)';
                header.style.backdropFilter = 'blur(20px) saturate(180%)';
            }
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
                <span class="stat-label">Daily Fraud Prevented</span>
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
                Impossible to fake in real-time conversations.
            </p>
        </div>

        <div class="feature-card fade-in" style="animation-delay: 0.2s">
            <div class="feature-icon">
                <i class="fas fa-user-shield"></i>
            </div>
            <h3 class="feature-title">Zero Data Exposure</h3>
            <p class="feature-desc">
                We never see your invoice contents, amounts, or details. 
                Complete privacy protection with end-to-end encryption.
            </p>
        </div>

        <div class="feature-card fade-in" style="animation-delay: 0.3s">
            <div class="feature-icon">
                <i class="fas fa-envelope"></i>
            </div>
            <h3 class="feature-title">Gmail Integration</h3>
            <p class="feature-desc">
                Works seamlessly with your existing Gmail workflow. 
                No new software to learn or complex setup required.
            </p>
        </div>

        <div class="feature-card fade-in" style="animation-delay: 0.4s">
            <div class="feature-icon">
                <i class="fas fa-certificate"></i>
            </div>
            <h3 class="feature-title">Cryptographic Badges</h3>
            <p class="feature-desc">
                RSA-signed JWT badges provide permanent, verifiable 
                proof of voice authentication for audit trails.
            </p>
        </div>

        <div class="feature-card fade-in" style="animation-delay: 0.5s">
            <div class="feature-icon">
                <i class="fas fa-mobile-alt"></i>
            </div>
            <h3 class="feature-title">Mobile Friendly</h3>
            <p class="feature-desc">
                Vendors can verify from any device. 
                Works perfectly on smartphones, tablets, and desktops.
            </p>
        </div>

        <div class="feature-card fade-in" style="animation-delay: 0.6s">
            <div class="feature-icon">
                <i class="fas fa-chart-line"></i>
            </div>
            <h3 class="feature-title">Enterprise Scale</h3>
            <p class="feature-desc">
                Handles thousands of verifications per minute. 
                Built for Fortune 500 companies with global reach.
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
                class="form-input"
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
    <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 2rem;">
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
        
        <div style="flex-shrink: 0;">
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
                style="background: var(--warning); box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3);"
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

# Verification modal template
VERIFICATION_MODAL_TEMPLATE = """
<div class="card" style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 1000; max-width: 500px; width: 90%;">
    <div class="card-header">
        <div class="card-icon">
            <i class="fas fa-microphone"></i>
        </div>
        <div>
            <h3 class="card-title">Voice Verification Challenge</h3>
            <p style="color: var(--text-light); margin: 0;">Speak the following words clearly</p>
        </div>
    </div>
    
    <div style="text-align: center; margin: 2rem 0;">
        <div style="background: var(--background); padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem;">
            <h4 style="color: var(--text); margin-bottom: 1rem;">Challenge Words:</h4>
            <div style="font-size: 1.2rem; font-weight: 600; color: var(--primary);">
                {% for word in challenge_words %}
                <span style="margin: 0 0.5rem; padding: 0.5rem 1rem; background: white; border-radius: 8px; display: inline-block; margin-bottom: 0.5rem;">{{ word }}</span>
                {% endfor %}
            </div>
        </div>
        
        <button id="start-recording" class="btn-primary" style="font-size: 1.1rem; padding: 1rem 2rem;">
            <i class="fas fa-microphone"></i>
            Start Recording
        </button>
        
        <button id="stop-recording" class="btn-primary" style="display: none; background: var(--danger);">
            <i class="fas fa-stop"></i>
            Stop Recording
        </button>
    </div>
    
    <div id="verification-result" style="margin-top: 2rem;"></div>
    
    <div style="text-align: right; margin-top: 2rem;">
        <button onclick="closeModal()" style="background: var(--text-light); color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 8px; cursor: pointer;">
            Cancel
        </button>
    </div>
</div>

<div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.5); z-index: 999;" onclick="closeModal()"></div>

<script>
function closeModal() {
    document.getElementById('verification-modal').innerHTML = '';
}

// Voice recording logic would go here
document.getElementById('start-recording').addEventListener('click', function() {
    // Start recording implementation
    this.style.display = 'none';
    document.getElementById('stop-recording').style.display = 'inline-flex';
});

document.getElementById('stop-recording').addEventListener('click', function() {
    // Stop recording and process
    this.style.display = 'none';
    document.getElementById('start-recording').style.display = 'inline-flex';
    
    // Show processing state
    document.getElementById('verification-result').innerHTML = `
        <div class="loading" style="justify-content: center; padding: 2rem;">
            <div class="spinner"></div>
            <span>Processing voice verification...</span>
        </div>
    `;
});
</script>
"""

def setup_templates():
    """Setup Jinja2 template environment"""
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    
    # Add custom filters
    env.filters['datetime'] = lambda x: x.strftime('%Y-%m-%d %H:%M:%S') if x else ''
    env.filters['currency'] = lambda x: f"${x:,.2f}" if x else '$0.00'
    
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
    'verification_modal.html': VERIFICATION_MODAL_TEMPLATE,
}

def save_templates():
    """Save all templates to files"""
    os.makedirs('templates', exist_ok=True)
    
    for filename, content in TEMPLATES.items():
        with open(f'templates/{filename}', 'w', encoding='utf-8') as f:
            f.write(content)
    
    print("✅ Enhanced templates saved to /templates/ directory")

if __name__ == "__main__":
    save_templates()
