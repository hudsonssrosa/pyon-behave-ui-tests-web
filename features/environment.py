from behave import use_fixture
from features import fixtures
from factory.singleton_web_driver import WebDriver
from factory.handling.base_logging import BaseLogging as Log
from factory.base_context import BaseContext as Bctx
from factory.handling.running_exception import RunningException as Rexc
from factory.utils.DataEncryptedUtil import DataEncrypted as RandData
from factory.utils.StringsUtil import StringUtil as String
from settings.environment_data_provider import EnvSettings as Conf
from settings.secrets_data_provider import SecretsSettings as SecFile

import urllib3
import traceback

urllib3.disable_warnings()

EXCLUDE_TAG = Bctx.flag_exclude.get()
SKIP_TAG = EXCLUDE_TAG if EXCLUDE_TAG is not None or EXCLUDE_TAG != "None" else "skip"
message_skipped_tags = f"    \n ctx SKIPPED WITH TAG: @{SKIP_TAG}"


def before_all(context):
    app_env = {
        "dev": Conf.get_url_app_dev(),
        "staging": Conf.get_url_app_staging(),
        "production": Conf.get_url_app_prod(),
    }
    admin_env = {
        "dev": Conf.get_admin_url_dev(),
        "staging": Conf.get_admin_url_staging(),
        "production": Conf.get_admin_url_prod(),
    }
    context.config.setup_logging()
    context.url = String.correct_link_bar(app_env[Bctx.flag_environment.get()])
    context.email_url = String.correct_link_bar(Conf.get_email_url())

    Bctx.random_data.set(RandData.generate_random_data(length=7))
    Log.info(f"Hash available for test scope: {Bctx.random_data.get()}")
    context.random_data = Bctx.random_data.get()
    Bctx.configcat_sdk_key_ff_dev.set(SecFile.get_secret_configcat_sdk_key_ff_dev())
    Bctx.configcat_sdk_key_ff_staging.set(SecFile.get_secret_configcat_sdk_key_ff_staging())
    Bctx.configcat_sdk_key_ff_production.set(SecFile.get_secret_configcat_sdk_key_ff_production())
    Log.info(f"ConfigCat SDK Keys are ready!")
    Bctx.app_url.set(context.url)
    Bctx.email_url.set(context.email_url)
    Log.info(f"URLs from application is ready!")


def before_feature(context, feature):
    Log.gherkin_feature_info(feature)
    if SKIP_TAG in feature.tags:
        feature.skip(f"Marked with @{SKIP_TAG}")
        Log.warning(message_skipped_tags.replace("ctx", "FEATURE"))
        return


def after_feature(context, feature):
    print("\n")


def before_scenario(context, scenario):
    last_scn_tag_name = scenario.effective_tags[len(scenario.effective_tags) - 1]
    scn_tags = f"---> TAG(s): @{last_scn_tag_name}\n"
    Log.gherkin_scenario_info(f"{scenario} {scn_tags}")
    if SKIP_TAG in scenario.effective_tags:
        scenario.skip(f"Marked with @{SKIP_TAG}")
        Log.warning(message_skipped_tags.replace("ctx", "SCENARIO"))
        return
    Bctx.flag_scenario.set(f"{scenario}")
    target_context = Bctx.flag_target.get()
    browser_context = Bctx.flag_browser.get()
    platform_execution = (
        lambda flag_cmd, fixture_def: use_fixture(fixture_def, context) if flag_cmd else None
    )
    try:
        if target_context == "local":
            platform_execution(browser_context == "chrome", fixtures.browser_chrome)
            platform_execution(browser_context == "firefox", fixtures.browser_firefox)
            platform_execution(browser_context == "safari", fixtures.browser_safari)
        else:
            platform_execution(target_context == "bs", fixtures.browserstack)
            platform_execution(target_context == "lt", fixtures.lambdatest)
    except Exception as ex:
        Rexc.raise_exception_error(f"RAISING ERROR.\n   Previous cause: ", ex)


def after_scenario(context, scenario):
    WebDriver.quit_webdriver()


def before_step(context, step):
    Log.gherkin_step_info(step)


def after_step(context, step):
    is_lambdatest_cloud = Bctx.flag_target.get() == "lt"
    if step.status == "passed":
        Log.status_passed()
        if is_lambdatest_cloud:
            WebDriver.execute_javascript("lambda-status=passed")
    if step.status == "failed":
        txt_tb = "".join(traceback.format_tb(step.exc_traceback))
        Log.status_failed(stacktrace=txt_tb)
        take_screenshot_when_is_failed(context)
        if is_lambdatest_cloud:
            WebDriver.execute_javascript("lambda-status=failed")


def before_tag(context, tag):
    Bctx.cur_tag.set(tag)


def take_screenshot_when_is_failed(context):
    try:
        WebDriver.take_screenshot("Failed")
    except:
        pass
