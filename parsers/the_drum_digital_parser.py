import time
from bs4 import BeautifulSoup
from tqdm import tqdm
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.utils import process_data, read_file, load_dict_from_file
from utils.webdriver_config import get_configured_driver


def the_drum_digital_parser():
    try:
        months_file_name = 'months.txt'
        months = load_dict_from_file(months_file_name)
        
        excel_path = "parsed_data/the_drum_digital.xlsx"        
        data = []
        top_elements_data = set()
        page = 1
        limit = 10
        parsing_completed = False

        existing_data, existing_titles = read_file(excel_path)
        driver = get_configured_driver()
        
        start_parsing_time = time.time()

        # for page in tqdm(range(page, limit + 1), desc="Parsing the_drum_digital_parser"):
        for page in range(page, limit+1):
            if parsing_completed:
                break  # Выход из цикла если парсинг завершен
            
            url = f"https://www.thedrum.com/digital/{page}#more-articles"
            driver.get(url)
            
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "hub__articles-data")))
            except:
                break
                
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            if not soup.title or soup.title.text == "Just a moment...":
                print("Сайт блокує парсинг")
                break

            # Загальні новини по тематиці, які не змінюються зі сторінками
            top_elements = soup.find(class_="hub__articles-grid hub__articles-grid--four").findAll(class_="hub__articles-data")
            for e in top_elements:
                title = e.find(class_="hub-article__info-title").text
                if title not in existing_titles and title not in top_elements_data:
                    link = "https://www.thedrum.com" + e.find(class_="hub-article__info-title").get("href")
                    driver.get(link)
                    top_elements_html = driver.page_source
                    top_elements_soup = BeautifulSoup(top_elements_html, "html.parser")

                    top_elements_soup.find(class_="article__font article__header__author__time")

                    temp_date = top_elements_soup.find(class_="article__font article__header__author__time").text.split("|")[0].strip().replace(",", "").split()
                    temp_date[0] = months.get(temp_date[0].lower())
                    temp_date[0], temp_date[1] = temp_date[1], temp_date[0]
                    date = " ".join(temp_date)
                    top_elements_data.add(title)
                    data.append({
                        "site": "thedrum.com/digital",
                        "date": date,
                        "title": title,
                        "link": link,
                    })
                

            elements = soup.find(class_="hub__articles hub__articles--more").findAll(class_="hub__articles-data")
            for e in elements:
                title = e.find(class_="hub-article__info-title").text
                if title not in existing_titles:
                    link = "https://www.thedrum.com" + e.find(class_="hub-article__info-title").get("href")
                    temp_date = e.find(class_="hub-article__info-time--release").text.split()
                    # В новинах що вишли недавно замість дати пишеться по типу 3 days ago, тому треба заходити всередину цих статтей 
                    if "days" in temp_date or "day" in temp_date:
                        driver.get(link)
                        temp_elements_html = driver.page_source
                        temp_elements_soup = BeautifulSoup(temp_elements_html, "html.parser")
                        temp_date = temp_elements_soup.find(class_="article__font article__header__author__time").text.split("|")[0].strip().replace(",", "").split()
                        temp_date[0] = months.get(temp_date[0].lower())
                        temp_date[0], temp_date[1] = temp_date[1], temp_date[0]
                        date = " ".join(temp_date)
                    else:
                        temp_date[1] = months.get(temp_date[1].lower())
                        date = " ".join(temp_date)

                    data.append({
                        "site": "thedrum.com/marketing",
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
    the_drum_digital_parser()