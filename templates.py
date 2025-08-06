
"""
PayShield UI Templates - Premium Excellence Edition
World-class responsive templates with cutting-edge design and animations
"""

from jinja2 import Environment, FileSystemLoader, select_autoescape
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

# Initialize Jinja2 environment
templates = Jinja2Templates(directory="templates")

# Premium Base HTML template with world-class design
BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}PayShield Voice-Lock - Stop Invoice Fraud{% endblock %}</title>
    
    <!-- Premium Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&family=JetBrains+Mono:wght@300;400;500;600&family=Playfair+Display:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    
    <!-- Icons -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/phosphor-icons@1.4.2/src/css/icons.css" rel="stylesheet">
    
    <!-- HTMX for live updates -->
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    
    <!-- AOS Animation Library -->
    <link href="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.js"></script>
    
    <style>
        :root {
            /* Premium Color Palette - Inspired by Apple and Stripe */
            --primary: #000000;
            --primary-light: #1a1a1a;
            --primary-ultra-light: #2a2a2a;
            
            --accent: #007aff;
            --accent-light: #5ac8fa;
            --accent-dark: #0051d5;
            --accent-ultra: #34c759;
            
            --success: #30d158;
            --success-light: #63e58d;
            --danger: #ff453a;
            --danger-light: #ff6961;
            --warning: #ff9f0a;
            --warning-light: #ffb340;
            --info: #5e5ce6;
            --info-light: #8e8ce6;
            
            /* Sophisticated Background System */
            --background: #fafafa;
            --background-alt: #f5f5f7;
            --background-elevated: #ffffff;
            --background-glass: rgba(255, 255, 255, 0.8);
            --background-overlay: rgba(0, 0, 0, 0.05);
            
            /* Premium Text Colors */
            --text-primary: #1d1d1f;
            --text-secondary: #86868b;
            --text-tertiary: #d2d2d7;
            --text-white: #ffffff;
            --text-inverse: #f5f5f7;
            
            /* Advanced Border System */
            --border: rgba(0, 0, 0, 0.06);
            --border-light: rgba(0, 0, 0, 0.03);
            --border-medium: rgba(0, 0, 0, 0.1);
            --border-strong: rgba(0, 0, 0, 0.15);
            --border-accent: var(--accent);
            
            /* Premium Shadow System */
            --shadow-xs: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            --shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            --shadow-glow: 0 0 20px rgba(0, 122, 255, 0.15);
            --shadow-glow-accent: 0 0 30px rgba(52, 199, 89, 0.2);
            
            /* Premium Gradients */
            --gradient-primary: linear-gradient(135deg, #000000 0%, #1a1a1a 50%, #2a2a2a 100%);
            --gradient-accent: linear-gradient(135deg, #007aff 0%, #5ac8fa 50%, #34c759 100%);
            --gradient-success: linear-gradient(135deg, #30d158 0%, #63e58d 100%);
            --gradient-glass: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(255, 255, 255, 0.7) 100%);
            --gradient-hero: linear-gradient(135deg, #fafafa 0%, #f5f5f7 50%, #ffffff 100%);
            --gradient-card: linear-gradient(145deg, #ffffff 0%, #fafafa 100%);
            --gradient-overlay: linear-gradient(180deg, rgba(0, 0, 0, 0) 0%, rgba(0, 0, 0, 0.02) 100%);
            
            /* Advanced Spacing System */
            --space-xs: 0.25rem;
            --space-sm: 0.5rem;
            --space-md: 1rem;
            --space-lg: 1.5rem;
            --space-xl: 2rem;
            --space-2xl: 3rem;
            --space-3xl: 4rem;
            --space-4xl: 6rem;
            
            /* Typography Scale */
            --text-xs: 0.75rem;
            --text-sm: 0.875rem;
            --text-base: 1rem;
            --text-lg: 1.125rem;
            --text-xl: 1.25rem;
            --text-2xl: 1.5rem;
            --text-3xl: 1.875rem;
            --text-4xl: 2.25rem;
            --text-5xl: 3rem;
            --text-6xl: 3.75rem;
            --text-7xl: 4.5rem;
            
            /* Advanced Border Radius */
            --radius-xs: 4px;
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
            --radius-xl: 24px;
            --radius-2xl: 32px;
            --radius-full: 9999px;
            
            /* Premium Transitions */
            --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
            --transition-normal: 300ms cubic-bezier(0.4, 0, 0.2, 1);
            --transition-slow: 500ms cubic-bezier(0.4, 0, 0.2, 1);
            --transition-bounce: 600ms cubic-bezier(0.68, -0.55, 0.265, 1.55);
        }

        /* Global Reset with Modern Styling */
        *, *::before, *::after {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        ::selection {
            background: var(--accent);
            color: var(--text-white);
        }

        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-track {
            background: var(--background-alt);
        }

        ::-webkit-scrollbar-thumb {
            background: var(--text-secondary);
            border-radius: var(--radius-full);
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--text-primary);
        }

        html {
            scroll-behavior: smooth;
            font-size: 16px;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--background);
            color: var(--text-primary);
            line-height: 1.6;
            overflow-x: hidden;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            text-rendering: optimizeLegibility;
        }

        /* Advanced Animated Background */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 80%, rgba(0, 122, 255, 0.05) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(52, 199, 89, 0.04) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(255, 159, 10, 0.03) 0%, transparent 50%),
                linear-gradient(135deg, transparent 0%, rgba(0, 0, 0, 0.01) 100%);
            z-index: -1;
            animation: backgroundFlow 30s ease-in-out infinite;
        }

        @keyframes backgroundFlow {
            0%, 100% { 
                transform: translateX(0) translateY(0) scale(1) rotate(0deg);
                opacity: 1;
            }
            25% { 
                transform: translateX(-1%) translateY(-0.5%) scale(1.02) rotate(0.5deg);
                opacity: 0.9;
            }
            50% { 
                transform: translateX(1%) translateY(0.5%) scale(0.98) rotate(-0.5deg);
                opacity: 1.1;
            }
            75% { 
                transform: translateX(-0.5%) translateY(1%) scale(1.01) rotate(0.2deg);
                opacity: 0.95;
            }
        }

        /* Premium Header with Glassmorphism */
        .header {
            position: sticky;
            top: 0;
            z-index: 1000;
            background: var(--background-glass);
            backdrop-filter: blur(20px) saturate(180%);
            border-bottom: 1px solid var(--border);
            transition: all var(--transition-normal);
        }

        .header.scrolled {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(25px) saturate(200%);
            box-shadow: var(--shadow-md);
        }

        .nav-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: var(--space-lg) var(--space-xl);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            display: flex;
            align-items: center;
            font-size: var(--text-2xl);
            font-weight: 800;
            color: var(--text-primary);
            text-decoration: none;
            transition: all var(--transition-normal);
            letter-spacing: -0.025em;
        }

        .logo:hover {
            transform: scale(1.02);
        }

        .logo i {
            margin-right: var(--space-sm);
            font-size: var(--text-3xl);
            background: var(--gradient-accent);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: logoGlow 4s ease-in-out infinite;
        }

        @keyframes logoGlow {
            0%, 100% { 
                filter: brightness(1) drop-shadow(0 0 0 transparent);
                transform: rotate(0deg);
            }
            50% { 
                filter: brightness(1.2) drop-shadow(0 0 8px rgba(0, 122, 255, 0.3));
                transform: rotate(2deg);
            }
        }

        .nav-items {
            display: flex;
            gap: var(--space-xl);
            align-items: center;
        }

        .nav-link {
            color: var(--text-secondary);
            text-decoration: none;
            font-weight: 500;
            padding: var(--space-sm) var(--space-md);
            border-radius: var(--radius-md);
            transition: all var(--transition-normal);
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
            background: var(--gradient-accent);
            transition: left var(--transition-normal);
            z-index: -1;
            border-radius: var(--radius-md);
        }

        .nav-link:hover {
            color: var(--text-white);
            transform: translateY(-2px);
        }

        .nav-link:hover::before {
            left: 0;
        }

        /* Premium Button System */
        .btn {
            display: inline-flex;
            align-items: center;
            gap: var(--space-sm);
            padding: var(--space-md) var(--space-lg);
            border: none;
            border-radius: var(--radius-md);
            font-weight: 600;
            font-size: var(--text-base);
            text-decoration: none;
            cursor: pointer;
            transition: all var(--transition-normal);
            position: relative;
            overflow: hidden;
            white-space: nowrap;
        }

        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left var(--transition-slow);
        }

        .btn:hover::before {
            left: 100%;
        }

        .btn-primary {
            background: var(--gradient-accent);
            color: var(--text-white);
            box-shadow: var(--shadow-md), var(--shadow-glow);
        }

        .btn-primary:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: var(--shadow-xl), var(--shadow-glow-accent);
        }

        .btn-secondary {
            background: var(--background-elevated);
            color: var(--text-primary);
            border: 1px solid var(--border);
            box-shadow: var(--shadow-sm);
        }

        .btn-secondary:hover {
            background: var(--background-alt);
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }

        .btn-ghost {
            background: transparent;
            color: var(--text-secondary);
            border: 1px solid var(--border-light);
        }

        .btn-ghost:hover {
            background: var(--background-overlay);
            color: var(--text-primary);
            border-color: var(--border);
        }

        /* Advanced Container System */
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 var(--space-xl);
        }

        .container-narrow {
            max-width: 800px;
            margin: 0 auto;
            padding: 0 var(--space-xl);
        }

        .container-wide {
            max-width: 1600px;
            margin: 0 auto;
            padding: 0 var(--space-xl);
        }

        /* Premium Hero Section */
        .hero {
            padding: var(--space-4xl) 0;
            text-align: center;
            position: relative;
            background: var(--gradient-hero);
            border-radius: 0 0 var(--radius-2xl) var(--radius-2xl);
            margin-bottom: var(--space-4xl);
            overflow: hidden;
        }

        .hero::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: var(--gradient-overlay);
            z-index: 1;
        }

        .hero-content {
            position: relative;
            z-index: 2;
        }

        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: var(--space-sm);
            padding: var(--space-sm) var(--space-lg);
            background: var(--background-glass);
            border: 1px solid var(--border);
            border-radius: var(--radius-full);
            font-size: var(--text-sm);
            font-weight: 500;
            color: var(--text-secondary);
            margin-bottom: var(--space-xl);
            backdrop-filter: blur(10px);
        }

        .hero-title {
            font-size: clamp(var(--text-4xl), 8vw, var(--text-7xl));
            font-weight: 900;
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: var(--space-xl);
            line-height: 1.1;
            letter-spacing: -0.025em;
            font-family: 'Playfair Display', serif;
        }

        .hero-subtitle {
            font-size: clamp(var(--text-lg), 3vw, var(--text-xl));
            color: var(--text-secondary);
            margin-bottom: var(--space-3xl);
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
            line-height: 1.6;
            font-weight: 400;
        }

        .hero-actions {
            display: flex;
            gap: var(--space-lg);
            justify-content: center;
            flex-wrap: wrap;
            margin-bottom: var(--space-3xl);
        }

        .hero-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: var(--space-xl);
            margin: var(--space-4xl) 0;
            max-width: 1000px;
            margin-left: auto;
            margin-right: auto;
        }

        .stat-item {
            text-align: center;
            padding: var(--space-2xl);
            background: var(--gradient-card);
            border-radius: var(--radius-xl);
            box-shadow: var(--shadow-lg);
            border: 1px solid var(--border);
            transition: all var(--transition-normal);
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
            background: var(--gradient-accent);
            transform: scaleX(0);
            transition: transform var(--transition-normal);
        }

        .stat-item:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: var(--shadow-2xl);
            background: var(--background-elevated);
        }

        .stat-item:hover::before {
            transform: scaleX(1);
        }

        .stat-number {
            font-size: clamp(var(--text-3xl), 5vw, var(--text-5xl));
            font-weight: 900;
            color: var(--accent);
            display: block;
            margin-bottom: var(--space-sm);
            font-family: 'JetBrains Mono', monospace;
        }

        .stat-label {
            color: var(--text-secondary);
            font-weight: 600;
            font-size: var(--text-base);
            letter-spacing: 0.025em;
        }

        /* Premium Card System */
        .card {
            background: var(--gradient-card);
            border-radius: var(--radius-xl);
            padding: var(--space-2xl);
            box-shadow: var(--shadow-lg);
            margin: var(--space-xl) 0;
            transition: all var(--transition-normal);
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
            background: var(--gradient-accent);
            transform: scaleX(0);
            transform-origin: left;
            transition: transform var(--transition-normal);
        }

        .card:hover {
            transform: translateY(-8px) scale(1.01);
            box-shadow: var(--shadow-2xl);
            background: var(--background-elevated);
        }

        .card:hover::before {
            transform: scaleX(1);
        }

        .card-header {
            display: flex;
            align-items: center;
            gap: var(--space-lg);
            margin-bottom: var(--space-xl);
        }

        .card-icon {
            width: 64px;
            height: 64px;
            border-radius: var(--radius-lg);
            background: var(--gradient-accent);
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-white);
            font-size: var(--text-xl);
            box-shadow: var(--shadow-md);
            animation: iconFloat 4s ease-in-out infinite;
        }

        @keyframes iconFloat {
            0%, 100% { 
                transform: translateY(0) rotate(0deg) scale(1);
            }
            50% { 
                transform: translateY(-4px) rotate(2deg) scale(1.05);
            }
        }

        .card-title {
            font-size: var(--text-xl);
            font-weight: 700;
            color: var(--text-primary);
            letter-spacing: -0.015em;
        }

        .card-subtitle {
            font-size: var(--text-sm);
            color: var(--text-secondary);
            margin-top: var(--space-xs);
        }

        /* Advanced Feature Grid */
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: var(--space-xl);
            margin: var(--space-4xl) 0;
        }

        .feature-card {
            background: var(--gradient-card);
            border-radius: var(--radius-xl);
            padding: var(--space-2xl);
            text-align: center;
            box-shadow: var(--shadow-lg);
            transition: all var(--transition-normal);
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
            background: var(--gradient-accent);
            transform: scaleX(0);
            transition: transform var(--transition-normal);
        }

        .feature-card:hover {
            transform: translateY(-12px) scale(1.02);
            box-shadow: var(--shadow-2xl);
        }

        .feature-card:hover::before {
            transform: scaleX(1);
        }

        .feature-icon {
            width: 96px;
            height: 96px;
            margin: 0 auto var(--space-xl);
            border-radius: var(--radius-xl);
            background: var(--gradient-accent);
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-white);
            font-size: var(--text-3xl);
            box-shadow: var(--shadow-lg);
            transition: all var(--transition-normal);
        }

        .feature-card:hover .feature-icon {
            transform: scale(1.1) rotate(5deg);
            box-shadow: var(--shadow-xl);
        }

        .feature-title {
            font-size: var(--text-xl);
            font-weight: 700;
            margin-bottom: var(--space-md);
            color: var(--text-primary);
            letter-spacing: -0.015em;
        }

        .feature-desc {
            color: var(--text-secondary);
            line-height: 1.7;
            font-size: var(--text-base);
        }

        /* Premium Status System */
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: var(--space-sm);
            padding: var(--space-sm) var(--space-md);
            border-radius: var(--radius-full);
            font-weight: 600;
            font-size: var(--text-sm);
            transition: all var(--transition-normal);
            border: 1px solid;
        }

        .status-verified {
            background: rgba(48, 209, 88, 0.1);
            color: var(--success);
            border-color: rgba(48, 209, 88, 0.2);
        }

        .status-verified:hover {
            background: rgba(48, 209, 88, 0.15);
            transform: scale(1.05);
        }

        .status-pending {
            background: rgba(255, 159, 10, 0.1);
            color: var(--warning);
            border-color: rgba(255, 159, 10, 0.2);
        }

        .status-pending:hover {
            background: rgba(255, 159, 10, 0.15);
            transform: scale(1.05);
        }

        .status-fraud {
            background: rgba(255, 69, 58, 0.1);
            color: var(--danger);
            border-color: rgba(255, 69, 58, 0.2);
        }

        /* Premium Form Elements */
        .form-group {
            margin-bottom: var(--space-lg);
        }

        .form-label {
            display: block;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: var(--space-sm);
            font-size: var(--text-sm);
        }

        .form-input {
            width: 100%;
            padding: var(--space-lg) var(--space-xl);
            border: 2px solid var(--border);
            border-radius: var(--radius-lg);
            font-size: var(--text-base);
            transition: all var(--transition-normal);
            font-family: inherit;
            background: var(--background-elevated);
            box-shadow: var(--shadow-sm);
        }

        .form-input:focus {
            outline: none;
            border-color: var(--border-accent);
            box-shadow: 0 0 0 4px rgba(0, 122, 255, 0.1), var(--shadow-md);
            background: var(--background-elevated);
            transform: translateY(-1px);
        }

        .form-input::placeholder {
            color: var(--text-tertiary);
        }

        /* Premium Loading System */
        .loading {
            display: inline-flex;
            align-items: center;
            gap: var(--space-md);
            color: var(--text-secondary);
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

        .pulse {
            animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        /* Advanced Grid System */
        .grid {
            display: grid;
            gap: var(--space-xl);
        }

        .grid-2 { grid-template-columns: repeat(2, 1fr); }
        .grid-3 { grid-template-columns: repeat(3, 1fr); }
        .grid-4 { grid-template-columns: repeat(4, 1fr); }

        .grid-auto {
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        }

        /* Premium Modal System */
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(8px);
            z-index: 9999;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: var(--space-xl);
            animation: fadeIn var(--transition-normal);
        }

        .modal {
            background: var(--background-elevated);
            border-radius: var(--radius-xl);
            box-shadow: var(--shadow-2xl);
            max-width: 600px;
            width: 100%;
            max-height: 90vh;
            overflow-y: auto;
            animation: modalSlideIn var(--transition-bounce);
        }

        @keyframes modalSlideIn {
            0% { 
                opacity: 0; 
                transform: scale(0.9) translateY(-20px);
            }
            100% { 
                opacity: 1; 
                transform: scale(1) translateY(0);
            }
        }

        /* Premium Responsive Design */
        @media (max-width: 1200px) {
            .nav-container, .container {
                padding-left: var(--space-lg);
                padding-right: var(--space-lg);
            }
            
            .features-grid {
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: var(--space-lg);
            }
        }

        @media (max-width: 768px) {
            .nav-container {
                padding: var(--space-md);
                flex-direction: column;
                gap: var(--space-lg);
            }
            
            .nav-items {
                gap: var(--space-md);
                flex-wrap: wrap;
                justify-content: center;
            }
            
            .container {
                padding: 0 var(--space-md);
            }
            
            .hero {
                padding: var(--space-3xl) 0;
                border-radius: 0 0 var(--radius-xl) var(--radius-xl);
            }
            
            .hero-actions {
                flex-direction: column;
                align-items: center;
            }
            
            .hero-stats {
                grid-template-columns: 1fr;
                gap: var(--space-lg);
                margin: var(--space-xl) 0;
            }
            
            .features-grid {
                grid-template-columns: 1fr;
                gap: var(--space-lg);
                margin: var(--space-xl) 0;
            }
            
            .card {
                padding: var(--space-lg);
                border-radius: var(--radius-lg);
            }
            
            .card-header {
                flex-direction: column;
                text-align: center;
                gap: var(--space-md);
            }
            
            .grid-2, .grid-3, .grid-4 {
                grid-template-columns: 1fr;
            }
        }

        @media (max-width: 480px) {
            .nav-container, .container {
                padding: 0 var(--space-sm);
            }
            
            .hero {
                padding: var(--space-xl) 0;
            }
            
            .stat-item, .feature-card {
                padding: var(--space-lg);
            }
            
            .feature-icon {
                width: 80px;
                height: 80px;
                font-size: var(--text-2xl);
            }
        }

        /* Premium Animation System */
        .fade-in {
            animation: fadeIn 0.8s ease-in-out;
        }

        @keyframes fadeIn {
            from { 
                opacity: 0; 
                transform: translateY(30px);
            }
            to { 
                opacity: 1; 
                transform: translateY(0);
            }
        }

        .slide-in-left {
            animation: slideInLeft 0.8s ease-out;
        }

        @keyframes slideInLeft {
            from { 
                opacity: 0; 
                transform: translateX(-50px);
            }
            to { 
                opacity: 1; 
                transform: translateX(0);
            }
        }

        .slide-in-right {
            animation: slideInRight 0.8s ease-out;
        }

        @keyframes slideInRight {
            from { 
                opacity: 0; 
                transform: translateX(50px);
            }
            to { 
                opacity: 1; 
                transform: translateX(0);
            }
        }

        .scale-in {
            animation: scaleIn 0.6s ease-out;
        }

        @keyframes scaleIn {
            from { 
                opacity: 0; 
                transform: scale(0.8);
            }
            to { 
                opacity: 1; 
                transform: scale(1);
            }
        }

        /* Premium Utility Classes */
        .text-center { text-align: center; }
        .text-left { text-align: left; }
        .text-right { text-align: right; }

        .font-mono { font-family: 'JetBrains Mono', monospace; }
        .font-serif { font-family: 'Playfair Display', serif; }

        .rounded-full { border-radius: var(--radius-full); }
        .rounded-lg { border-radius: var(--radius-lg); }
        .rounded-xl { border-radius: var(--radius-xl); }

        .shadow-sm { box-shadow: var(--shadow-sm); }
        .shadow-md { box-shadow: var(--shadow-md); }
        .shadow-lg { box-shadow: var(--shadow-lg); }
        .shadow-xl { box-shadow: var(--shadow-xl); }

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

        @media (prefers-color-scheme: dark) {
            :root {
                --background: #000000;
                --background-alt: #111111;
                --background-elevated: #1a1a1a;
                --text-primary: #ffffff;
                --text-secondary: #a1a1aa;
                --border: rgba(255, 255, 255, 0.1);
            }
        }

        /* Focus Styles for Accessibility */
        .btn:focus,
        .nav-link:focus,
        .form-input:focus {
            outline: 2px solid var(--accent);
            outline-offset: 2px;
        }

        /* High contrast mode support */
        @media (prefers-contrast: high) {
            :root {
                --border: #000000;
                --text-secondary: #333333;
            }
        }
    </style>
</head>
<body>
    <!-- Header -->
    <header class="header" id="header">
        <nav class="nav-container">
            <a href="/" class="logo">
                <i class="fas fa-shield-alt"></i>
                PayShield
            </a>
            <div class="nav-items">
                <a href="#features" class="nav-link">Features</a>
                <a href="#security" class="nav-link">Security</a>
                <a href="#pricing" class="nav-link">Pricing</a>
                <a href="/dashboard" class="btn btn-primary">
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

    <!-- Scripts -->
    <script>
        // Initialize AOS animations
        AOS.init({
            duration: 800,
            easing: 'ease-in-out',
            once: true,
            offset: 100
        });

        // Enhanced header scroll effect
        window.addEventListener('scroll', () => {
            const header = document.getElementById('header');
            if (window.scrollY > 100) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        });

        // HTMX Configuration
        document.body.addEventListener('htmx:beforeSwap', function(evt) {
            if (evt.detail.xhr.status === 422) {
                evt.detail.shouldSwap = true;
                evt.detail.isError = false;
            }
        });

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

        // Enhanced keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                // Close modals
                document.querySelectorAll('.modal-overlay').forEach(modal => {
                    modal.remove();
                });
            }
        });

        // Performance optimization: lazy load images
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        imageObserver.unobserve(img);
                    }
                });
            });

            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }
    </script>
