import requests
import re
from bs4 import BeautifulSoup as soup


# TODO: use selenium
def get(url):
    header = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "referer": "https://www.zillow.com/homes",
    }
    html = requests.get(url=url, headers=header)
    if html.status_code != 200:
        raise Exception(f"Couldn't successfully retrieve '{url}'")

    soup_object = soup(html.content, "lxml")
    print(soup_object)

    inactive_status = soup_object.find(
        "span",
        {"class": "Text-c11n-8-99-3__sc-aiai24-0 dpf__sc-1yftt2a-1 dFxMdJ ixkFNb"},
    )
    active_status = soup_object.find(
        "span",
        {
            "class": "Text-c11n-8-100-2__sc-aiai24-0 HomeStatusIconAndText__StyledStatusText-fshdp-8-100-2__sc-1yftt2a-1 bSfDch ijIdQj"
        },
    )
    status = inactive_status
    isListing = False
    if not status:
        status = active_status
    if status:
        status = status.text.strip()
        isListing = True

    price_element = soup_object.find("span", {"data-testid": "price"})
    if not price_element or not hasattr(price_element.find("span"), "text"):
        # TODO: just make price None
        raise Exception(f"Couldn't find the price of '{url}'")
    # errors are handled for null case already
    price_text = price_element.find("span").text.strip()
    price = int(price_text.replace("$", "").replace(",", ""))

    address_element = soup_object.find(
        "h1", {"class": "Text-c11n-8-100-2__sc-aiai24-0 bSfDch"}
    )
    if not address_element or not hasattr(address_element, "text"):
        raise Exception(f"Couldn't find the address of '${url}'")
    address_text = address_element.text.strip().split(",")
    address = address_text[0]
    city = re.sub(r"[^a-zA-Z]", "", address_text[1])
    state = address_text[2].split(" ")[1]
    zip = address_text[2].split(" ")[2]
    # print(address, city, state, zip)

    price_history = None
    if isListing:
        price_history = soup_object.find(
            "table", {"class": "StyledTableComponents__StyledTable-sc-f00yqe-2 kNXiqz"}
        )
        # print(price_history)
    else:
        price_history = soup_object.find(
            "table",
            {
                "class": "StyledTableComponents__StyledTable-fshdp-8-100-2__sc-shu7eb-2 jaWGxh"
            },
        )
        # print(price_history)
    if price_history:
        price_history = []
        for row in price_history.find_all("tr"):
            # date, event, price
            row_data = []
            for col in row.find_all("td"):
                col_data = col.find("span")
                if not col_data.find("span"):
                    row_data.append(col_data.text.strip())
                else:
                    row_data.append(col_data.find("span").text.strip())
            price_history.append(row_data)
        # print(price_history)


# get("https://www.zillow.com/homedetails/19615387_zpid/")
get(
    "https://www.zillow.com/homedetails/1641-Albatross-Dr-Sunnyvale-CA-94087/19615387_zpid/"
)
