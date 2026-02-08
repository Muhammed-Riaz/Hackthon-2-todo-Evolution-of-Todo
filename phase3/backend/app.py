from src.main import app

# This file serves as the entry point for Hugging Face Spaces
# The app object is imported from src.main

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)