import os
import pickle
import random
import re
import queue
import pprint
import psycopg2
import threading
import argparse
import concurrent.futures
import asyncio
import asyncpg
import aiofiles
import datetime
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright


load_dotenv()
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_DATABASE = os.getenv("DB_DATABASE")
CONNECTION_STRING = os.getenv("CONNECTION_STRING")

# write_lock = threading.Lock()
write_lock = asyncio.Lock()


async def store_data(start, end, failed):
    async with write_lock:
        async with aiofiles.open("cursor", "wb") as data_file:
            data = {"start": start, "end": end, "failed": failed}
            await data_file.write(pickle.dumps(data))


async def load_data():
    async with aiofiles.open("cursor", "rb") as data_file:
        data = await data_file.read()
        if not data:
            raise ValueError("No cursor file or no data in cursor file")
        print(pickle.loads(data))
        return pickle.loads(data)


async def insert_database(property, db):
    # cursor = db.cursor()
    async with db.acquire() as conn:
        async with conn.transaction():
            # insert_property_query = """
            # INSERT INTO properties (
            #     address,
            #     city,
            #     zip,
            #     state,
            #     status,
            #     price,
            #     bathrooms,
            #     full_bathrooms,
            #     half_bathrooms,
            #     three_fourths_bathrooms,
            #     one_fourths_bathrooms,
            #     stories,
            #     bedrooms,
            #     parcel_number,
            #     year_built,
            #     zoning,
            #     lot_size,
            #     structure_size,
            #     interior_living_size,
            #     parking_spaces,
            #     garage_spaces,
            #     covered_spaces,
            #     fireplace_count,
            #     home_type,
            #     architectural_style,
            #     basement,
            #     hoa,
            #     hoa_fee,
            #     laundry,
            #     foundation,
            #     senior_community,
            #     property_condition
            # ) VALUES (
            #     %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            #     %s, %s, %s, %s, %s, %s, %s, %s, %s
            # ) ON CONFLICT DO NOTHING
            # """
            # insert_price_history_query = """
            # INSERT INTO price_history (
            #     date,
            #     event,
            #     price,
            #     address,
            #     city,
            #     zip,
            #     state
            # ) VALUES (
            #     %s, %s, %s, %s, %s, %s, %s
            # ) ON CONFLICT DO NOTHING
            # """
            # insert_tax_history_query = """
            # INSERT INTO tax_history (
            #     year,
            #     assessment,
            #     tax,
            #     address,
            #     city,
            #     zip,
            #     state
            # ) VALUES (
            #     %s, %s, %s, %s, %s, %s, %s
            # ) ON CONFLICT DO NOTHING
            # """
            # insert_detail_query_template = """
            # INSERT INTO {table} (
            #     {column},
            #     address,
            #     city,
            #     zip,
            #     state
            # ) VALUES (
            #     %s, %s, %s, %s, %s
            # ) ON CONFLICT DO NOTHING
            # """
            insert_property_query = """
            INSERT INTO properties (
                address, 
                city, 
                zip, 
                state, 
                status, 
                price, 
                bathrooms, 
                full_bathrooms, 
                half_bathrooms, 
                three_fourths_bathrooms,
                one_fourths_bathrooms,
                stories,
                bedrooms,
                parcel_number,
                year_built,
                zoning,
                lot_size,
                structure_size,
                interior_living_size,
                parking_spaces,
                garage_spaces,
                covered_spaces,
                fireplace_count,
                home_type,
                architectural_style,
                basement,
                hoa,
                hoa_fee,
                laundry,
                foundation,
                senior_community,
                property_condition
            ) VALUES (
                $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, 
                $20, $21, $22, $23, $24, $25, $26, $27, $28, $29, $30, $31, $32
            ) ON CONFLICT DO NOTHING
            """
            insert_price_history_query = """
            INSERT INTO price_history (
                date,
                event,
                price,
                address,
                city,
                zip,
                state
            ) VALUES (
                $1, $2, $3, $4, $5, $6, $7
            ) ON CONFLICT DO NOTHING
            """
            insert_tax_history_query = """
            INSERT INTO tax_history (
                year,
                assessment,
                tax,
                address,
                city,
                zip,
                state
            ) VALUES (
                $1, $2, $3, $4, $5, $6, $7
            ) ON CONFLICT DO NOTHING
            """
            insert_detail_query_template = """
            INSERT INTO {table} (
                {column},
                address,
                city,
                zip,
                state
            ) VALUES (
                $1, $2, $3, $4, $5
            ) ON CONFLICT DO NOTHING
            """
            address = property["address"]
            city = property["city"]
            zip = property["zip"]
            state = property["state"]
            details = property["details"]
            price_history = property["price_history"]
            tax_history = property["tax_history"]
            property_data = (
                address,
                city,
                zip,
                state,
                property["status"],
                property["price"],
                details["bathrooms"],
                details["full_bathrooms"],
                details["half_bathrooms"],
                details["three_fourths_bathrooms"],
                details["one_fourths_bathrooms"],
                details["stories"],
                details["bedrooms"],
                details["parcel_number"],
                details["year_built"],
                details["zoning"],
                details["lot_size"],
                details["structure_size"],
                details["interior_living_size"],
                details["parking_spaces"],
                details["garage_spaces"],
                details["covered_spaces"],
                details["fireplace_count"],
                details["home_type"],
                details["architectural_style"],
                details["basement"],
                details["hoa"],
                details["hoa_fee"],
                details["laundry"],
                details["foundation"],
                details["senior_community"],
                details["property_condition"],
            )

            # cursor.execute(insert_property_query, property_data)
            cast = lambda value, type_conversion: (
                type_conversion(value) if value is not None else None
            )
            await conn.execute(
                insert_property_query,
                cast(address, str),
                cast(city, str),
                cast(zip, str),
                cast(state, str),
                cast(property["status"], str),
                cast(property["price"], str),
                cast(details["bathrooms"], float),
                cast(details["full_bathrooms"], int),
                cast(details["half_bathrooms"], int),
                cast(details["three_fourths_bathrooms"], int),
                cast(details["one_fourths_bathrooms"], int),
                cast(details["stories"], int),
                cast(details["bedrooms"], int),
                cast(details["parcel_number"], int),
                cast(details["year_built"], str),
                cast(details["zoning"], str),
                cast(details["lot_size"], str),
                cast(details["structure_size"], str),
                cast(details["interior_living_size"], str),
                cast(details["parking_spaces"], int),
                cast(details["garage_spaces"], int),
                cast(details["covered_spaces"], int),
                cast(details["fireplace_count"], int),
                cast(details["home_type"], str),
                cast(details["architectural_style"], str),
                cast(details["basement"], bool),
                cast(details["hoa"], bool),
                cast(details["hoa_fee"], str),
                cast(details["laundry"], str),
                cast(details["foundation"], str),
                cast(details["senior_community"], bool),
                cast(details["property_condition"], str),
            )

            for price in price_history:
                date = price["date"]
                date_components = date.split("/")
                price_data = (
                    f"{date_components[2]}-{date_components[0]}-{date_components[1]}",
                    price["event"],
                    price["price"],
                    address,
                    city,
                    zip,
                    state,
                )
                # cursor.execute(insert_price_history_query, price_data)
                await conn.execute(
                    insert_price_history_query,
                    datetime.date(
                        int(date_components[2]),
                        int(date_components[0]),
                        int(date_components[1]),
                    ),
                    cast(price["event"], str),
                    cast(price["price"], str),
                    cast(address, str),
                    cast(city, str),
                    cast(zip, str),
                    cast(state, str),
                )
            for tax in tax_history:
                tax_data = (
                    tax["year"],
                    tax["assessment"],
                    tax["taxes"],
                    address,
                    city,
                    zip,
                    state,
                )
                # cursor.execute(insert_tax_history_query, tax_data)
                await conn.execute(
                    insert_tax_history_query,
                    cast(tax["year"], str),
                    cast(tax["assessment"], str),
                    cast(tax["taxes"], str),
                    cast(address, str),
                    cast(city, str),
                    cast(zip, str),
                    cast(state, str),
                )
            details_table = {
                "accessibility_features": "feature",
                "additional_structures": "structure",
                "amenities": "amenity",
                "bathroom_features": "feature",
                "bedroom_features": "feature",
                "construction_materials": "material",
                "cooling": "type",
                "dining_features": "feature",
                "exterior_features": "feature",
                "family_features": "feature",
                "fencing": "type",
                "fireplace_features": "feature",
                "flooring": "type",
                "gas": "type",
                "heating": "type",
                "included_appliances": "appliance",
                "interior_features": "feature",
                "kitchen_features": "feature",
                "lot_features": "feature",
                "parking": "type",
                "patio_porch_details": "detail",
                "pool_features": "feature",
                "property_subtype": "type",
                "roof": "type",
                "services": "service",
                "sewer": "type",
                "spa_features": "feature",
                "utilities": "utility",
                "view_description": "description",
            }
            for table, column in details_table.items():
                features = details[table]
                if not features:
                    continue
                insert_table_query = insert_detail_query_template.format(
                    table=table, column=column
                )
                if isinstance(features, (list, tuple)):
                    for feature in features:
                        details_data = (feature, address, city, zip, state)
                        # cursor.execute(insert_table_query, details_data)
                        await conn.execute(
                            insert_table_query,
                            cast(feature, str),
                            cast(address, str),
                            cast(city, str),
                            cast(zip, str),
                            cast(state, str),
                        )
                else:
                    details_data = (details[table], address, city, zip, state)
                    # cursor.execute(insert_table_query, details_data)
                    await conn.execute(
                        insert_table_query,
                        cast(details[table], str),
                        cast(address, str),
                        cast(city, str),
                        cast(zip, str),
                        cast(state, str),
                    )

            # db.commit()
            # cursor.close()


