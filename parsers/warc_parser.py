import time
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from utils.utils import process_data, read_file, load_dict_from_file
from utils.webdriver_config import get_configured_driver

def warc_parser():
    try:
        # Файл для стандартизації назви місяця
        months_file_name = 'months.txt'
        months = load_dict_from_file(months_file_name) 
        
        excel_path = "parsed_data/warc.xlsx"        
        data = []

        start_parsing_time = time.time()

        existing_data, existing_titles = read_file(excel_path)
    
        driver = get_configured_driver(disable_javascript=False)
        url = "https://www.warc.com/feed/"
        driver.get(url)
        
        # Очікування провантаження сторінки (код чекає поки в HTML сторінки з'явиться клас із шуканим ім'ям)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'modal')))

        button_cookies = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
        time.sleep(1)
        button_cookies.click()

        find_element = driver.find_element(By.CLASS_NAME, "hide-desktop")
        for _ in range(1, 30):
            action = ActionChains(driver)
            action.move_to_element(find_element).perform()
            scroll_by = 'window.scrollBy(0, 300);'
            driver.execute_script(scroll_by)
            time.sleep(2)
        
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        if not soup.title or soup.title.text == "Just a moment...":
            print("Сайт блокує парсинг")

        elements = soup.find('section', id='feed-grid').findAll(class_="modal")
        for e in elements:
            title = e.find(class_="feed-show-details").h5.text
            if title not in existing_titles:
                temp_date = e.find(class_="tag date").text.split()
                temp_date[1] = months.get(temp_date[1].lower())
                date = " ".join(temp_date)
                link = "https://www.warc.com/" + e["data-item-url"]
                data.append({
                    "site": "warc.com/feed",
                    "date": date,
                    "title": title,
                    "link": link,
                })
            else:
                break

        process_data(data, existing_data, excel_path)
        parsing_time = round(time.time()-start_parsing_time)
        print(f"Час парсингу: {parsing_time} сек")
    except Exception as e:
        print("Error:", e)
    finally:
        driver.close()
        driver.quit()

if __name__ == "__main__":
    warc_parser()