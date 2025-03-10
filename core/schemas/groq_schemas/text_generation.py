from pydantic import BaseModel
import os
from typing import Dict, List

class TextGeneration(BaseModel):
    passkey : str = os.getenv("passkey","None")
    user_prompt : List[Dict[str,str]] = [
        {
            "role": "system",
            "content": "you are a helpful assistant."
        },
        {
            "role": "user",
            "content": "What is a python language?",
        }
    ]


class SuccessTextGeneration(BaseModel):
    response: str = "Python is a versatile and popular programming language known for its readability and simplicity. It's widely used in various fields, including:\n\n**1. Web Development:** Python is used to create web applications, both on the server-side (using frameworks like Django and Flask) and for client-side tasks (using libraries like PyScript).\n\n**2. Data Science and Machine Learning:** Python's extensive libraries like NumPy, Pandas, Scikit-learn, and TensorFlow make it a go-to language for data analysis, manipulation, and building machine learning models.\n\n**3. Scripting and Automation:** Python is excellent for automating tasks like system administration, web scraping, and data processing. Its clear syntax makes it easy to write scripts that can perform complex operations.\n\n**4. Game Development:** Python libraries like Pygame allow for the creation of 2D games with graphics, sound, and user interaction.\n\n**5. Desktop Applications:** Python can be used to develop graphical user interface (GUI) applications using libraries like PyQt and Tkinter.\n\n**Why Python is Popular:**\n\n* **Easy to Learn:** Python's syntax is designed to be simple and readable, making it easy for beginners to pick up.\n* **Versatile:** Its wide range of libraries and frameworks cater to a diverse set of applications.\n* **Large Community:** A vast and active community provides ample resources, support, and contributions.\n* **Open Source:** Python is free to use and distribute, making it accessible to anyone.\n* **Cross-Platform:** Python runs on various operating systems like Windows, macOS, and Linux.\n\n**In essence, Python is a powerful and user-friendly programming language that empowers developers to create a wide range of applications, from simple scripts to complex machine learning models.**\n"

    class Config:
        json_schema_extra = {
            "example": {
                "response": {
                    "text": "Python is a versatile and popular programming language known for its readability and simplicity. It's widely used in various fields, including:\n\n**1. Web Development:** Python is used to create web applications, both on the server-side (using frameworks like Django and Flask) and for client-side tasks (using libraries like PyScript).\n\n**2. Data Science and Machine Learning:** Python's extensive libraries like NumPy, Pandas, Scikit-learn, and TensorFlow make it a go-to language for data analysis, manipulation, and building machine learning models.\n\n**3. Scripting and Automation:** Python is excellent for automating tasks like system administration, web scraping, and data processing. Its clear syntax makes it easy to write scripts that can perform complex operations.\n\n**4. Game Development:** Python libraries like Pygame allow for the creation of 2D games with graphics, sound, and user interaction.\n\n**5. Desktop Applications:** Python can be used to develop graphical user interface (GUI) applications using libraries like PyQt and Tkinter.\n\n**Why Python is Popular:**\n\n* **Easy to Learn:** Python's syntax is designed to be simple and readable, making it easy for beginners to pick up.\n* **Versatile:** Its wide range of libraries and frameworks cater to a diverse set of applications.\n* **Large Community:** A vast and active community provides ample resources, support, and contributions.\n* **Open Source:** Python is free to use and distribute, making it accessible to anyone.\n* **Cross-Platform:** Python runs on various operating systems like Windows, macOS, and Linux.\n\n**In essence, Python is a powerful and user-friendly programming language that empowers developers to create a wide range of applications, from simple scripts to complex machine learning models.**\n"
                }
            }
        }