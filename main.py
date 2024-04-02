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
    the_drum_digital_parser,
    the_drum_media_parser,
    the_drum_marketing_parser,
    warc_parser,
    insiderintelligence_parser,
    campaignlive_parser,
    strategyonline_parser,
)


def run_parser(parser_function):
    print(f"\n\033[92mParsing {parser_function.__name__}\033[0m")
    parser_function()



def main():
    start_processing = time.time()

    # mmr_news з підвищеним захистом від cloudflare, тому з ним постійні проблеми
    parsers = [
        mmr_news_parser.mmr_news_parser,
        mmr_digital_parser.mmr_digital_parser,
        mmr_social_parser.mmr_social_parser,
        detector_media_news_parser.detector_media_news_parser,
        detector_media_rinok_parser.detector_media_rinok_parser,
        detector_media_internet_parser.detector_media_internet_parser,
        gradus_app_parser.gradus_app_parser,
        mix_digital_news_parser_ru.mix_digital_news_parser_ru,
        mix_digital_news_parser_ua.mix_digital_news_parser_ua,
        mix_digital_cases_parser_ru.mix_digital_cases_parser_ru,
        mix_digital_cases_parser_ua.mix_digital_cases_parser_ua,
        blog_uamaster_imarketing.blog_uamaster_imarketing,
        blog_uamaster_analytics.blog_uamaster_analytics,
        the_drum_digital_parser.the_drum_digital_parser,
        the_drum_media_parser.the_drum_media_parser,
        the_drum_marketing_parser.the_drum_marketing_parser,
        warc_parser.warc_parser,
        insiderintelligence_parser.insiderintelligence_parser,
        campaignlive_parser.campaignlive_parser,
        strategyonline_parser.strategyonline_parser,
    ]

    # Ліміт одночасно працюючих парсерів
    max_workers = 3 # Чим більше значення, тим більше ресурсів компа їсть
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(run_parser, parsers)

    end_processing = time.time()
    time_processing = round((end_processing - start_processing)/60, 2)
    print(f"\nЗагальний час парсингу {time_processing} хв")

if __name__ == "__main__":
    main()
