import time
from bs4 import BeautifulSoup
from tqdm import tqdm
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.utils import process_data, read_file, load_dict_from_file
from utils.webdriver_config import get_configured_driver

def mix_digital_cases_parser_ru():
    try:
        months_file_name = 'months.txt'
        months = load_dict_from_file(months_file_name)
        
        excel_path = "parsed_data/mix_digital_cases_ru.xlsx"        
        data = []
        page = 1
        limit = 10
        parsing_completed = False

        existing_data, existing_titles = read_file(excel_path)
        driver = get_configured_driver()
        
        start_parsing_time = time.time()

        for page in tqdm(range(page, limit + 1), desc="Parsing mix_digital_cases_ru"):
            if parsing_completed:
                break  # Выход из цикла если парсинг завершен
            
            url = f"https://mixdigital.com.ua/ru/blog/cases/page/{page}/"
            driver.get(url)
            
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "row")))
            except:
                break
                
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            if not soup.title or soup.title.text == "Just a moment...":
                print("Сайт блокує парсинг")
                break

            elements = soup.findAll(class_="col-lg-4 col-md-6")
            for e in elements:
                title = e.find(class_="mix-post-box-title").a.text
                if title not in existing_titles:
                    link = e.find(class_="mix-post-box-title").a.get("href")
                    temp_data = e.find(class_="mix-post-box-date").text.replace(",", "").split()
                    temp_data[1] = months.get(temp_data[1].lower())
                    date = " ".join(temp_data)
                    data.append({
                        "site": "mixdigital.com.ua/ru/blog/cases",
                        "date": date,
                        "title": title,
                        "link": link,
                    })
                else:
                    parsing_completed = True
                    break
            page += 1
        

        process_data(data, existing_data, excel_path)
        parsing_time = round(time.time()-start_parsing_time)
        print(f"Час парсингу: {parsing_time} сек")
    except Exception as e:
        print("Error:", e)
    finally:
        driver.close()
        driver.quit()


if __name__ == "__main__":
    mix_digital_cases_parser_ru()
