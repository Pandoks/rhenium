import re
from playwright.sync_api import sync_playwright


def get(url):
    print(f"---------- Getting {url} ----------")

    with sync_playwright() as playwright:
        chromium = playwright.chromium
        browser = chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state("domcontentloaded")

        isListing = False
        status = page.query_selector(
            "span.Text-c11n-8-99-3__sc-aiai24-0.dpf__sc-1yftt2a-1.dFxMdJ.ixkFNb"
        )
        if not status:
            isListing = True
            status = page.query_selector(
                "span.Text-c11n-8-100-2__sc-aiai24-0.HomeStatusIconAndText__StyledStatusText-fshdp-8-100-2__sc-1yftt2a-1.bSfDch.ijIdQj"
            )
        if not status:
            raise Exception(f"Couldn't figure out the status of the listing '{url}'")
        else:
            status = status.inner_text()
        print("status:", status)

        price = None
        price_element = page.query_selector('span[data-testid="price"]')
        if price_element:
            price = price_element.inner_text().replace("$", "").replace(",", "")
        print("price:", price)

        address = None
        city = None
        state = None
        zip = None
        address_element = page.query_selector(
            "h1.Text-c11n-8-100-2__sc-aiai24-0.bSfDch"
        )
        if address_element:
            address_element_text = address_element.inner_text().split(",")
            address = address_element_text[0]
            city = re.sub(r"[^a-zA-Z]", "", address_element_text[1])
            state = address_element_text[2].split(" ")[1]
            zip = address_element_text[2].split(" ")[2]
        print("address:", address)
        print("city:", city)
        print("state:", state)
        print("zip:", zip)

        price_history_table_element = None
        if isListing:
            price_history_table_element = page.query_selector(
                "table.StyledTableComponents__StyledTable-fshdp-8-100-2__sc-shu7eb-2.jaWGxh"
            )
        else:
            price_history_table_element = page.query_selector(
                "table.StyledTableComponents__StyledTable-sc-f00yqe-2 kNXiqz"
            )
        if price_history_table_element:
            price_history_table_element = price_history_table_element.query_selector(
                "tbody"
            )
        price_history = []
        if price_history_table_element:
            price_history_rows = price_history_table_element.query_selector_all(
                "tr[id]"
            )
            for price_rows in price_history_rows:
                price_history_columns = price_rows.query_selector_all("td")
                price_date = (
                    price_history_columns[0].query_selector("span").inner_text()
                )
                price_event = (
                    price_history_columns[1].query_selector("span").inner_text()
                )
                price_price = (
                    price_history_columns[2]
                    .query_selector("span")
                    .query_selector("span")
                    .inner_text()
                    .replace("$", "")
                    .replace(",", "")
                )
                price_history.append([price_date, price_event, price_price])

        print(price_history)

        browser.close()

    # print(price_history_element)


get("https://www.zillow.com/homedetails/19615387_zpid/")
