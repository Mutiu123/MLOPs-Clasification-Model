from setuptools import setup, find_packages 

setup(
    name="h2_pipeline_detection",
    version="1.0.0",
    author="Mutiu Adegboye",
    author_email="adegboyemutiu@gmail.com",
    description="Hydrogen Pipeline Leak Detection and Characterization System",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "pydantic",
        "pandas",
        "numpy",
        "scikit-learn",
        "pymongo",
        "boto3",
        "python-dotenv",
        "pyyaml",
        "dill",
        "prometheus-client",
        "python-json-logger",
        "python-multipart",
        "PyJWT",
        "from-root",
    ]
)