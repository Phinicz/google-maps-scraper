from selenium.webdriver.common.by import By
import urllib.parse
from selenium.webdriver.common.by import By
from bose import BaseTask, Wait, Output
import time, sys, json
import pywhatkit as kit 
import datetime, time
import pyautogui

counter = 0
msg =[
    """Hi there,

I noticed you don’t have a website for your shop and I can build a modern beautiful website for your place. I’m a student and I’m building my portfolio. I charge $50 for the website, and if you didn’t like the final result, you don’t pay anything. A website can shift your online presence 180 degrees; most sales now are online.

The website consists of four sections. The first is an introduction about the place, name, and exact location. The second is products you sell, their pictures, titles, and price. The third is a contact us page with a button and animation that, when clicked, will open the phone app and insert your phone number. The final section is reviews that I will pull online with their pictures.

Thank you in advance. Message me back if you like the proposal, and we can discuss how you want it to look.""",
"""Hi there,

I found your Shop on google maps, and I checked your website, and I think I can rebuild your website to be so much better and modern and change your customers' experience. I’m a student, and I’m building my portfolio, and I will make your website for $50, and if you didn’t like what you see, you pay nothing.

Thanks in advance, message me, and we can discuss if you want it to look a specific way or if you have something in mind already."""
]

def write(result):
    Output.write_finished(result)
    Output.write_csv(result, "finished.csv")


def do_filter(ls, filter_data):
    def fn(i):

        min_rating = filter_data.get("min_rating")
        min_reviews = filter_data.get("min_reviews")
        is_kosher = filter_data.get("is_kosher", False)
        is_car = filter_data.get("is_car", False)
        has_phone = filter_data.get("has_phone")
        has_website = filter_data.get("has_website")

        rating = i.get('rating')
        number_of_reviews = i.get('number_of_reviews')
        title = i.get("title")
        category = i.get("category")
        web_site = i.get("website")
        phone = i.get("phone")

        if min_rating != None:
            if rating == '' or rating is None or rating < min_rating:
                return False

        if min_reviews != None:
            if number_of_reviews == '' or number_of_reviews is None or number_of_reviews < min_reviews:
                return False

        if is_kosher:
            if 'kosher' in category.lower() or 'jew' in category.lower() or 'kosher' in title.lower() or 'jew' in title.lower():
                pass
            else:
                return False

        if has_website is not None:
            if has_website == False:
                if web_site is not None:
                    return False

        if has_phone is not None:
            if has_phone == True:
                if phone is None or phone == '':
                    return False

        if is_car:
            if 'car' in category.lower() or 'car' in title.lower():
                pass
            else:
                return False

        return True

    return list(filter(fn, ls))


