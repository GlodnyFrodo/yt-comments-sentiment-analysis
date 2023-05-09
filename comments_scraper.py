import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from textblob import TextBlob
import time


# Function that downloads comments from a YouTube video and saves them to a JSON file with sentiment score.
def get_comments(url, filename):
    # Browser initialization
    driver = webdriver.Chrome()
    driver.maximize_window()

    # Go to Yt video site
    driver.get(url)

    #Automaticly accept yt cookies
    # For english chrome browser change: @aria-label='Agree to the use of cookies and other data for the purposes described'
    consent_button_xpath = "//button[@aria-label='Zaakceptuj wykorzystywanie plików cookie i innych danych do opisanych celów']"
    consent = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, consent_button_xpath)))
    consent = driver.find_element(By.XPATH, consent_button_xpath)
    consent.click()

    # Going to end of the page to load all comments
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Finding comments elements
    comments = driver.find_elements(By.XPATH, '//*[@id="content-text"]')

    # Sentiment analysis of each comment and saving the results to a JSON file.
    results = []
    for comment in comments:
        text = comment.text
        sentiment_score = TextBlob(text).sentiment.polarity
        subjectivity_score = TextBlob(text).sentiment.subjectivity
        result = {"comment": text, "sentiment_score": sentiment_score, "subjectivity_score": subjectivity_score}
        results.append(result)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    driver.quit()