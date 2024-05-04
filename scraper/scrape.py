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
        print(address_element)
        print("address:", address)
        print("city:", city)
        print("state:", state)
        print("zip:", zip)

        # price_history_table_element = None
        # if isListing:
        #     price_history_table_element = page.query_selector(
        #         "table.StyledTableComponents__StyledTable-fshdp-8-100-2__sc-shu7eb-2.jaWGxh"
        #     )
        # else:
        #     price_history_table_element = page.query_selector(
        #         "table.StyledTableComponents__StyledTable-sc-f00yqe-2 kNXiqz"
        #     )
        # price_history_table_element = page.query_selector(
        #     "table.StyledTableComponents__StyledTable-fshdp-8-100-2__sc-shu7eb-2.jaWGxh"
        # )
        # print(price_history_table_element)

        browser.close()

    # print(price_history_element)


get("https://www.zillow.com/homedetails/19615387_zpid/")