class Task(BaseTask):
    
    GET_FIRST_PAGE = False
    queries = [
        "cloth shop near me in London",
        "cloth shop near me in Birmingham",
        "cloth shop near me in Manchester",
        "cloth shop near me in Glasgow",
        "cloth shop near me in Leeds",
        "cloth shop near me in Liverpool",
        "cloth shop near me in Newcastle",
        "cloth shop near me in Sheffield",
        "cloth shop near me in Bristol",
        "cloth shop near me in Edinburgh",
        "cloth shop near me in Cardiff",
        "cloth shop near me in Belfast",
        "cloth shop near me in Nottingham",
        "cloth shop near me in Southampton",
        "cloth shop near me in Brighton",
        "cloth shop near me in Plymouth",
        "cloth shop near me in Reading",
        "cloth shop near me in Aberdeen",
        "cloth shop near me in Oxford",
        "cloth shop near me in Cambridge",
        "cloth shop near me in York",
        "cloth shop near me in Swansea",
        "cloth shop near me in Norwich",
        "cloth shop near me in Exeter",
        "cloth shop near me in Dundee",
        "cloth shop near me in Bath",
        "cloth shop near me in Inverness",
        "cloth shop near me in Canterbury",
        "cloth shop near me in Portsmouth",
        "cloth shop near me in Wolverhampton",
        "cloth shop near me in Sunderland",
        "cloth shop near me in Leicester",
        "cloth shop near me in Aberdeen",
        "cloth shop near me in Stoke-on-Trent",
        "cloth shop near me in Preston",
        "cloth shop near me in Hull",
        "cloth shop near me in Swansea",
        "cloth shop near me in Wrexham",
        "cloth shop near me in Dundee",
        "cloth shop near me in Wolverhampton",
        "cloth shop near me in Blackpool",
        "cloth shop near me in Ipswich",
        "cloth shop near me in Telford"
    ]

    
    

    def run(self, driver):
        def get_links(query):
            def scroll_till_end(times):
                try:
                    current_time = time.time()
                    def visit_gmap():
                        endpoint = f'maps/search/{urllib.parse.quote_plus(query)}'
                        url = f'https://www.google.com/{endpoint}'
                        try:
                            time.sleep(1)
                            english_link = driver.find_element(By.XPATH, '//a[text()="English"]')
                            english_link.click()
                            time.sleep(3)
                        except Exception as e:
                            print("now to the next word")
                        driver.get_by_current_page_referrer(url)

                        if not driver.is_in_page(endpoint, Wait.LONG * 3):
                            print('Revisiting')
                            visit_gmap()

                    visit_gmap()
                    while time.time() - current_time < 60 * .12:
                            el = driver.get_element_or_none_by_selector(
                                '[role="feed"]', Wait.LONG)
                            time.sleep(5)
                            driver.scroll_element(el)
                except Exception as e:
                    print(f'ran into and error while scrolling Refreshing....')
                    

            scroll_till_end(1)

            def extract_links(elements):
                def extract_link(el):
                    return el.get_attribute("href")

                return list(map(extract_link, elements))

            els = driver.get_elements_or_none_by_selector(
                '[role="feed"]  [role="article"] > a', Wait.LONG)
            links = extract_links(els)

            Output.write_pending(links)

            print('Done Filter')

            return links

        def get_maps_data(links):
            def get_data(link):
                try:
                    driver.get_by_current_page_referrer(link)

                    tmp_elem = driver.get_element_or_none(
                        "//div[@class='TIHn2']", Wait.SHORT)
                    out_dict = {}
                    heading = driver.get_element_or_none_by_selector(
                        'h1', Wait.SHORT)

                    if heading is not None:
                        out_dict['title'] = heading.text

                    else:
                        out_dict['title'] = ''

                    rating = driver.get_element_or_none_by_selector(
                        'div.F7nice', Wait.SHORT)

                    if rating is not None:
                        val = rating.text
                    else:
                        val = None

                    if (val is None) or (val == ''):
                        out_dict['rating'] = None
                        out_dict['number_of_reviews'] = None
                    else:
                        out_dict['rating'] = float(val[:3].replace(',', '.'))
                        num = ''
                        for c in val[3:]:
                            if c.isdigit():
                                num = num + c
                        if len(num) > 0:
                            out_dict['number_of_reviews'] = int(num)
                        else:
                            out_dict['number_of_reviews'] = None

                    category = driver.get_element_or_none_by_selector(
                        'button[jsaction="pane.rating.category"]')
                    out_dict['category'] = '' if category is None else category.text
                    tmp_elem = driver.get_element_or_none("//div[@class='m6QErb']")

                    def get_el_text(el):
                        if el is not None:
                            return el.text
                        return ''

                    out_dict['address'] = get_el_text(
                        driver.get_element_or_none("//button[@data-item-id='address']"))
                    out_dict['website'] = get_el_text(
                        driver.get_element_or_none("//a[@data-item-id='authority']"))
                    out_dict['phone'] = get_el_text(driver.get_element_or_none(
                        "//button[starts-with(@data-item-id,'phone:tel:')]"))

                    tmp_elem = driver.get_element_or_none_by_selector(
                        ".RZ66Rb.FgCUCc img")

                    if tmp_elem is not None:
                        out_dict['img_link'] = tmp_elem.get_attribute("src")

                    out_dict['link'] = link

                    global counter
                    if out_dict['phone'] != '':
                        trim_phone = out_dict['phone'].replace(" ","").replace("-","")
                        kit.sendwhatmsg(trim_phone,msg[0] if out_dict["website"] == "" else msg[1] ,datetime.datetime.now().hour,datetime.datetime.now().minute+2)
                        time.sleep(20)
                        pyautogui.hotkey('alt', 'f4')
                        print(f"Message sent to {out_dict['phone']} @ index number {counter} {'No Website' if out_dict['website'] == '' else 'Has Website'}")
                        counter = counter + 1
                            
                    return out_dict
                except Exception as e:
                    print(f'error occured Now Refreshing.... {e}')
                    driver.refresh()
                    

            ls = list(map(get_data, links))
            return ls


        
        queries =  self.queries 

        def get_data():
            result = []
            max_listings = 10

            driver.get_google()

            for q in queries:
                links = get_links(q)

                print(f'Fetched {len(links)} links.')

                filter_data = {
                    "min_reviews": 0,
                    "has_phone": True,

                }

                a = get_maps_data(links)
                new_results = do_filter(a, filter_data)

                print(f'Filtered {len(new_results)} links from {len(a)}.')

                result = result + new_results
                if len(result) > max_listings:
                    return result

            return result

        result = get_data()
        write(result)