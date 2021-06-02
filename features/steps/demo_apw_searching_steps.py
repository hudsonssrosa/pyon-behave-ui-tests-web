from behave import *
from features.pages.demo_automation_practice_website.home_page import HomePage

home_page = HomePage(object)


@given("that Automation Practice website is open")
def step_given_that_automation_practice_is_open(context):
    home_page.open(context.url)


@when('user types the "{clothing_name}" on search')
def step_when_user_types_the_clothing_name_on_search(context, clothing_name):
    context.clothing = clothing_name
    home_page.type_input_search(context.clothing)
    home_page.click_on_search_button()


@when('user sees the unit price "{unit_price}" from an "{item}"')
def step_when_user_sees_the_unit_price_from_item(context, unit_price, item):
    context.unit_price = unit_price
    home_page.type_input_search(item)
    home_page.click_on_search_button().wait_until_product_name_is_visible(context.clothing)
    home_page.validate_label_product_unit_price(context.unit_price)


@then("the product is found after search")
def step_then_teh_product_is_found_after_search(context):
    home_page.take_screenshot("home_page_search_results")
    (
        home_page.wait_until_product_name_is_visible(context.clothing).validate_label_product_name(
            context.clothing
        )
    )