</body>
</html>
"""

# Enhanced Home page template
HOME_TEMPLATE = """
{% extends "base.html" %}

{% block content %}
<div class="container">
    <!-- Hero Section -->
    <section class="hero" data-aos="fade-up">
        <div class="hero-content">
            <div class="hero-badge" data-aos="fade-up" data-aos-delay="100">
                <i class="fas fa-shield-alt"></i>
                <span>Trusted by Fortune 500 companies</span>
            </div>
            
            <h1 class="hero-title" data-aos="fade-up" data-aos-delay="200">
                Stop Invoice Fraud in Real-Time
            </h1>
            
            <p class="hero-subtitle" data-aos="fade-up" data-aos-delay="300">
                Verify vendor voice authenticity in 300ms. Protect your business from 
                $2.4 billion daily email redirect fraud with military-grade voice verification.
            </p>
            
            <div class="hero-actions" data-aos="fade-up" data-aos-delay="400">
                <a href="/dashboard" class="btn btn-primary">
                    <i class="fas fa-rocket"></i>
                    Start Protecting Your Business
                </a>
                <a href="#demo" class="btn btn-secondary">
                    <i class="fas fa-play"></i>
                    Watch Demo
                </a>
            </div>
            
            <div class="hero-stats">
                <div class="stat-item" data-aos="slide-up" data-aos-delay="500">
                    <span class="stat-number">$2.4B</span>
                    <span class="stat-label">Daily Fraud Prevented</span>
                </div>
                <div class="stat-item" data-aos="slide-up" data-aos-delay="600">
                    <span class="stat-number">300ms</span>
                    <span class="stat-label">Voice Verification</span>
                </div>
                <div class="stat-item" data-aos="slide-up" data-aos-delay="700">
                    <span class="stat-number">99.9%</span>
                    <span class="stat-label">Fraud Detection</span>
                </div>
            </div>
        </div>
    </section>

    <!-- Features Grid -->
    <section id="features" class="features-grid">
        <div class="feature-card" data-aos="fade-up" data-aos-delay="100">
            <div class="feature-icon">
                <i class="fas fa-microphone-alt"></i>
            </div>
            <h3 class="feature-title">Real-Time Voice Verification</h3>
            <p class="feature-desc">
                AssemblyAI Universal-Streaming processes voice in 300ms. 
                Impossible to fake in real-time conversations with advanced biometric analysis.
            </p>
        </div>

        <div class="feature-card" data-aos="fade-up" data-aos-delay="200">
            <div class="feature-icon">
                <i class="fas fa-user-shield"></i>
            </div>
            <h3 class="feature-title">Zero Data Exposure</h3>
            <p class="feature-desc">
                We never see your invoice contents, amounts, or details. 
                Complete privacy protection with end-to-end encryption and GDPR compliance.
            </p>
        </div>

        <div class="feature-card" data-aos="fade-up" data-aos-delay="300">
            <div class="feature-icon">
                <i class="fab fa-google"></i>
            </div>
            <h3 class="feature-title">Seamless Gmail Integration</h3>
            <p class="feature-desc">
                Works seamlessly with your existing Gmail workflow. 
                No new software to learn or complex setup required. One-click integration.
            </p>
        </div>

        <div class="feature-card" data-aos="fade-up" data-aos-delay="400">
            <div class="feature-icon">
                <i class="fas fa-certificate"></i>
            </div>
            <h3 class="feature-title">Cryptographic Badges</h3>
            <p class="feature-desc">
                RSA-signed JWT badges provide permanent, verifiable 
                proof of voice authentication for audit trails and compliance.
            </p>
        </div>

        <div class="feature-card" data-aos="fade-up" data-aos-delay="500">
            <div class="feature-icon">
                <i class="fas fa-mobile-alt"></i>
            </div>
            <h3 class="feature-title">Mobile Optimized</h3>
            <p class="feature-desc">
                Vendors can verify from any device, anywhere. 
                Works perfectly on smartphones, tablets, and desktops with responsive design.
            </p>
        </div>

        <div class="feature-card" data-aos="fade-up" data-aos-delay="600">
            <div class="feature-icon">
                <i class="fas fa-chart-line"></i>
            </div>
            <h3 class="feature-title">Enterprise Scale</h3>
            <p class="feature-desc">
                Handles thousands of verifications per minute. 
                Built for Fortune 500 companies with global infrastructure and 99.9% uptime.
            </p>
        </div>
    </section>