async def get_zillow(url, failed, db, semaphore, end):
    async with semaphore:
        async with async_playwright() as playwright:
            # with sync_playwright() as playwright:
            browsers = [playwright.chromium, playwright.firefox, playwright.webkit]
            open_browser = await random.choice(browsers).launch(headless=False)
            try:
                print(f"---------- Getting {url} ----------")

                property_info = {}

                page = await open_browser.new_page()
                await page.goto(url)

                await page.wait_for_load_state("domcontentloaded")
                price_history_element = page.locator(
                    'h2:text-is("Price history")'
                ).locator("xpath=..")
                if not await price_history_element.count():
                    price_history_element = page.locator(
                        'h5:text-is("Price history")'
                    ).locator("xpath=..")
                button = price_history_element.locator(
                    'span:text-is("Show more")'
                ).locator("xpath=..")
                if await button.count() > 0:
                    await button.click()

                tax_history_element = page.locator(
                    'h2:text-is("Public tax history")'
                ).locator("xpath=..")
                if not await tax_history_element.count():
                    tax_history_element = page.locator(
                        'h5:text-is("Public tax history")'
                    ).locator("xpath=..")
                button = tax_history_element.locator(
                    'span:text-is("Show more")'
                ).locator("xpath=..")
                if await button.count() > 0:
                    await button.click()

                facts_element = page.locator(
                    'h4:text-is("Facts and features")'
                ).locator("xpath=..")
                if not await facts_element.count():
                    facts_element = page.locator(
                        'h2:text-is("Facts & features")'
                    ).locator("xpath=..")
                button = facts_element.locator(
                    'span:text-is("See more facts and features")'
                ).locator("xpath=..")
                if not await button.count():
                    button = facts_element.locator('span:text-is("Show more")')
                if await button.count() > 0:
                    await button.click()
                await page.wait_for_load_state("domcontentloaded")

                isListing = False
                status = await page.query_selector(
                    "span.Text-c11n-8-99-3__sc-aiai24-0.dpf__sc-1yftt2a-1.dFxMdJ.ixkFNb"
                )
                if not status:
                    isListing = True
                    status = await page.query_selector(
                        "span.Text-c11n-8-100-2__sc-aiai24-0.HomeStatusIconAndText__StyledStatusText-fshdp-8-100-2__sc-1yftt2a-1.bSfDch.ijIdQj"
                    )
                if not status:
                    raise Exception(
                        f"Couldn't figure out the status of the listing '{url}'"
                    )
                else:
                    status = await status.inner_text()
                property_info["status"] = status

                price = None
                price_element = await page.query_selector('span[data-testid="price"]')
                if price_element:
                    price = (
                        (await price_element.inner_text())
                        .replace("$", "")
                        .replace(",", "")
                    )
                property_info["price"] = price

                address = None
                city = None
                state = None
                zip = None
                address_element = await page.query_selector(
                    "h1.Text-c11n-8-100-2__sc-aiai24-0.bSfDch"
                )
                if not address_element:
                    address_element = await page.query_selector(
                        "h1.Text-c11n-8-99-3__sc-aiai24-0.dFxMdJ"
                    )
                if address_element:
                    address_element_text = (await address_element.inner_text()).split(
                        ","
                    )
                    address = address_element_text[0]
                    city = re.sub(r"[^a-zA-Z]", "", address_element_text[1])
                    state = address_element_text[2].split(" ")[1]
                    zip = address_element_text[2].split(" ")[2]
                property_info["address"] = address
                property_info["city"] = city
                property_info["state"] = state
                property_info["zip"] = zip

                price_history = []
                for price_rows in (
                    await price_history_element.locator("tbody")
                    .locator("tr[id]")
                    .element_handles()
                ):
                    price_columns = await price_rows.query_selector_all("td")
                    price_date = (
                        await price_columns[0].query_selector("span")
                    ).inner_text()
                    price_event = (
                        await price_columns[1].query_selector("span")
                    ).inner_text()
                    price_price = (
                        (
                            await (
                                await (
                                    await price_columns[2].query_selector("span")
                                ).query_selector("span")
                            ).inner_text()
                        )
                        .replace("$", "")
                        .replace(",", "")
                    )
                    price_history.append(
                        {
                            "date": await price_date,
                            "event": await price_event,
                            "price": price_price,
                        }
                    )
                property_info["price_history"] = price_history

                tax_history = []
                for tax_rows in (
                    await tax_history_element.locator("tbody")
                    .locator("tr")
                    .element_handles()
                ):
                    tax_columns = []
                    if not isListing:
                        tax_columns.append(await tax_rows.query_selector("th"))
                    tax_columns.extend(await tax_rows.query_selector_all("td"))
                    tax_year = await tax_columns[0].inner_text()
                    property_taxes = (
                        (
                            await (
                                await tax_columns[1].query_selector("span")
                            ).inner_text()
                        )
                        .replace("$", "")
                        .replace(",", "")
                        .split(" ")[0]
                    )
                    if property_taxes == "--":
                        property_taxes = None
                    tax_assessment = (
                        (
                            await (
                                await tax_columns[2].query_selector("span")
                            ).inner_text()
                        )
                        .replace("$", "")
                        .replace(",", "")
                        .split(" ")[0]
                    )
                    tax_history.append(
                        {
                            "year": tax_year,
                            "taxes": property_taxes,
                            "assessment": tax_assessment,
                        }
                    )
                property_info["tax_history"] = tax_history

                # dict = { "feature": [[list of locators], [list of locators]] }
                fact_locators = {
                    "bedrooms": [['span:has-text("Bedrooms")']],
                    "bathrooms": [['span:text-matches("Bathrooms")']],
                    "full_bathrooms": [['span:has-text("Full bathrooms")']],
                    "three_fourths_bathrooms": [['span:has-text("3/4 bathrooms")']],
                    "half_bathrooms": [['span:has-text("1/2 bathrooms")']],
                    "one_fourths_bathrooms": [['span:has-text("1/4 bathrooms")']],
                    "year_built": [['span:text-matches("Year built: ")']],
                    "lot_size": [['span:has-text("Lot size:")']],
                    "lot_features": [['span:has-text("Lot features")']],
                    "home_type": [['span:has-text("Home type")']],
                    "architectural_style": [['span:has-text("Architectural style")']],
                    "property_subtype": [['span:has-text("Property subType")']],
                    "foundation": [['span:has-text("Foundation")']],
                    "roof": [['span:has-text("Roof")']],
                    "property_condition": [['span:has-text("Property condition")']],
                    "stories": [['span:has-text("Stories")']],
                    "interior_living_size": [
                        ['span:has-text("interior livable area")']
                    ],
                    "structure_size": [['span:has-text("structure area")']],
                    "parking": [['span:has-text("parking features")']],
                    "parking_spaces": [['span:has-text("total spaces")']],
                    "garage_spaces": [['span:has-text("garage spaces")']],
                    "covered_spaces": [['span:has-text("covered spaces")']],
                    "hoa": [['span:has-text("has HOA")']],
                    "hoa_fee": [['span:has-text("HOA fee")']],
                    "basement": [['span:has-text("Has basement")']],
                    "fencing": [['span:has-text("Fencing")']],
                    "gas": [['span:has-text("Gas information")']],
                    "sewer": [['span:has-text("Sewer information")']],
                    "water": [['span:has-text("Water information")']],
                    "utilities": [['span:has-text("Utilities for property")']],
                    "construction_materials": [
                        ['span:has-text("Construction materials:")']
                    ],
                    "parcel_number": [['span:has-text("Parcel number")']],
                    "bedroom_features": [
                        [
                            'h6:text-is("Bedroom")',
                            "xpath=..",
                            'span:has-text("Features")',
                        ]
                    ],
                    "bathroom_features": [
                        [
                            'h6:text-is("Bathroom")',
                            "xpath=..",
                            'span:has-text("Features")',
                        ]
                    ],
                    "dining_features": [
                        [
                            'h6:text-is("Dining room")',
                            "xpath=..",
                            'span:has-text("Features")',
                        ]
                    ],
                    "family_features": [
                        [
                            'h6:text-is("Family room")',
                            "xpath=..",
                            'span:has-text("Features")',
                        ]
                    ],
                    "kitchen_features": [
                        [
                            'h6:text-is("Kitchen")',
                            "xpath=..",
                            'span:has-text("Features")',
                        ]
                    ],
                    "flooring": [['span:has-text("Flooring")']],
                    "heating": [['span:has-text("Heating features")']],
                    "cooling": [['span:has-text("Cooling features")']],
                    "included_appliances": [['span:has-text("Appliances included")']],
                    "laundry": [['span:has-text("Laundry features")']],
                    "pool_features": [['span:has-text("Pool features")']],
                    "view_description": [['span:has-text("View description")']],
                    "senior_community": [['span:has-text("Senior community")']],
                    "interior_features": [['span:has-text("Interior features")']],
                    "fireplace_features": [['span:has-text("Fireplace features")']],
                    "fireplace_count": [
                        ['span:has-text("Total number of fireplaces")']
                    ],
                    "spa_features": [['span:has-text("Spa features")']],
                    "patio_porch_details": [['span:has-text("Patio & porch details")']],
                    "zoning": [['span:has-text("Zoning")']],
                    "exterior_features": [['span:has-text("Exterior features")']],
                    "amenities": [['span:has-text("Amenities included")']],
                    "services": [['span:has-text("Services included")']],
                    "exterior_features": [['span:has-text("Exterior features")']],
                    "interior_features": [['span:has-text("Interior features")']],
                    "accessibility_features": [
                        ['span:has-text("Accessibility features")']
                    ],
                    "additional_structures": [
                        ['span:has-text("Additional structures included")']
                    ],
                }
                fact_info = {}
                for key, fact_locators in fact_locators.items():
                    element = None
                    for locators in fact_locators:
                        element = facts_element
                        for locator in locators:
                            element = element.locator(locator)
                            if not await element.count():
                                element = None
                                break

                        if element and element != facts_element:
                            break
                        else:
                            element = None

                    if not element or not await element.count():
                        fact_info[key] = None
                        continue

                    if await element.count() > 1:
                        element = element.nth(0)
                    element_text = (await element.inner_text()).split(": ")[1]

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

                    fact_info[key] = [element_text]
                property_info["details"] = fact_info

                pprint.pprint(property_info)
                zillow_property_id = url.split("/")[-2].split("_")[0]
                await insert_database(property_info, db)
                await store_data(zillow_property_id, end, failed)

            except Exception as error:
                print(error)
                zillow_property_id = url.split("/")[-2].split("_")[0]
                failed.add(int(zillow_property_id))

            finally:
                await open_browser.close()


