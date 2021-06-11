import os
import json
import requests
import socket

from behave import fixture
from sys import platform as _platform

from factory.singleton_web_driver import WebDriver
from factory.handling.base_logging import BaseLogging as Log
from factory.handling.running_exception import RunningException as Rexc
from factory.base_context import BaseContext as Bctx
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver

from settings.environment_data_provider import EnvSettings as Conf
from factory.utils.OsUtil import OsUtil

import urllib3

urllib3.disable_warnings()


SAFARIDRIVER = "safaridriver"
GECKODRIVER = "geckodriver"
CHROMEDRIVER = "chromedriver"
browser = None
cap_config = lambda conf_condition: True if conf_condition == "true" else False
set_flag_in_cap = (
    lambda flag_context, config_var: flag_context if flag_context != "" else config_var
)


def log_web_driver_error(ex):
    Rexc.raise_exception_error(f"Error to execute the Web Driver. \nPrevious cause: ", ex)


def log_web_driver_in_instance(webdriver_name):
    Log.success(f"▶ {str(webdriver_name).upper()} is running...")


def check_web_driver_dir():
    if os.path.exists(Conf.get_external_web_driver_dir()):
        return Conf.get_external_web_driver_dir()
    else:
        return Conf.get_internal_resources_webdriver_dir()


def provide_webdriver(context, browser_session, wd_name):
    try:
        browser_session.maximize_window()
        WebDriver.delete_cookies()
    except Exception:
        pass
    log_web_driver_in_instance(wd_name + f"- ID: {Bctx.random_data.get()}")
    WebDriver.set_driver(browser_session)
    context.web = WebDriver.use()
    WebDriver.set_driver(context.web)

    yield WebDriver


@fixture(name="chrome")
def browser_chrome(context):
    chrome_options = webdriver.ChromeOptions()
    message_headless = ""
    caps = {"platform": "ANY", "browserName": "chrome", "javascriptEnabled": True}
    if Bctx.flag_mode.get() == "headless":
        chrome_options.headless = True
        chrome_options.add_argument("window-size=1920,1080")
        message_headless = "HEADLESS"
    else:
        chrome_options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--start-maximized")
    global browser
    try:
        web_driver_executable = (
            check_web_driver_dir()
            + os.sep
            + CHROMEDRIVER
            + OsUtil.get_os_platform_web_driver_name()
        )
        browser = webdriver.Chrome(
            executable_path=web_driver_executable,
            chrome_options=chrome_options,
            desired_capabilities=caps,
        )
    except:
        browser = webdriver.Chrome()
    finally:
        log_web_driver_in_instance(CHROMEDRIVER + " - " + message_headless)
        yield from provide_webdriver(context, browser, CHROMEDRIVER + " - " + message_headless)


@fixture(name="firefox")
def browser_firefox(context):
    binary = ""
    global browser
    if _platform == "win64" or _platform == "win32":
        binary = FirefoxBinary(f"C:{os.sep}Program Files{os.sep}Mozilla Firefox{os.sep}firefox.exe")
    else:
        binary = FirefoxBinary(f"{os.sep}usr{os.sep}lib{os.sep}firefox{os.sep}firefox")
    web_driver_executable = (
        check_web_driver_dir()
        + os.sep
        + GECKODRIVER
        + OsUtil.get_os_platform_to_execute_a_file_format()
    )
    browser = webdriver.Firefox(
        firefox_binary=binary,
        executable_path=web_driver_executable,
        desired_capabilities=webdriver.DesiredCapabilities.FIREFOX,
    )
    yield from provide_webdriver(context, browser, GECKODRIVER)


@fixture(name="safari")
def browser_safari(context):
    global browser
    default_browser = f"{os.sep}usr{os.sep}bin{os.sep}safaridriver"
    browser = webdriver.Safari(executable_path=default_browser)
    yield from provide_webdriver(context, browser, SAFARIDRIVER)


