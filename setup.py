from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="openweather-wrapper", 
    version="1.0.0", 
    author="Shrish Kamboj",  
    author_email="shrishkamboz@gmail.com",  
    description="A simple Python wrapper for OpenWeatherMap API.",
    long_description=long_description,  # README.md
    long_description_content_type="text/markdown",  
    url="https://github.com/SHRISH01/openweather-wrapper", 
    project_urls={  
        "Documentation": "https://github.com/SHRISH01/openweather-wrapper/wiki",
        "Source": "https://github.com/SHRISH01/openweather-wrapper",
        "Bug Tracker": "https://github.com/SHRISH01/openweather-wrapper/issues",
    },
    
    
    packages=find_packages(),
    include_package_data=True,
    
    python_requires=">=3.12.0",

    install_requires=[
        "requests>=2.25.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",  
        "Programming Language :: Python :: 3.12",  
        "License :: OSI Approved :: MIT License",  
        "Operating System :: OS Independent", 
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    keywords="weather, OpenWeatherMap, API wrapper, python, weather data",
)