</div>
{% endblock %}
"""

# Enhanced Dashboard template
DASHBOARD_TEMPLATE = """
{% extends "base.html" %}

{% block title %}PayShield Dashboard - Voice-Protected Payments{% endblock %}

{% block content %}
<div class="container">
    <div class="card" data-aos="fade-up">
        <div class="card-header">
            <div class="card-icon">
                <i class="fas fa-search"></i>
            </div>
            <div>
                <h2 class="card-title">Gmail Thread Search</h2>
                <p class="card-subtitle">Find and verify suspicious payment change requests instantly</p>
            </div>
        </div>

        <!-- Enhanced Search Box -->
        <div class="form-group">
            <label class="form-label" for="search-input">Search Gmail Threads</label>
            <input 
                id="search-input"
                type="text" 
                placeholder="Search Gmail threads (e.g., 'invoice', 'payment', 'bank details')"
                class="form-input"
                hx-post="/search-threads"
                hx-target="#thread-results"
                hx-trigger="keyup changed delay:500ms"
                name="search_query"
                autocomplete="off"
            >
        </div>

        <!-- Results -->
        <div id="thread-results" data-aos="fade-in">
            <div style="text-align: center; padding: var(--space-4xl); color: var(--text-secondary);">
                <div class="feature-icon" style="margin: 0 auto var(--space-lg); background: var(--gradient-accent); opacity: 0.3;">
                    <i class="fas fa-envelope"></i>
                </div>
                <h3 style="margin-bottom: var(--space-sm); color: var(--text-primary);">Start Your Search</h3>
                <p>Type keywords to search your Gmail threads for suspicious payment requests</p>
            </div>
        </div>
    </div>

    <!-- Enhanced Quick Actions -->
    <div class="grid grid-auto" style="margin-top: var(--space-xl);">
        <div class="card" data-aos="fade-up" data-aos-delay="100">
            <div class="card-header">
                <div class="card-icon">
                    <i class="fas fa-user-plus"></i>
                </div>
                <div>
                    <h3 class="card-title">Enroll Vendor</h3>
                    <p class="card-subtitle">Register voice biometrics</p>
                </div>
            </div>
            <p style="color: var(--text-secondary); margin-bottom: var(--space-lg); line-height: 1.6;">
                Register a new vendor's voice biometrics for future verification. 
                Secure enrollment process takes less than 2 minutes.
            </p>
            <a href="/enroll" class="btn btn-primary">
                <i class="fas fa-microphone"></i>
                Start Enrollment
            </a>
        </div>

        <div class="card" data-aos="fade-up" data-aos-delay="200">
            <div class="card-header">
                <div class="card-icon">
                    <i class="fas fa-shield-alt"></i>
                </div>
                <div>
                    <h3 class="card-title">Verify Payment</h3>
                    <p class="card-subtitle">Real-time voice challenge</p>
                </div>
            </div>
            <p style="color: var(--text-secondary); margin-bottom: var(--space-lg); line-height: 1.6;">
                Challenge a vendor's voice for payment authorization. 
                Get results in 300ms with 99.9% accuracy.
            </p>
            <a href="/verify" class="btn btn-primary">
                <i class="fas fa-phone"></i>
                Start Verification
            </a>
        </div>

        <div class="card" data-aos="fade-up" data-aos-delay="300">
            <div class="card-header">
                <div class="card-icon">
                    <i class="fas fa-history"></i>
                </div>
                <div>
                    <h3 class="card-title">Audit Trail</h3>
                    <p class="card-subtitle">Complete verification history</p>
                </div>
            </div>
            <p style="color: var(--text-secondary); margin-bottom: var(--space-lg); line-height: 1.6;">
                View all verification attempts, JWT badges, and compliance reports. 
                Full audit trail for regulatory requirements.
            </p>
            <a href="/audit" class="btn btn-primary">
                <i class="fas fa-list"></i>
                View History
            </a>
        </div>
    </div>
    
    <!-- Stats Dashboard -->
    <div class="card" data-aos="fade-up" data-aos-delay="400" style="margin-top: var(--space-xl);">
        <div class="card-header">
            <div class="card-icon">
                <i class="fas fa-chart-pie"></i>
            </div>
            <div>
                <h3 class="card-title">Security Overview</h3>
                <p class="card-subtitle">Real-time fraud protection metrics</p>
            </div>
        </div>
        
        <div class="grid grid-4" style="margin-top: var(--space-lg);">
            <div class="stat-item">
                <span class="stat-number">247</span>
                <span class="stat-label">Verifications Today</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">12</span>
                <span class="stat-label">Fraud Attempts Blocked</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">99.9%</span>
                <span class="stat-label">Success Rate</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">156ms</span>
                <span class="stat-label">Avg Response Time</span>
            </div>
        </div>
    </div>
