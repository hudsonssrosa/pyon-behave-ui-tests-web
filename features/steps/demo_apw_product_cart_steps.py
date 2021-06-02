from behave import *
from features.pages.demo_automation_practice_website.home_page import HomePage
from features.pages.demo_automation_practice_website.modal_cart_page import ModalCartPage

home_page = HomePage(object)
modal_cart_page = ModalCartPage(object)


@when("user adds to chart proceeding to checkout")
def step_when_user_adds_to_chart_proceeding_to_checkout(context):
    (home_page.move_over_to_product().click_on_add_to_cart_button())
    (
        modal_cart_page.wait_until_modal_cart_is_visible()
        .wait_until_proceed_to_checkout_is_visible()
        .click_on_proceed_to_checkout()
    )