@fixture(name="crossbrowsertesting")
def crossbrowser(context):
    build_number = os.environ.get("BUILD_NUMBER", f"{Bctx.random_data.get()}")
    cbt_username = os.environ.get("CBT_USERNAME", Conf.get_cbt_username())
    cbt_authkey = os.environ.get("CBT_APIKEY", Conf.get_cbt_authkey())
    cbt_os = Bctx.flag_os.get()
    cbt_os_version = Bctx.flag_os_version.get()
    cbt_browser = Bctx.flag_browser.get()
    cbt_resolution = Bctx.flag_resolution.get()
    cbt_mobile_os = Bctx.flag_os.get()
    cbt_mobile_os_version = Bctx.flag_os_version.get()
    cbt_mobile_browser = Bctx.flag_browser.get()
    cbt_mobile_device = Bctx.flag_device_name.get()
    cbt_mobile_orientation = Bctx.flag_orientation.get()
    cbt_sel_url = "https://crossbrowsertesting.com/api/v3/selenium/"
    context.api_session = requests.Session()
    context.api_session.auth = (cbt_username, cbt_authkey)
    context.test_result = None
    url = f"http://{cbt_username}:{cbt_authkey}@hub.crossbrowsertesting.com:80/wd/hub"
    caps = {
        "name": set_test_build_description(build_number),
        "build": set_project_build_description(build_number),
        "record_video": Conf.get_cbt_record_video(),
        "record_network": Conf.get_cbt_record_network(),
        "max_duration": "5400",
        "timezone": "GMT+01:00",
        "acceptSslCerts": "true",
        "browserConnectionEnabled": "false",
        "unexpectedAlertBehaviour": "ignore",
        "databaseEnabled": "false",
    }
    if Bctx.flag_mode.get() == "headless":
        caps["browserName"] = "Chrome"
        caps["platform"] = "Headless"
        caps["version"] = "Latest"
        caps["screenResolution"] = "1280x1024"
    elif Bctx.flag_mode.get() == "mobile":
        caps["browserName"] = cbt_mobile_browser
        caps["deviceName"] = cbt_mobile_device
        caps["platformName"] = cbt_mobile_os
        caps["platformVersion"] = cbt_mobile_os_version
        caps["deviceOrientation"] = cbt_mobile_orientation
    else:
        caps["browser_api_name"] = cbt_browser
        caps["browser_name"] = cbt_browser
        caps["os_api_name"] = cbt_os
        caps["platform"] = cbt_os
        caps["version"] = cbt_os_version
        caps["take_snapshot"] = Conf.get_cbt_take_snapshot()
        caps["screenResolution"] = cbt_resolution
    rem = webdriver.Remote(desired_capabilities=caps, command_executor=url)
    snapshot_hash = None
    cbt_headless_name = "Headless: Chrome80x64" if Bctx.flag_mode.get() == "headless" else cbt_os
    try:
        yield from provide_webdriver(context, rem, "CROSSBROWSER-TESTING: " + cbt_headless_name)
        snapshot_hash = context.api_session.post(
            cbt_sel_url + rem.session_id + "/snapshots"
        ).json()["hash"]
        context.test_result = "pass"
        if context.test_result is not None:
            context.api_session.put(
                cbt_sel_url + rem.session_id,
                data={"action": "set_score", "score": context.test_result},
            )
    except Exception as ex:
        context.api_session.put(
            cbt_sel_url + rem.session_id + "/snapshots/" + snapshot_hash,
            data={"description": "AssertionError: " + str(ex)},
        )
        context.test_result = "fail"
        log_web_driver_error(ex)


@fixture(name="browserstack")
def browserstack(context):
    build_number = os.environ.get("BUILD_NUMBER", f"{Bctx.random_data.get()}")
    bs_username = os.environ.get("BS_USERNAME", Conf.get_bs_user_key())
    bs_authkey = os.environ.get("BS_ACCESS_KEY", Conf.get_bs_access_key())
    bs_os = Bctx.flag_os.get()
    bs_os_version = Bctx.flag_os_version.get()
    bs_browser = Bctx.flag_browser.get()
    bs_browser_version = Bctx.flag_browser_version.get()
    bs_resolution = Bctx.flag_resolution.get()
    bs_mobile_os = Bctx.flag_os.get()
    bs_mobile_os_version = Bctx.flag_os_version.get()
    bs_mobile_browser = Bctx.flag_browser.get()
    bs_mobile_device = Bctx.flag_device_name.get()
    bs_mobile_orientation = Bctx.flag_orientation.get()
    bs_headless_name = "Headless: Chrome" if Bctx.flag_mode.get() == "headless" else bs_os
    caps = {
        "name": set_test_build_description(build_number),
        "project": "PYON-UI-TESTS",
        "build": set_project_build_description(build_number),
        "browser_version": "Latest",
        "browserstack.video": Conf.get_bs_record_video(),
        "browserstack.local": "false",
        "browserstack.seleniumLogs": "true",
        "browserstack.appiumLogs": "false",
        "browserstack.networkLogs": "false",
        "realMobile": "true" if Bctx.flag_mode.get() == "mobile" else "false",
        "acceptSslCerts": "true",
    }
    if Bctx.flag_mode.get() == "headless":
        caps["resolution"] = "1280x1024"
    elif Bctx.flag_mode.get() == "mobile":
        caps["browserName"] = bs_mobile_browser
        caps["deviceName"] = bs_mobile_device
        caps["device"] = bs_mobile_device
        caps["platformName"] = bs_mobile_os
        caps["os_version"] = bs_mobile_os_version
        caps["deviceOrientation"] = bs_mobile_orientation
    elif Bctx.flag_mode.get() == "app":
        app_path = (
            str(os.path.abspath(Bctx.flag_mobile_app_path.get()))
            .replace("\\", os.sep)
            .replace("//", os.sep)
        )
        Log.info(app_path)
        result = os.popen(
            f'curl -u "{bs_username}:{bs_authkey}" -X POST "https://api-cloud.browserstack.com/app-automate/upload" -F "file=@{app_path}"'
        ).read()
        app_id = json.loads(result)
        OsUtil.set_env_var("MOB_APP_ID", str(app_id["app_url"]))
        caps["browserName"] = bs_mobile_browser
        caps["deviceName"] = bs_mobile_device
        caps["device"] = bs_mobile_device
        caps["platformName"] = bs_mobile_os
        caps["os_version"] = bs_mobile_os_version
        caps["deviceOrientation"] = bs_mobile_orientation
        caps["app"] = os.environ["MOB_APP_ID"]
    else:
        caps["browser"] = bs_browser
        caps["browser_version"] = bs_browser_version
        caps["os"] = bs_os
        caps["os_version"] = bs_os_version
        caps["resolution"] = bs_resolution
    web_rem = webdriver.Remote(
        command_executor=f"http://{bs_username}:{bs_authkey}@hub-cloud.browserstack.com/wd/hub",
        desired_capabilities=caps,
    )
    yield from provide_webdriver(context, web_rem, "BROWSERSTACK: " + bs_headless_name)
    requests.put(
        f"https://{bs_username}:{bs_authkey}@api.browserstack.com/automate/sessions/<session-id>.json",
        data={"status": "passed", "reason": ""},
    )