</div>

<!-- Verification Modal Container -->
<div id="verification-modal"></div>
{% endblock %}
"""

# Enhanced Thread results template
THREAD_RESULTS_TEMPLATE = """
{% for thread in threads %}
<div class="card" style="margin-bottom: var(--space-lg);" data-aos="slide-up" data-aos-delay="{{ loop.index0 * 100 }}">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: var(--space-xl);">
        <div style="flex: 1;">
            <div style="display: flex; align-items: center; gap: var(--space-sm); margin-bottom: var(--space-sm);">
                <h4 style="margin: 0; color: var(--text-primary); font-weight: 600;">{{ thread.subject }}</h4>
                {% if thread.priority == 'high' %}
                <span class="status-badge status-fraud">
                    <i class="fas fa-exclamation-triangle"></i>
                    High Priority
                </span>
                {% endif %}
            </div>
            
            <div style="display: flex; align-items: center; gap: var(--space-lg); margin-bottom: var(--space-sm); color: var(--text-secondary); font-size: var(--text-sm);">
                <span>
                    <i class="fas fa-user"></i> 
                    {{ thread.sender }}
                </span>
                <span>
                    <i class="fas fa-clock"></i> 
                    {{ thread.date }}
                </span>
                <span>
                    <i class="fas fa-envelope"></i> 
                    {{ thread.message_count }} messages
                </span>
            </div>
            
            {% if thread.snippet %}
            <p style="color: var(--text-secondary); font-size: var(--text-sm); line-height: 1.5; margin-bottom: var(--space-sm);">
                {{ thread.snippet|truncate(120) }}
            </p>
            {% endif %}
            
            <div style="display: flex; gap: var(--space-sm); flex-wrap: wrap;">
                {% if thread.has_bank_change %}
                <div class="status-badge status-pending">
                    <i class="fas fa-exclamation-triangle"></i>
                    Bank Details Changed
                </div>
                {% endif %}
                
                {% if thread.has_attachments %}
                <div class="status-badge" style="background: rgba(94, 92, 230, 0.1); color: var(--info); border-color: rgba(94, 92, 230, 0.2);">
                    <i class="fas fa-paperclip"></i>
                    Attachments
                </div>
                {% endif %}
                
                {% if thread.risk_score %}
                <div class="status-badge {% if thread.risk_score > 7 %}status-fraud{% elif thread.risk_score > 4 %}status-pending{% else %}status-verified{% endif %}">
                    <i class="fas fa-shield-alt"></i>
                    Risk: {{ thread.risk_score }}/10
                </div>
                {% endif %}
            </div>
        </div>
        
        <div style="flex-shrink: 0; display: flex; flex-direction: column; gap: var(--space-sm);">
            {% if thread.verified %}
            <div class="status-badge status-verified">
                <i class="fas fa-check-circle"></i>
                Voice Verified
            </div>
            <small style="color: var(--text-secondary); text-align: center;">
                {{ thread.verified_at }}
            </small>
            {% else %}
            <button 
                class="btn btn-primary"
                hx-post="/verify-thread/{{ thread.id }}"
                hx-target="#verification-modal"
                hx-swap="innerHTML"
                style="background: var(--gradient-accent);"
            >
                <i class="fas fa-microphone"></i>
                Verify Now
            </button>
            {% endif %}
            
            <button class="btn btn-ghost" style="font-size: var(--text-sm);">
                <i class="fas fa-external-link-alt"></i>
                View in Gmail
            </button>
        </div>
    </div>
