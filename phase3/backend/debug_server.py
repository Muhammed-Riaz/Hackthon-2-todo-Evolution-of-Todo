import sys
import traceback
from main import app
from fastapi.responses import JSONResponse
import uvicorn

# Add exception handler
@app.exception_handler(500)
async def custom_http_exception_handler(request, exc):
    print(f"Internal server error: {exc}")
    import traceback
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error occurred"}
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)