from setuptools import setup, find_packages

setup(
    name="backend",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.100.0",
        "uvicorn>=0.20.0",
        "sqlalchemy>=2.0.0",
        "asyncpg>=0.27.0",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.0",
        "python-multipart>=0.0.6",
        "sqlmodel>=0.0.8"
    ],
    author="Todo App Developer",
    description="Backend for the Todo application",
    python_requires=">=3.8",
)