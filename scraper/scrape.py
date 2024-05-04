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
        price_history_element = page.locator('h2:text-is("Price history")').locator(
            "xpath=.."
        )
        button = price_history_element.locator('span:text-is("Show more")').locator(
            "xpath=.."
        )
        if button.count() > 0:
            button.click()

        tax_history_element = page.locator('h2:text-is("Public tax history")').locator(
            "xpath=.."
        )
        button = tax_history_element.locator('span:text-is("Show more")').locator(
            "xpath=.."
        )
        if button.count() > 0:
            button.click()

        facts_element = page.locator('h4:text-is("Facts and features")').locator(
            "xpath=.."
        )
        if not facts_element.count():
            facts_element = page.locator('h2:text-is("Facts & features")').locator(
                "xpath=.."
            )
        button = facts_element.locator(
            'span:text-is("See more facts and features")'
        ).locator("xpath=..")
        if not button.count():
            button = facts_element.locator('span:text-is("Show more")')
        if button.count() > 0:
            button.click()
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

        # price = None
        # price_element = page.query_selector('span[data-testid="price"]')
        # if price_element:
        #     price = price_element.inner_text().replace("$", "").replace(",", "")
        # print("price:", price)

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

        price_history = []
        for price_rows in (
            price_history_element.locator("tbody").locator("tr[id]").element_handles()
        ):
            price_columns = price_rows.query_selector_all("td")
            price_date = price_columns[0].query_selector("span").inner_text()
            price_event = price_columns[1].query_selector("span").inner_text()
            price_price = (
                price_columns[2]
                .query_selector("span")
                .query_selector("span")
                .inner_text()
                .replace("$", "")
                .replace(",", "")
            )
            price_history.append([price_date, price_event, price_price])
        print("price history:", price_history)

        tax_history = []
        for tax_rows in (
            tax_history_element.locator("tbody").locator("tr[id]").element_handles()
        ):
            tax_columns = tax_rows.query_selector_all("td")
            tax_year = tax_columns[0].query_selector("span").inner_text()
            property_taxes = (
                tax_columns[1]
                .query_selector("span")
                .inner_text()
                .replace("$", "")
                .replace(",", "")
                .split(" ")[0]
            )
            if property_taxes == "--":
                property_taxes = None
            tax_assessment = (
                tax_columns[2]
                .query_selector("span")
                .inner_text()
                .replace("$", "")
                .replace(",", "")
                .split(" ")[0]
            )
            tax_history.append([tax_year, property_taxes, tax_assessment])
        print("tax history:", tax_history)

        fact_locators = {
            "bedrooms": 'span:has-text("Bedrooms")',
            "bathrooms": 'span:text-matches("Bathrooms")',
            "full_bathrooms": 'span:has-text("Full bathrooms")',
            "three_fourths_bathrooms": 'span:has-text("3/4 bathrooms")',
            "half_bathrooms": 'span:has-text("1/2 bathrooms")',
            "one_fourths_bathrooms": 'span:has-text("1/4 bathrooms")',
            "year_built": 'span:has-text("Year built")',
            "lot_size": 'span:has-text("Lot size")',
            "home_type": 'span:has-text("Home type")',
            "stories": 'span:has-text("Stories")',
            "size": 'span:has-text("interior livable area")',
            "parking": 'span:has-text("parking features")',
            "parking_spaces": 'span:has-text("total spaces")',
            "garage_spaces": 'span:has-text("garage spaces")',
            "covered_spaces": 'span:has-text("covered spaces")',
            "hoa": 'span:has-text("has HOA")',
            "hoa_fee": 'span:has-text("HOA fee")',
        }
        fact_info = {}
        for key, fact_locator in fact_locators.items():
            element = facts_element.locator(fact_locator)
            if not element.count():
                fact_info[key] = None
                continue

            element_text = element.inner_text().split(": ")[1]

            if element_text == "Yes":
                fact_info[key] = True
                continue
            elif element_text == "No":
                fact_info[key] = False
                continue

            if re.search(r"\d", element_text):
                fact_info[key] = element_text.replace(",", "").replace("$", "")
                continue
            elif element_text.find(", ") != -1:
                element_split_text = element_text.split(", ")
                fact_info[key] = element_split_text
                continue

            fact_info[key] = element_text
        print(fact_info)

        browser.close()

    # print(price_history_element)


get("https://www.zillow.com/homedetails/19615387_zpid/")
# get(
#     "https://www.zillow.com/homedetails/875-Cotati-Trl-5-Sunnyvale-CA-94085/300481656_zpid/"
# )