def db_insert_worker(queue, db):
    while True:
        try:
            property_info = queue.get()
            if property_info is None:
                break

            insert_database(property_info, db)
            queue.task_done()

        except Exception as error:
            print(error)


def scrape_complete_callback(zillow_property_id, end, failed):
    def callback(_):
        if zillow_property_id in failed:
            return
        store_data(zillow_property_id, end, failed)

    return callback


async def get_zillow_range(start, end, failed, db, semaphore_count):
    # property_queue = queue.Queue()
    #
    # db_insert_thread = threading.Thread(
    #     target=db_insert_worker,
    #     args=(
    #         property_queue,
    #         db,
    #     ),
    # )
    # db_insert_thread.daemon = True
    # db_insert_thread.start()
    #
    # with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    #     futures = []
    #     for zillow_property_id in range(start, end, 1):
    #         future = executor.submit(
    #             get_zillow,
    #             f"https://www.zillow.com/homedetails/{zillow_property_id}_zpid/",
    #             property_queue,
    #             failed,
    #         )
    #         future.add_done_callback(
    #             scrape_complete_callback(zillow_property_id, end, failed)
    #         )
    #         futures.append(future)
    #
    # for future in concurrent.futures.as_completed(futures):
    #     future.result()

    tasks = set()
    semaphore = asyncio.Semaphore(semaphore_count)

    for zillow_property_id in range(start, end):
        task = asyncio.create_task(
            get_zillow(
                f"https://www.zillow.com/homedetails/{zillow_property_id}_zpid/",
                failed,
                db,
                semaphore,
                end,
            )
        )
        tasks.add(task)
        if len(tasks) >= semaphore_count:
            await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    await asyncio.gather(*tasks)

    # property_queue.put(None)
    print("Failed:", failed)
    return failed


