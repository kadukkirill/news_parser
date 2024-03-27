import time
import concurrent.futures
from parsers import (
    mmr_news_parser,
    mmr_digital_parser,
    mmr_social_parser,
    detector_media_news_parser,
    detector_media_rinok_parser,
    detector_media_internet_parser,
    gradus_app_parser,
    mix_digital_news_parser_ru,
    mix_digital_news_parser_ua,
    mix_digital_cases_parser_ru,
    mix_digital_cases_parser_ua,
    blog_uamaster_imarketing,
    blog_uamaster_analytics,
)


def run_parser(parser_function):
    try:
        parser_function()
        # print(f"Parser {parser_function.__name__} completed successfully")
    except Exception as e:
        print(f"Error in parser {parser_function.__name__}: {e}")


def main():
    start_processing = time.time()

    parsers = [
        # mmr_news_parser.mmr_news_parser,
        # mmr_digital_parser.mmr_digital_parser,
        # mmr_social_parser.mmr_social_parser,
        # detector_media_news_parser.detector_media_news_parser,
        # detector_media_rinok_parser.detector_media_rinok_parser,
        # detector_media_internet_parser.detector_media_internet_parser,
        # gradus_app_parser.gradus_app_parser,
        # mix_digital_news_parser_ru.mix_digital_news_parser_ru,
        # mix_digital_news_parser_ua.mix_digital_news_parser_ua,
        # mix_digital_cases_parser_ru.mix_digital_cases_parser_ru,
        # mix_digital_cases_parser_ua.mix_digital_cases_parser_ua,
        blog_uamaster_imarketing.blog_uamaster_imarketing,
        # blog_uamaster_analytics.blog_uamaster_analytics,
    
    ]

    # Ограничение числа одновременно выполняемых парсеров
    max_workers = 5  # Можно подстроить в зависимости от доступных ресурсов
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(run_parser, parsers)

    end_processing = time.time()
    time_processing = round((end_processing - start_processing)/60, 2)
    print(f"\nЗагальний час парсингу {time_processing} хв")

if __name__ == "__main__":
    main()