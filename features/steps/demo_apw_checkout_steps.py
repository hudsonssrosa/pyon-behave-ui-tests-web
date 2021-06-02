from behave import *
from features.pages.demo_automation_practice_website.shopping_cart_summary_page import (
    CartSummaryPage,
)

cart_summary_page = CartSummaryPage(object)


@then('the "{total_purchasing}" considers the correct "{total_shipping}"')
def step_then_the_total_purchasing_considers_the_correct_total_shipping(
    context, total_shipping, total_purchasing
):
    cart_summary_page.take_screenshot("cart_page_totals")
    (
        cart_summary_page.validate_label_total_product(context.unit_price)
        .validate_label_total_shipping(total_shipping)
        .validate_label_total_price(total_purchasing)
    )
