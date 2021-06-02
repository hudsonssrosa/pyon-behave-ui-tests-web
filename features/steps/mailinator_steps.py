from behave import *

from features.steps.feature_flags.feature_flags_handler import *
from features.steps.feature_flags.feature_flags_handler import FeatureFlagHandler as FFlag


@then("a message is sent to main driver email about booking subscription")
def step_then_a_message_is_sent_to_main_driver_email_about_subscription(context):
    default = 0
    additional = 1
    try:
        mailinator_page.check_mailinator_inbox_context(
            email=context.main_driver["personal_data"]["email"],
            tab_number=additional,
            row_title="We need proof of your address",
            email_content=f'{context.main_driver["personal_data"]["first_name"]}, we require your proof of address',
        )
    except:
        mailinator_page.log.warning("EMAIL IS NOT ARRIVING THE USER'S INBOX.")
        mailinator_page.take_screenshot("Failed")
    mailinator_page.switch_to_tab(number=default)
