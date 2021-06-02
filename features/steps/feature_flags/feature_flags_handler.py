from factory.base_context import BaseContext as Bctx
from driver_wrappers.selenium.page_wrapper import BasePage
from factory.handling.configcat_impl import ConfigCat
from factory.utils.DataEncryptedUtil import DataEncrypted as RandomData

# Import all Page Object classes here
from features.pages.mailinator.inbox_page import InboxPage
from features.pages.demo_automation_practice_website.home_page import HomePage
from features.pages.demo_automation_practice_website.modal_cart_page import ModalCartPage
from features.pages.demo_automation_practice_website.shopping_cart_summary_page import (
    CartSummaryPage,
)

# Instantiate the Page objects imported
mailinator_page = InboxPage(object)
home_page = HomePage(object)
modal_cart_page = ModalCartPage(object)
cart_summary_page = CartSummaryPage(object)

is_production_environment = Bctx.flag_environment.get() == "production"
is_staging_environment = Bctx.flag_environment.get() == "staging"
is_dev_environment = Bctx.flag_environment.get() == "dev"


def is_the_flag_enabled(flag, context_data):

    """
    Use this method in the scenario steps to check feature flags from application reducing the complexity
    in use a same scenario to recognise when a feature flag from ConfigCat should be activated or deactivated
    for a specific user or not. To see further information about ConfigCat client implementation,
    get this link:

        https://configcat.com/docs/sdk-reference/python/

    Call this method considering

        from features.steps.feature_flags.feature_flag_handler import *

        @given("that a feature flag example is set")
        def step_given_that_a_feature_flag_is_set(context):
            if is_the_flag_enabled(flag=FFlag.ff_my_flag_to_be_on, context_data=context.user_email):
                # [IMPLEMENT THE LOGIC FOR NEW FF HERE]
            else:
                # [IMPLEMENT OTHER LOGIC IF THE FLAG IS SKIPPED]

    :return:
    """
    return ConfigCat.get_feature_flag(flag, fflag_state=True, email_address=context_data)


class FeatureFlagHandler(BasePage):
    """[summary]

    Args:
        BasePage (object): If your app is using ConfigCat to handle feature flags for the environments, just provide the existing flag name here
    """

    ff_my_flag_to_be_on_1 = "configcat_flag_name_1_here"
    ff_my_flag_to_be_on_2 = "configcat_flag_name_2_here"
    ff_my_flag_to_be_on_3 = "configcat_flag_name_3_here"
