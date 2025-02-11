import os
from dotenv import load_dotenv
import re
import time
import json
from twocaptcha import TwoCaptcha
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

def get_element(locator, browser):
    return WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.XPATH, locator)))

def get_captcha_params(browser):
    browser.refresh()
    intercept_script = """ 
        console.clear = () => console.log('Console was cleared')
        const i = setInterval(()=>{
            if (window.turnstile) {
                console.log('success!!');
                clearInterval(i);
                window.turnstile.render = (a,b) => {
                    let params = {
                        sitekey: b.sitekey,
                        pageurl: window.location.href,
                        data: b.cData,
                        pagedata: b.chlPageData,
                        action: b.action,
                        userAgent: navigator.userAgent,
                    };
                    console.log('intercepted-params:' + JSON.stringify(params));
                    window.cfCallback = b.callback;
                    return;
                };
            }
        },50);
    """
    browser.execute_script(intercept_script)
    # Wait a few seconds to allow the logs to be generated.
    time.sleep(5)
    logs = browser.get_log("browser")
    params = None
    for log in logs:
        if "intercepted-params:" in log['message']:
            # Decode the log message
            log_entry = log['message'].encode('utf-8').decode('unicode_escape')
            match = re.search(r'intercepted-params:({.*?})', log_entry)
            if match:
                json_string = match.group(1)
                params = json.loads(json_string)
                break
    print("Parameters received:", params)
    return params

def solver_captcha(apikey, params):
    solver = TwoCaptcha(apikey)
    try:
        result = solver.turnstile(
            sitekey=params["sitekey"],
            url=params["pageurl"],
            action=params["action"],
            data=params["data"],
            pagedata=params["pagedata"],
            useragent=params["userAgent"]
        )
        print("Captcha solved")
        return result['code']
    except Exception as e:
        print(f"An error occurred while solving captcha: {e}")
        return None

def send_token_callback(token, browser):
    script = f"cfCallback('{token}')"
    browser.execute_script(script)
    print("The token is sent to the callback function")

def final_message(browser):

    locator = "//p[contains(@class,'successMessage')]"
    message = get_element(locator, browser).text
    print("Final message:", message)


def trigger_capcha(browser):
    apikey = os.getenv('apikey') 
    params = get_captcha_params(browser)
    if params:
        token = solver_captcha(apikey, params)
        if token:
            send_token_callback(token, browser)
            try:
                final_message(browser)
            except Exception:
                print("Success message element not found; skipping verification.")
            print("Captcha process finished")
        else:
            print("Failed to solve captcha")
    else:
        print("Intercept captcha parameters did not trigger")