async def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    continue_parser = subparsers.add_parser("continue")

    start_parser = subparsers.add_parser("start")
    start_parser.add_argument("--start", type=int, required=True)
    start_parser.add_argument("--end", type=int, required=True)

    args = parser.parse_args()

    # db = psycopg2.connect(
    #     database=DB_DATABASE,
    #     host=DB_HOST,
    #     user=DB_USERNAME,
    #     password=DB_PASSWORD,
    #     port=DB_PORT,
    # )
    db_pool = await asyncpg.create_pool(CONNECTION_STRING)
    if not db_pool:
        raise ValueError("Database connection failed")

    if args.command == "continue":
        continue_data = await load_data()
        if not continue_data:
            print("There is no cursor file or there is no data in the cursor file")
        print(
            f"""
            Continuing from {continue_data['start']} to {continue_data['end']}.
            Failures so far: {continue_data['failed']}.
        """
        )
        await get_zillow_range(
            continue_data["start"],
            continue_data["end"],
            continue_data["failed"],
            db_pool,
            5,
        )

    elif args.command == "start":
        print(f"Start command from {args.start} to {args.end}")
        print("Starting")
        await get_zillow_range(args.start, args.end, set(), db_pool, 5)

    await db_pool.close()


if __name__ == "__main__":
    asyncio.run(main())
