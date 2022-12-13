import string
from dataclasses import dataclass
from pickle import dump
import requests
from bs4 import BeautifulSoup
all_elements = []
n = 20
for id_ in range(1, 201):  # range(1, 2057):
    url = f"https://web.usos.agh.edu.pl/kontroler.php?_action=katalog2/jednostki/pokazSale&sala_id={id_}&plan_showSettings=1&plan_showStartTime=1&plan_showEndTime=1&plan_showTypeShort=1&plan_showTypeFull=1&plan_showGroupNumber=1&plan_showCourseName=1&plan_showCourseCode=1&plan_showRoom=1&plan_showBuildingCode=1&plan_showLecturers=1&plan_overridePrintWidth=1&plan_format=html&plan_colorScheme=default"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    elements = soup.find_all("div", class_="autoscroll")
    if len(elements) > 0:
        tabele_elements = elements[0].findAll(lambda tag: tag.name == 'tr')

        for elem in tabele_elements:
            if "," in elem.text:
                elems = elem.findAll(lambda tag: tag.name == 'td')
                for el in elems:
                    elements_3 = el.findAll(lambda tag: tag.name == 'div')
                    elements_4 = el.findAll(lambda tag: tag.name == 'span')
                    for el3, el4 in zip(elements_3, elements_4):
                        if ',' in el3.text:
                            all_elements.append((el3.text, el4.text))

    print(id_, "/", 2057)
    if id_ % 100 == 0:
        with open(f"all_classes_{n}.bin", "wb") as file:
            dump(all_elements, file)
        n += 1
        all_elements = []

with open(f"all_classes_{n}.bin", "wb") as file:
    dump(all_elements, file)

print(*all_elements)






