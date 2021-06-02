@demo-web-apw
Feature: Choosing and sending a product to cart in Automation Practice website

	@demo-find-product
	Scenario Outline: The user can search a product and send to the chart
		Given that Automation Practice website is open
		When user types the "<item>" on search
		Then the product is found after search

		Examples:
			| item   |
			| Blouse |

	@demo-total-purchase
	Scenario Outline: The user can send a product to the chart
		Given that Automation Practice website is open
		When user types the "<item>" on search
		And user sees the unit price "<unit_price>" from an "<item>"
		And user adds to chart proceeding to checkout
		Then the "<total_purchasing>" considers the correct "<total_shipping>"

		Examples:
			| item   | unit_price | total_shipping | total_purchasing |
			| Blouse | $27.00     | $2.00          | $29.00           |
