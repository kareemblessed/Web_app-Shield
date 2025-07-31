import sys
import traceback

print("🔍 Starting server diagnostics...")
print("=" * 50)

# Check Python version
print(f"Python version: {sys.version}")

# Check dependencies
missing_deps = []

try:
    import fastapi
    print(f"✅ FastAPI version: {fastapi.__version__}")
except ImportError:
    print("❌ FastAPI not installed")
    missing_deps.append("fastapi")

try:
    import uvicorn
    print(f"✅ Uvicorn available")
except ImportError:
    print("❌ Uvicorn not installed")
    missing_deps.append("uvicorn")

try:
    import jinja2
    print(f"✅ Jinja2 available")
except ImportError:
    print("❌ Jinja2 not installed")
    missing_deps.append("jinja2")

if missing_deps:
    print(f"\n💡 Install missing dependencies:")
    print(f"pip install {' '.join(missing_deps)}")
    print("Or install all at once: pip install fastapi[all]")
    sys.exit(1)

print("=" * 50)

# Now try to start the server
try:
    from fastapi import FastAPI, Request, HTTPException
    from fastapi.responses import HTMLResponse, JSONResponse
    from fastapi.templating import Jinja2Templates
    from fastapi.staticfiles import StaticFiles
    import uvicorn
    import os
    from datetime import datetime

    print("✅ All imports successful")

    app = FastAPI(title="Test Server", version="1.0.0")

    # Check if templates directory exists
    template_dir_exists = os.path.exists("templates")
    static_dir_exists = os.path.exists("static")
    
    print(f"📁 Templates directory: {'✅ Found' if template_dir_exists else '❌ Not found'}")
    print(f"📁 Static directory: {'✅ Found' if static_dir_exists else '❌ Not found'}")

    if template_dir_exists:
        templates = Jinja2Templates(directory="templates")
        print("✅ Templates initialized")
    else:
        templates = None
        print("⚠️  Using fallback HTML")

    if static_dir_exists:
        app.mount("/static", StaticFiles(directory="static"), name="static")
        print("✅ Static files mounted")

    # Sample data for your templates
    sample_data = {
        "users": [
            {"id": 1, "name": "John Doe", "email": "john@example.com"},
            {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
            {"id": 3, "name": "Bob Wilson", "email": "bob@example.com"}
        ],
        "stats": {
            "total_users": 3,
            "active_sessions": 12,
            "server_uptime": "2 hours",
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    }

    @app.get("/", response_class=HTMLResponse)
    async def home(request: Request):
        try:
            if templates and os.path.exists("templates/home.html"):
                context = {
                    "request": request,
                    "users": sample_data["users"],
                    "stats": sample_data["stats"],
                    "title": "Home"
                }
                return templates.TemplateResponse("home.html", context)
            else:
                return HTMLResponse("""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>🏠 Home - Test Server</title>
                    <style>
                        body { font-family: Arial, sans-serif; margin: 40px; background: #f0f8ff; }
                        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
                        .success { background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin: 20px 0; }
                        .info { background: #d1ecf1; color: #0c5460; padding: 15px; border-radius: 5px; margin: 20px 0; }
                        .nav { margin: 20px 0; }
                        .nav a { margin-right: 15px; color: #007bff; text-decoration: none; padding: 8px 15px; background: #f8f9fa; border-radius: 5px; }
                        .nav a:hover { background: #e9ecef; }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>🎉 Test Server is Working!</h1>
                        <div class="success">
                            <strong>Success!</strong> Your FastAPI server is running correctly.
                        </div>
                        <div class="nav">
                            <a href="/">🏠 Home</a>
                            <a href="/dashboard">📊 Dashboard</a>
                            <a href="/api/health">❤️ Health</a>
                            <a href="/docs">📖 API Docs</a>
                        </div>
                        <div class="info">
                            <strong>File Status:</strong><br>
                            • Templates directory: """ + ("✅ Found" if template_dir_exists else "❌ Missing") + """<br>
                            • Static directory: """ + ("✅ Found" if static_dir_exists else "❌ Missing") + """<br>
                            • Server time: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """
                        </div>
                        <h3>📊 Sample Data:</h3>
                        <p>Users: """ + str(len(sample_data["users"])) + """</p>
                        <h3>🔗 API Endpoints:</h3>
                        <ul>
                            <li><a href="/api/users">GET /api/users</a> - List users</li>
                            <li><a href="/api/stats">GET /api/stats</a> - Get stats</li>
                            <li><a href="/api/health">GET /api/health</a> - Health check</li>
                        </ul>
                    </div>
                </body>
                </html>
                """)
        except Exception as e:
            print(f"❌ Error in home route: {e}")
            return HTMLResponse(f"<h1>Error in home route: {str(e)}</h1>")

    @app.get("/dashboard", response_class=HTMLResponse) 
    async def dashboard(request: Request):
        try:
            if templates and os.path.exists("templates/dashboard.html"):
                context = {
                    "request": request,
                    "users": sample_data["users"],
                    "stats": sample_data["stats"],
                    "title": "Dashboard"
                }
                return templates.TemplateResponse("dashboard.html", context)
            else:
                users_list = "<br>".join([f"• {u['name']} ({u['email']})" for u in sample_data["users"]])
                return HTMLResponse(f"""
                <!DOCTYPE html>
                <html>
                <head><title>📊 Dashboard</title></head>
                <body style="font-family: Arial; margin: 40px;">
                    <h1>📊 Dashboard</h1>
                    <p>✅ Server is running!</p>
                    <p>⚠️ Add templates/dashboard.html to customize this page</p>
                    <h3>Users ({len(sample_data['users'])})</h3>
                    <div>{users_list}</div>
                    <p><a href="/">🏠 Home</a> | <a href="/api/users">👥 Users API</a></p>
                </body>
                </html>
                """)
        except Exception as e:
            print(f"❌ Error in dashboard route: {e}")
            return HTMLResponse(f"<h1>Error in dashboard route: {str(e)}</h1>")

    @app.get("/api/users")
    async def get_users():
        return {"success": True, "data": sample_data["users"], "count": len(sample_data["users"])}

    @app.get("/api/stats")
    async def get_stats():
        return {"success": True, "data": sample_data["stats"]}

    @app.get("/api/health")
    async def health_check():
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "templates_available": templates is not None,
            "static_files": static_dir_exists,
            "python_version": sys.version,
            "fastapi_version": fastapi.__version__
        }

    @app.exception_handler(404)
    async def not_found_handler(request: Request, exc: HTTPException):
        return HTMLResponse("""
        <html><body style="font-family: Arial; margin: 40px;">
        <h1>❌ Page Not Found</h1>
        <p>The page you're looking for doesn't exist.</p>
        <p><a href="/">🏠 Go Home</a></p>
        </body></html>
        """, status_code=404)

    print("✅ FastAPI app created successfully")

    if __name__ == "__main__":
        print("\n🚀 Starting test server...")
        print("📍 URL: http://127.0.0.1:8000")
        print("🏠 Home: http://127.0.0.1:8000/")
        print("📊 Dashboard: http://127.0.0.1:8000/dashboard")
        print("📖 API Docs: http://127.0.0.1:8000/docs")
        print("❤️  Health: http://127.0.0.1:8000/api/health")
        print("\n💡 If you see this message, dependencies are OK")
        print("💡 Press Ctrl+C to stop the server")
        print("=" * 50)
        
        try:
            # Try different ports if 8000 is busy
            for port in [8000, 8001, 8002, 8080]:
                try:
                    print(f"🔄 Trying port {port}...")
                    uvicorn.run(
                        app, 
                        host="127.0.0.1", 
                        port=port,
                        log_level="info"
                    )
                    break
                except OSError as e:
                    if "Address already in use" in str(e):
                        print(f"❌ Port {port} is busy, trying next...")
                        continue
                    else:
                        raise e
        except Exception as e:
            print(f"\n❌ Server failed to start: {e}")
            print(f"Error details: {traceback.format_exc()}")
            print("\n💡 Try these solutions:")
            print("1. Make sure no other server is running on port 8000")
            print("2. Try running: pip install fastapi[all]")
            print("3. Check if your firewall is blocking the connection")

except Exception as e:
    print(f"❌ Failed to import or create FastAPI app: {e}")
    print(f"Error details: {traceback.format_exc()}")
    print("\n💡 Try installing dependencies:")
    print("pip install fastapi uvicorn jinja2")