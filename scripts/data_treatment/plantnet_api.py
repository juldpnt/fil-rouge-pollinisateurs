import requests
import urllib.parse

"""
plantnet_api.py

This module contains the PlantNetAPIClient class which is used to interact with the PlantNet API.
The PlantNetAPIClient provides methods to make predictions based on images using the PlantNet API.

Classes:
    - PlantNetAPIClient: A class to interact with the PlantNet API.

Methods:
    - __init__(self, key:str) -> None: Initializes the PlantNet API client.
    - predict(self, imageURL:str, organs: Array[str], includeRelatedImages:bool=False) -> dict: Makes a prediction using the PlantNet API.
    - get_most_likely_species(self, prediction:dict) -> str: Returns the most likely species from a prediction result. Only for ease of use.
    
Exceptions:
    - Exception: If the API request fails, an exception is raised with the status code and the image URL.

"""

class PlantNetPredictor:
    def __init__(self, key: str) -> None:
        """
        Initializes the PlantNet API client.

        Args:
            key (str): The API key for the PlantNet API.
            This should NEVER be stored in the code.

        Attributes:
            API_URL (str): The base URL for the PlantNet API.
            _key (str): The API key for the PlantNet API.
            _project (str): The project location to use for identification. Set to 'weurope'.
            _lang (str): The language to use for identification. Set to 'fr'.
        """

        self.API_URL = "https://my-api.plantnet.org/v2/identify"
        self._key = key
        self._project = "weurope"
        self._lang = "fr"

    def predict(
        self, imageURL: str, organs: str, includeRelatedImages: bool = False
    ) -> dict:
        """
        Makes a prediction using the PlantNet API.

        Args:
            imageURL (str): The URL of the image to be predicted.
            organs (str): The organs of the plant present in the image (leaf/flower/fruit/bark/auto)
            includeRelatedImages (bool, optional): Whether to include related images in the response. Defaults to False.

        Returns:
            dict: The prediction result in JSON format.

        Raises:
            Exception: If the API request fails, an exception is raised with the status code and the image URL.
        """
        URLencoded = urllib.parse.quote(imageURL, safe="")
        URL = f"{self.API_URL}/{self._project}?images={URLencoded}&organs={organs}&lang={self._lang}&include-related-images={includeRelatedImages}&api-key={self._key}"
        response = requests.get(URL)
        status = response.status_code

        if status == 200:
            prediction = response.json()
            return prediction
        else:
            raise Exception(
                f"Error {status} while predicting image {imageURL}")

    def get_most_likely_species(self, prediction: dict) -> str:
        """
        Returns the most likely species from a prediction result.

        Args:
            prediction (dict): The prediction result in JSON format.

        Returns:
            str: The most likely species name.
        """
        return prediction["results"][0]