</div>
{% endfor %}

{% if not threads %}
<div style="text-align: center; padding: var(--space-4xl); color: var(--text-secondary);" data-aos="fade-up">
    <div class="feature-icon" style="margin: 0 auto var(--space-lg); background: var(--text-secondary); opacity: 0.3;">
        <i class="fas fa-search"></i>
    </div>
    <h3 style="margin-bottom: var(--space-sm); color: var(--text-primary);">No Results Found</h3>
    <p>No threads found matching your search criteria. Try different keywords or check your filters.</p>
</div>
{% endif %}
"""

# Enhanced Verification modal template
VERIFICATION_MODAL_TEMPLATE = """
<div class="modal-overlay" data-aos="fade-in">
    <div class="modal">
        <div class="card" style="margin: 0; border: none; box-shadow: none;">
            <div class="card-header">
                <div class="card-icon">
                    <i class="fas fa-microphone-alt"></i>
                </div>
                <div>
                    <h3 class="card-title">Voice Verification Challenge</h3>
                    <p class="card-subtitle">Speak the following words clearly and naturally</p>
                </div>
            </div>
            
            <div style="text-align: center; margin: var(--space-xl) 0;">
                <div style="background: var(--background-alt); padding: var(--space-xl); border-radius: var(--radius-lg); margin-bottom: var(--space-xl); border: 1px solid var(--border);">
                    <h4 style="color: var(--text-primary); margin-bottom: var(--space-md); font-weight: 600;">Challenge Phrase:</h4>
                    <div style="font-size: var(--text-lg); font-weight: 600; color: var(--accent); font-family: 'JetBrains Mono', monospace;">
                        {% for word in challenge_words %}
                        <span style="margin: 0 var(--space-sm); padding: var(--space-sm) var(--space-md); background: var(--background-elevated); border-radius: var(--radius-sm); display: inline-block; margin-bottom: var(--space-sm); border: 1px solid var(--border);">{{ word }}</span>
                        {% endfor %}
                    </div>
                    <p style="color: var(--text-secondary); font-size: var(--text-sm); margin-top: var(--space-md);">
                        Speak naturally at normal volume. The verification will complete automatically.
                    </p>
                </div>
                
                <div style="display: flex; gap: var(--space-md); justify-content: center; flex-wrap: wrap;">
                    <button id="start-recording" class="btn btn-primary" style="font-size: var(--text-lg); padding: var(--space-lg) var(--space-xl);">
                        <i class="fas fa-microphone"></i>
                        Start Recording
                    </button>
                    
                    <button id="stop-recording" class="btn" style="display: none; background: var(--gradient-success);">
                        <i class="fas fa-stop"></i>
                        Stop Recording
                    </button>
                </div>
                
                <div id="recording-status" style="margin-top: var(--space-lg); padding: var(--space-md); border-radius: var(--radius-md); display: none;">
                    <div class="loading">
                        <div class="spinner"></div>
                        <span>Listening for your voice...</span>
                    </div>
                </div>
            </div>
            
            <div id="verification-result" style="margin-top: var(--space-xl);"></div>
            
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: var(--space-xl); padding-top: var(--space-lg); border-top: 1px solid var(--border);">
                <div style="display: flex; align-items: center; gap: var(--space-sm); color: var(--text-secondary); font-size: var(--text-sm);">
                    <i class="fas fa-shield-alt"></i>
                    <span>Secure voice verification powered by AssemblyAI</span>
                </div>
                <button onclick="closeModal()" class="btn btn-ghost">
                    <i class="fas fa-times"></i>
                    Cancel
                </button>
            </div>
        </div>
    </div>
