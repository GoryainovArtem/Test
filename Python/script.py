import logging
import csv
import os

import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def convert_json_response_to_csv(response):
    """
        Конвертировать JSON формат в CSV.
    """

    logger.info("Обработка HTTP response")
    with open("file.csv", "w", encoding="utf-8", newline="") as output_file:
        logger.info("Был создан file.csv")
        writer = csv.writer(output_file)
        writer.writerow(("Страна", "Населенный пункт", "Название станции", "Направление", "Код яндекса",
                         "Тип станции", "Тип транспорта", "Долгота", "Широта"
                         )
                        )
        writer.writerow(("country_nm", "settlement_nm", "station_nm", "direction", "yandex_cd",
                         "station_type", "transport_type", "long", "lat"
                         )
                        )
        for country in response.get("countries"):
            country_nm = country.get('title', "")
            regions = country.get("regions")
            if regions:
                for region in regions:
                    settlements = region.get("settlements")
                    if settlements:
                        for settlement in settlements:
                            settlement_nm = settlement.get("title", "")
                            stations = settlement.get("stations")
                            if stations:
                                for station in stations:
                                    station_nm = station.get("title", "")
                                    direction = station.get("direction", "")
                                    yandex_cd = station.get("codes").get("yandex_code", "")
                                    station_type = station.get("station_type", "")
                                    transport_type = station.get("transport_type", "")
                                    long = station.get("longitude", "")
                                    lat = station.get("latitude", "")
                                    writer.writerow((country_nm, settlement_nm, station_nm, direction, yandex_cd, station_type,
                                                     transport_type, long, lat
                                                     )
                                                    )
                            else:
                                logger.info(f"У населенного пункта {settlement} нет станций")
                    else:
                        logger.info(f"У региона {region} нет населенных пунктов")
            else:
                logger.info(f"У страны {country} нет регионов")


def get_available_stations():
    """
        Выполнить GET запрос к API Яндекс Расписаний и сохранить результат в CSV файл.
    """

    logger.info("Начало выполнения программы")
    api_key = os.getenv("yandex_station_api_key")
    url = f"https://api.rasp.yandex.net/v3.0/stations_list/?apikey={api_key}&lang=ru_RU&format=json"
    try:
        response = requests.get(url)
        logger.info("HTTP response был успешно получен.")
        convert_json_response_to_csv(response.json())
    except:
        logger.error("Ошибка. HTTP response не был получен.")
    logger.info("Окончание выполнения программы")


if __name__ == "__main__":
    get_available_stations()
