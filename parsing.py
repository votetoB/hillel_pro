from bs4 import BeautifulSoup
import requests
from selenium import webdriver


if __name__ == "__main__":
    response = requests.get("https://google.com.ua")
    soup = BeautifulSoup(response.content)
    driver = webdriver.Firefox()
    driver.get("https://google.com.ua")