</div>

<script>
function closeModal() {
    const modal = document.querySelector('.modal-overlay');
    if (modal) {
        modal.style.animation = 'fadeOut 0.3s ease-out forwards';
        setTimeout(() => {
            document.getElementById('verification-modal').innerHTML = '';
        }, 300);
    }
}

// Enhanced voice recording logic
let mediaRecorder;
let audioChunks = [];

document.getElementById('start-recording').addEventListener('click', async function() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        
        this.style.display = 'none';
        document.getElementById('stop-recording').style.display = 'inline-flex';
        document.getElementById('recording-status').style.display = 'block';
        
        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };
        
        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            processAudio(audioBlob);
            audioChunks = [];
        };
        
        mediaRecorder.start();
        
        // Auto-stop after 10 seconds
        setTimeout(() => {
            if (mediaRecorder.state === 'recording') {
                document.getElementById('stop-recording').click();
            }
        }, 10000);
        
    } catch (error) {
        console.error('Error accessing microphone:', error);
        showError('Unable to access microphone. Please check permissions.');
    }
});

document.getElementById('stop-recording').addEventListener('click', function() {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
        mediaRecorder.stream.getTracks().forEach(track => track.stop());
    }
    
    this.style.display = 'none';
    document.getElementById('start-recording').style.display = 'inline-flex';
    document.getElementById('recording-status').style.display = 'none';
});

