from main import app
from fastapi.routing import APIRoute

# Print all registered routes
print("Registered routes:")
for route in app.routes:
    if hasattr(route, 'methods') and hasattr(route, 'path'):
        print(f"  {route.methods} {route.path}")

print("\nLooking for chat routes...")
chat_routes = [route for route in app.routes 
               if hasattr(route, 'path') and 'chat' in route.path.lower()]
for route in chat_routes:
    print(f"  Found chat route: {route.methods} {route.path}")