@fixture(name="lambdatest")
def lambdatest(context):
    build_number = os.environ.get("LT_BUILD_NUMBER", f"{Bctx.random_data.get()}")
    lt_user = os.environ.get("LT_USERNAME", Conf.get_lt_username())
    lt_key = os.environ.get("LT_APPKEY", Conf.get_lt_app_key())
    lt_os = Bctx.flag_os.get()
    lt_browser = Bctx.flag_browser.get()
    lt_browser_version = Bctx.flag_browser_version.get()
    lt_resolution = Bctx.flag_resolution.get()
    lt_headless_name = "Headless: Chrome" if Bctx.flag_mode.get() == "headless" else ""
    caps = {
        "name": set_test_build_description(build_number),
        "build": set_project_build_description(build_number),
        "tunnel": cap_config(Conf.get_lt_tunnel()),
        "visual": cap_config(Conf.get_lt_visual()),
        "video": cap_config(Conf.get_lt_video()),
        "console": cap_config(Conf.get_lt_console()),
        "network": cap_config(Conf.get_lt_network()),
        "javascriptEnabled": True,
        "timezone": "UTC+00:00",
        "acceptSslCerts": True,
    }
    if Bctx.flag_mode.get() == "headless":
        caps["headless"] = True
        caps["platform"] = "Windows 10"
        caps["browserName"] = "Chrome"
        caps["resolution"] = "1280x1024"
    else:
        caps["browserName"] = lt_browser
        caps["version"] = lt_browser_version
        caps["platform"] = lt_os
        caps["resolution"] = lt_resolution
    web_rem = webdriver.Remote(
        command_executor=f"http://{lt_user}:{lt_key}@hub.lambdatest.com/wd/hub",
        desired_capabilities=caps,
    )
    web_rem.maximize_window()
    yield from provide_webdriver(context, web_rem, "LAMBDATEST: " + lt_headless_name)


def set_test_build_description(build_number):
    environment = str(Bctx.flag_environment.get()).upper()
    scenario = Bctx.flag_scenario.get()
    tags_fmt = "Tag: #" + Bctx.cur_tag.get() if scenario is not None or scenario != "" else ""
    return f"[{build_number}] | {environment} | {tags_fmt} {scenario}"


def set_project_build_description(build_number):
    environment = str(Bctx.flag_environment.get()).upper()
    hostname = "-"
    try:
        hostname = socket.gethostname()
    except:
        hostname = "Undefined"
    tags = (
        "Tags: #"
        + str(
            str(Bctx.flag_tags.get()).replace("--tags=", "").replace("-", " ").replace(",", "  #")
        )
        .title()
        .strip()
    )
    return f"BUILD-[{build_number}]-PyonUIT | {environment} | {tags} | Server-{hostname}"


fixture_registry = {
    "chrome": browser_chrome,
    "firefox": browser_firefox,
    "safari": browser_safari,
    "browserstack": browserstack,
    "crossbrowsertesting": crossbrowser,
    "lambdatest": lambdatest,
}