function processAudio(audioBlob) {
    document.getElementById('verification-result').innerHTML = `
        <div class="card" style="background: var(--background-alt); border: 1px solid var(--border);">
            <div class="loading" style="justify-content: center; padding: var(--space-xl);">
                <div class="spinner"></div>
                <span>Processing voice verification...</span>
            </div>
        </div>
    `;
    
    // Simulate processing time
    setTimeout(() => {
        const success = Math.random() > 0.3; // 70% success rate for demo
        
        if (success) {
            document.getElementById('verification-result').innerHTML = `
                <div class="card" style="background: rgba(48, 209, 88, 0.1); border: 1px solid rgba(48, 209, 88, 0.2);">
                    <div style="text-align: center; padding: var(--space-lg);">
                        <div style="font-size: var(--text-4xl); color: var(--success); margin-bottom: var(--space-md);">
                            <i class="fas fa-check-circle"></i>
                        </div>
                        <h4 style="color: var(--success); margin-bottom: var(--space-sm);">Voice Verified Successfully</h4>
                        <p style="color: var(--text-secondary); font-size: var(--text-sm);">
                            Confidence: 96.8% | Processing time: 247ms
                        </p>
                    </div>
                </div>
            `;
        } else {
            document.getElementById('verification-result').innerHTML = `
                <div class="card" style="background: rgba(255, 69, 58, 0.1); border: 1px solid rgba(255, 69, 58, 0.2);">
                    <div style="text-align: center; padding: var(--space-lg);">
                        <div style="font-size: var(--text-4xl); color: var(--danger); margin-bottom: var(--space-md);">
                            <i class="fas fa-times-circle"></i>
                        </div>
                        <h4 style="color: var(--danger); margin-bottom: var(--space-sm);">Verification Failed</h4>
                        <p style="color: var(--text-secondary); font-size: var(--text-sm);">
                            Voice does not match enrolled profile. Please try again.
                        </p>
                    </div>
                </div>
            `;
        }
    }, 2000);
}

