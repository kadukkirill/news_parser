import time
import re
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.utils import process_data, read_file, load_dict_from_file
from utils.webdriver_config import get_configured_driver


def detector_media_rinok_parser():
    try:
        months_file_name = 'months.txt'
        months = load_dict_from_file(months_file_name)
        
        excel_path = "parsed_data/detector_media_rinok.xlsx"        
        data = []
        page = 1
        limit = 30
        parsing_completed = False

        pattern = re.compile(r'cat_blkPost\s+cat_limit_\d+')
        pattern2 = re.compile(r"cat_blkPostTitle\s+global_ptitle(?:\s+blkStrong)?")

        existing_data, existing_titles = read_file(excel_path)
        driver = get_configured_driver()
        
        start_parsing_time = time.time()

        for page in tqdm(range(page, limit + 1), desc="Parsing detector_media_rinok"):
            if parsing_completed:
                break  # Выход из цикла если парсинг завершен

            url = f"https://detector.media/category/rinok/pagenum/{page}/"
            driver.get(url)
            
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "cat_blkList")))

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            if not soup.title or soup.title.text == "Just a moment...":
                print("Сайт блокує парсинг")
                break
            
            elements = soup.find("div", class_="cat_blkList").findAll(class_=pattern)
            for e in elements:
                title = e.find(class_=pattern2).text.strip()
                if title not in existing_titles:
                    temp_date = e.find(class_="cat_blkPostDate global_pdate").text.split()[0].split(".")
                    temp_date[1] = months.get(temp_date[1])
                    date = " ".join(temp_date)
                    data.append({
                        "site": "detector.media/category/rinok",
                        "date": date,
                        "title": title,
                        "link": e.find(class_=pattern2).a.get("href"),
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
    detector_media_rinok_parser()
