import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ["TOKEN"]
HEADERS = {"X-USER-TOKEN": TOKEN}
USERNAME = os.environ["USER_NAME"]
URL_ACCOUNT = "https://pixe.la/v1/users"
URL_GRAPHS = f"{URL_ACCOUNT}/{USERNAME}/graphs"

def user_creation() -> None:
    """Create a new Pixela user.

    Returns:
        dict: An information stored in json telling whether the user creation process has been successful or not.
    """
    user_params = {
        "token": TOKEN,
        "username": USERNAME,
        "agreeTermsOfService": "yes",
        "notMinor": "yes"
    }

    response = requests.post(url=URL_ACCOUNT, json=user_params)
    
    data = response.json()
    print(data.get("message", data))
    return data

def graph_creation(graph_number: int, graph_name: str, unit: str, data_type: str, color: str) -> str:
    """Create a new pixelation graph definition.

    Args:
        graph_number (int): ~th number of graph you want to create (e.g. if it is your first graph then graph_number = 1, if second then graph_number=2 and so on).
        graph_name (str): It is the name of the pixelation graph.
        unit (str): It is a unit of the quantity recorded in the pixelation graph (e.g. commit, kilogram, calory).
        type (str): It is the type of quantity to be handled in the graph. Only int or float are supported.
        color (str): Defines the display color of the pixel in the pixelation graph. shibafu (green), momiji (red), sora (blue), ichou (yellow), ajisai (purple) and kuro (black) are supported as color kind.

    Returns:
        str: An ID for identifying the pixelation graph.
        dict: An information stored in json telling whether the graph creation process has been successful or not.
    """
    graph_params = {
        "id": f"graph{graph_number}",
        "name": graph_name,
        "unit": unit,
        "type": data_type,
        "color": color
    }

    response = requests.post(url=URL_GRAPHS, json=graph_params, headers=HEADERS)
    
    data = response.json()
    print(data.get("message", data))
    
    return graph_params["id"], data

def record_graph_pixel(graph: str, year: int, month:int , day: int, quantity: str) -> None:
    """It records the quantity of the specified date as a "Pixel" in specified graph.

    Args:
        graph (str): An ID for identifying the pixelation graph in which the quantity of the specified date as a "Pixel" is about to be recorded.
        year (int): The year on which the quantity is about to be recorded.
        month (int): The month on which the quantity is about to be recorded.
        day (int): The day on which the quantity is about to be recorded.
        quantity (str): Specify the quantity to be registered on the specified date.

    Returns:
        dict: An information stored in json telling whether the recording process has been successful or not.
    """
    date = datetime(year=year, month=month, day=day).strftime("%Y%m%d")
    url_pixel = f"{URL_ACCOUNT}/{USERNAME}/graphs/{graph}"
    
    pixel_body = {
        "date": date,
        "quantity": quantity
    }

    response = requests.post(url=url_pixel, json=pixel_body, headers=HEADERS)
    
    data = response.json()
    print(data.get("message", data))
    return data

def update_graph_pixel(graph: str, year: int, month:int , day: int, new_quantity: str) -> None:
    """Update the quantity already registered as a "Pixel". If target "Pixel" not exist, create a new "Pixel" and set quantity.

    Args:
        graph (str): An ID for identifying the pixelation graph in which the quantity of the specified date as a "Pixel" is about to be updated.
        year (int): The year on which the quantity is about to be updated.
        month (int): The month on which the quantity is about to be updated.
        day (int): The day on which the quantity is about to be updated.
        new_quantity (str): Specify the quantity to be registered on the specified date.
    
    Returns:
        dict: An information stored in json telling whether the pixel updating process has been successful or not.
    """
    date = datetime(year=year, month=month, day=day).strftime("%Y%m%d")
    url_changed_pixel = f"{URL_ACCOUNT}/{USERNAME}/graphs/{graph}/{date}"
    
    modified_pixel_data = {
        "quantity": new_quantity
    }

    response = requests.put(url=url_changed_pixel, json=modified_pixel_data, headers=HEADERS)
    
    data = response.json()
    print(data.get("message", data))
    return data

def delete_graph_pixel(graph: str, year: int, month:int , day: int) -> None:
    """Delete the registered "Pixel".
    Args:
        graph (str): An ID for identifying the pixelation graph in which the quantity of the specified date as a "Pixel" is about to be deleted.
        year (int): The year on which the quantity is about to be deleted.
        month (int): The month on which the quantity is about to be deleted.
        day (int): The day on which the quantity is to about be deleted.
    
    Returns:
        dict: An information stored in json telling whether the pixel deleting process has been successful or not.
    """
    to_delete = datetime(year=year, month=month, day=day).strftime("%Y%m%d")
    url_to_delete = f"{URL_ACCOUNT}/{USERNAME}/graphs/{graph}/{to_delete}"

    response = requests.delete(url = url_to_delete, headers = HEADERS)
    
    data = response.json()
    print(data.get("message", data))
    return data

#Example usage:
if __name__ == "__main__":
    user_1 = user_creation()
    graph_1 = graph_creation(1, "Spanish Words That I have learnt.", "Words", "int", "shibafu")
    recording = record_graph_pixel(graph_1[0], 2025, 9, 20, "10")
    updating = update_graph_pixel(graph_1[0], 2025, 9, 20, "20")
    deleting = delete_graph_pixel(graph_1[0], 2025, 9, 20)