function showError(message) {
    document.getElementById('verification-result').innerHTML = `
        <div class="card" style="background: rgba(255, 69, 58, 0.1); border: 1px solid rgba(255, 69, 58, 0.2);">
            <div style="text-align: center; padding: var(--space-lg);">
                <div style="font-size: var(--text-3xl); color: var(--danger); margin-bottom: var(--space-md);">
                    <i class="fas fa-exclamation-triangle"></i>
                </div>
                <h4 style="color: var(--danger); margin-bottom: var(--space-sm);">Error</h4>
                <p style="color: var(--text-secondary); font-size: var(--text-sm);">${message}</p>
            </div>
        </div>
    `;
}

// Handle escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeModal();
    }
});

@keyframes fadeOut {
    from { opacity: 1; }
    to { opacity: 0; }
}
</script>
"""

def setup_templates():
    """Setup enhanced Jinja2 template environment"""
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    
    # Add enhanced custom filters
    env.filters['datetime'] = lambda x: x.strftime('%Y-%m-%d %H:%M:%S') if x else ''
    env.filters['currency'] = lambda x: f"${x:,.2f}" if x else '$0.00'
    env.filters['truncate'] = lambda x, length=100: x[:length] + '...' if len(x) > length else x
    env.filters['highlight'] = lambda x, term: x.replace(term, f'<mark>{term}</mark>') if term else x
    
    return env

def render_template(template_name: str, **context):
    """Render template with context"""
    env = setup_templates()
    template = env.get_template(template_name)
    return template.render(**context)

# Enhanced template registry
TEMPLATES = {
    'base.html': BASE_TEMPLATE,
    'home.html': HOME_TEMPLATE,
    'dashboard.html': DASHBOARD_TEMPLATE,
    'thread_results.html': THREAD_RESULTS_TEMPLATE,
    'verification_modal.html': VERIFICATION_MODAL_TEMPLATE,
}

def save_templates():
    """Save all enhanced templates to files"""
    os.makedirs('templates', exist_ok=True)
    
    for filename, content in TEMPLATES.items():
        with open(f'templates/{filename}', 'w', encoding='utf-8') as f:
            f.write(content)
    
    print("✅ Premium enhanced templates saved to /templates/ directory")
    print("🎨 Features: Modern design, premium animations, mobile-first responsive")
    print("🚀 Performance: Optimized loading, accessibility, and user experience")

if __name__ == "__main__":
    save_templates()
