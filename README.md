<img src=".resources/logos/pyon_logo_min.png" height="360">

# pyon-behave-ui-tests-web
PYON-BEHAVE | Selenium-based UI Automated Testing Framework in Python-Behave

Pyon UI Test Automation project is available to implement UI tests for web and mobile applications with the following stacks and approaches:

- Programming Language: [Python-based](https://www.python.org/downloads/).
- Framework for behavioural tests: [Behave](https://behave.readthedocs.io/en/latest/)
- Minimal library requirements: [Behave](https://pypi.org/project/behave/) and [Selenium](https://pypi.org/project/selenium/)

To know how you can configure your environment to implement and execute this project locally or even remotely, follow all the instructions from this documentation. So, let's start with it and good luck!

## CLONING THE PROJECT FROM GITHUB

Go to [GITHUB](https://github.com/hudsonssrosa/pyon-behave-ui-tests-web) and **CLONE** the project using **GIT** (download and install GIT from [here](https://git-scm.com/downloads))

In you local machine, choose you local repository and clone the project using SSH for Mac OS or Linux platforms with this command:

```bash
    git clone git@github.com:hudsonssrosa/pyon-behave-ui-tests-web.git
```

If you are having issues when cloning or pushing to the repository make sure you have all your SSH keys in place. Click [here](https://help.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh) for more information about it.

## PREPARING YOUR ENVIRONMENT

### 1. Install Python

Download and install the [latest Python](https://www.python.org/downloads/) version (3.8 or over). Then, in any terminal, try this command to check if Python is correctly installed:

```bash
      python
```

### 2. Choose a good IDE

Once you have opened the project in an IDE of your preference (suggestion: install [Visual Studio Code](https://code.visualstudio.com/download) or [PyCharm CE](https://www.jetbrains.com/pycharm/)), then you will need to *set the Python interpreter* for the project.

After this, you are able to create the *Python Virtual Environment* for the PyonUIT project and install all the requirements needed (libraries/packages). You just need to run for the first time the `update.py` and then the virtual environment as well the libraries in `requirements.txt` will be automatically installed for you.

- In Windows:

```bash
      python update.py
```

- In MacOSX or Linux:

```bash
      python3 update.py
```

### 3. Dockerize the project

At some point you will need to execute the tests from your local machine to simulate the environment like in a continuous integration server (with all requirements installed and configured properly - OS, Python, PYON and execution of tests in a specific server).
Install [Docker](https://www.docker.com/get-started), check if it is working for PYON and execute the `docker-compose` file with this command line:

```bash
    docker-compose run --rm web
 ```

Increment this command with CLI presented in next section 4.3, if you want to simulate the PyonUIT using Docker.

### 4. Ways to run this project

By default, the tests will run locally on Chrome browser, but you have 3 ways to customise your execution.

#### 4.1 Run in debugging mode

To check if the environment is totally operational to begin with some implementation, or even check the existing tests, you might dealing with the environment variables to prepare for an execution. Thus, copy the file `env_settings.properties.local` and paste the new one in project's root (in the same place as the original file) renaming it to `env_settings.properties`. So, you can edit the properties freely, because this file is ignored by GIT versioning.

Into this file, to consider a development setting, ensure the property `development_mode` is set as `true`. With this, all the properties that start with `debug_...` will be considered in a project debugging overwriting any command lines from CLI:

```properties
    development_mode = true
    debug_flag_environment = staging

    # Get more information about PYON CLI, type in the terminal console: "python behave_runner.py --help"
    debug_flag_target = local
    debug_flag_os =
    debug_flag_os_version =
    debug_flag_device_name =
    debug_flag_browser =
    debug_flag_browser_version =
    debug_flag_mode = web
    debug_behave_tags =
    debug_behave_excluded_tags = wip
    debug_flag_orientation =
    debug_flag_resolution = 1280x1024
```

- To generate Allure Reports locally, make sure you have `Java` installed and the flag `generate_report = true` on your `env_settings.properties`.

#### 4.2 Run as if it were in CI

After any implementation into the PyonUIT, it is recommended to validate the tests simulating an execution capable to inject parameters in environment variables, like it is performed in a build from a CI server. To validate a test execution, keep in mind to run in a remote server such as LambdaTest, BrowserStack or any other supported by PyonUIT in `fixtures.py`. Before this, you also will need to copy the file `run_behave.sh.local` and paste the new one in project's root (in the same place as the original file) renaming it to `run_behave.sh` to be ignored in commits.

Into this script file, you can set those environment variables, like this:

```bash
    PYON_ENVIRONMENT='staging'
    PYON_TARGET='lt'
    PYON_MODE='web'
    PYON_OS='MacOS Catalina'
    PYON_OS_VERSION=
    PYON_DEVICE='local'
    PYON_BROWSER='chrome'
    PYON_BROWSER_VERSION='90.0'
    PYON_ORIENTATION='Portrait'
    PYON_RESOLUTION='1280x1024'
    PYON_TAGS='demo-web-apw'
    PYON_EXCLUDED_TAG='wip'
```

#### 4.3 Run via CLI (only command line)

You can handle all those parameters presented previously (in section 4.2) setting them directly via CLI. You just need to pass the desired values in the arguments by command line.
First of all, call the main runner file in the terminal and press Enter. So, try this:

```bash
      python3 behave_runner.py --help
```

You might see all the supported arguments that you can use:

```bash
usage: behave_runner.py [options]

optional arguments:
  -h, --help            show this help message and exit
  --environment {staging,dev,production}
                        ==> Environment to execute the tests (default = staging). Find the app URLs in properties file
  --target {local,lt,bs,cbt}
                        ==> Platform to execute the tests (in browsers: default = local): LT - LambdaTest; BS - BrowserStack; CBT -
                        CrossBrowserTesting
  --mode {web,headless,mobile}
                        ==> Browser execution mode according the platform / OS (default = web)
  --os {MacOS High Sierra,MacOS Catalina,MacOS Big sur,Windows,Windows 10,iOS,Android,}
                        ==> Operational System from the current server
  --os_version {14.3,14.0,14,13.0,13,12.0,12,11.0,11,10.0,10,9.0,9,8.1,8.0,8,7.1,7.0,7,6.0,6,5.0,5,4.4,}
                        ==> Preferably use XX.X for mobile and XX for OS platform versions
  --device_name {local,Google Pixel 4 XL,Google Pixel 4,Google Pixel 3a XL,Google Pixel 3a,Google Pixel 3 XL,Google Pixel 3,Google Pixel 2,Google Pixel,Google Nexus 6,Google Nexus 5,iPhone 12 Pro Max,iPhone 12 Pro,iPhone 12,iPhone 11 Pro Max,iPhone 11 Pro,iPhone 11,iPhone XS Max,iPhone XS,iPhone XR,iPhone X,iPhone 8 Plus,iPhone 8,iPhone 7 Plus,iPhone 7,iPhone 6S Plus,iPhone 6S,iPhone 6,iPhone SE 2020,iPhone SE,iPad,iPad Pro 12.9 2020,iPad Pro 12.9 2018,iPad Pro 11 2020,iPad Mini 2019,iPad Air 2019,iPad 7th,iPad Pro 11 2018,iPad Pro 9.7 2016,iPad Pro 12.9 2017,iPad Mini 4,iPad 6th,iPad 5th,Motorola Moto G7 Play,Motorola Moto X 2nd Gen,Motorola Moto X 2nd Gen,OnePlus 8,OnePlus 7,OnePlus 7T,OnePlus 6T,Samsung Galaxy S20,Samsung Galaxy S20 Plus,Samsung Galaxy S20 Ultra,Samsung Galaxy Note 20 Ultra,Samsung Galaxy Note 20,Samsung Galaxy Note 10 Plus,Samsung Galaxy Note 10,Samsung Galaxy Note 9,Samsung Galaxy Note 8,Samsung Galaxy Note 4,Samsung Galaxy A51,Samsung Galaxy A11,Samsung Galaxy A10,Samsung Galaxy S10e,Samsung Galaxy S10 Plus,Samsung Galaxy S10,Samsung Galaxy S9 Plus,Samsung Galaxy S9,Samsung Galaxy S8 Plus,Samsung Galaxy S8,Samsung Galaxy S7,Samsung Galaxy S6,Samsung Galaxy J7 Prime,Samsung Galaxy Tab S6,Samsung Galaxy Tab S5e,Samsung Galaxy Tab S4,Samsung Galaxy Tab S3,Samsung Galaxy Tab 4,Vivo Y50,Xiaomi Redmi Note 8,Xiaomi Redmi Note 7}
                        ==> The device name models (check the platform version supported in --os_version)
  --browser {chrome,firefox,safari}
                        ==> Browser accessed by web / mobile in desktop executions (default = chrome)
  --browser_version {90.0,89.0,88.0,87.0,86.0,85.0,84.0,83.0,81.0,80.0,78.0,77.0,76.0,13.0,}
                        ==> Browser version from Chrome (80..88) or Firefox (76..78) or Safari (13.0 - MacOS is required)
  --orientation {Landscape,Portrait}
                        ==> Screen orientation for mobile executions (default = Portrait)
  --resolution {1024x768,1280x1024,1600x1200,1920x1080}
                        ==> Resolution allowed for a browser in web execution (default = 1280x1024)
  --tags TAGS           ==> Feature(s) / Scenario(s) to be executed (separate tags by comma and without spaces)
  --exclude {wip,skip,bug,slow,obsolete,}
                        ==> Feature(s) / Scenario(s) to be ignored / skipped from execution using a single tag (recommended: wip)
```

Finally, you can vary the command options such as these samples below and much more. If you does not pass the other arguments, it will be considered the default values:

```bash
     python behave_runner.py --target local
     python behave_runner.py --target local --browser safari --environment production --resolution '1024x768'
     python behave_runner.py --target local --browser chrome --mode headless
     python behave_runner.py --target lt
     python behave_runner.py --target lt --os 'Windows' --os_version '10' --browser chrome
     python behave_runner.py --target lt --mode headless
     python behave_runner.py --target lt --tags demo-web-apw
     python behave_runner.py --target bs --mode mobile --os iOS --os_version '14' --device_name 'iPhone 11'.resources\\mobile_automation\\Sample.ipa'
```

## BDD APROACHING USING PYTHON-BEHAVE

The [Behaviour Driven Development](https://cucumber.io/docs/bdd/) can make our automated tests much more agile, productive, sustainable and with a living-documentation of business. Considering this, in the following sections will be presented a step-by-step about how to implement a simple scenario considering Python-Behave (library backed up by Python code - Cucumber-based) and Selenium to make possible to automate our Gherkin scenarios.

### HOW TO IMPLEMENT TESTS USING PYONUIT?

Considering that the number of tests can increase significantly in this project, it is very important to keep in mind that you also need to have a good and coherent organisation of files, scenarios, features and settings associated to the tests. Initially, to have the codes recognised by Behave framework, all the files related to test cases should be implemented into the `features` folder. Take a look at the recommended structure below.

#### 1. Gherkin Files

All the tests are documented in [Gherkin](https://behave.readthedocs.io/en/latest/tutorial.html#feature-files), a structured and natural language with properly keywords (Given, When, Then) that allows us to write testable specifications. Those files have the format `.feature` and should be organised into the '/features' with subfolders such as ENVIRONMENT FOLDER (dev/staging/production) > DOMAIN FOLDER (global name of a functionality) > FEATURE FILE. For example:

```
    features
    └─── feature_domains
        └─── staging
            └─── authentication
            │    │   login.feature
            │    │   sign_up.feature
            │        ...
            └─── demo_web_shipping.feature
            |        ...
            production
            └─── ...
```

##### 1.1. Create a Feature

With this, you could create a simple scenario that validates if user can search a product at Automation Practice Website. You just need to use the keywords with `Feature:`, `Background`, `Scenario:`, and describe the behaviours for steps with `Given`, `When` and `Then`:

```gherkin
    @demo-web-apw
    Feature: Choosing and sending a product to cart in Automation Practice website
    
        @demo-find-product
        Scenario Outline: The user can search a product and send to the chart
            Given that Automation Practice website is open
            When user types the "<item>" word on search
            Then the product is found after search

            Examples:
                | item   |
                | Blouse |
```

As you could see, add a **tag** (started with @) trying to choose an easy and intuitive name that reminds you about the Feature. Also, you can include another tag above the scenario, if you want to create new scenarios into the same file. This can make easier to call specific scenarios or an entire feature to be executed via Behave command line.

##### 1.2. Generate the Step definitions

After having a scenario defined, make sure that `development_mode` is `false` in `env_settings.properties` if you want to execute the `python3 behave_runner.py --tags demo-find-product` in the terminal (or set `development_mode` to `true` and include the tag `demo-find-product` to property `debug_behave_tags`). Then, copy the snippet definitions generated automatically in console. You will need to implement your steps using them, like these:

```bash
        You can implement step definitions for undefined steps with these snippets:

        @given(u'that Automation Practice website is open')
        def step_impl(context):
            raise NotImplementedError(u'STEP: Given that Automation Practice website is open')


        @when(u'user types the "Blouse" word on search')
        def step_impl(context):
            raise NotImplementedError(u'STEP: When user types the "Blouse" on search')


        @then(u'the product is found after search')
        def step_impl(context):
            raise NotImplementedError(u'STEP: Then the product is found after search')
```

##### 1.3. Create a Step skeleton

Copied the snippets, create a new Python file into the '/features/steps' folder with the same or similar name of your `.feature`.
Try to increment the file name ending with `*_steps.py` and place them in the `steps` folder only (to be read by Behave framework).

```
    features
    └─── steps
        |   demo_apw_checkout_steps.py
        │   demo_apw_product_cart_steps.py
        │   demo_apw_searching_steps.py
            ...
```

Into this new Python file, you should import `behave` library to take the advantages of Behave to your [Step Implementation](https://behave.readthedocs.io/en/latest/tutorial.html#python-step-implementations).

```python
from behave import *

    # Paste your snippets for steps...
```

Then, just paste your snippets from clipboard into the `features/steps/demo_apw_searching_steps.py` and change the `step_impl` names.

```python
from behave import *

@given(u'that Automation Practice website is open')
def step_given_that_automation_practice_is_open(context):
    raise NotImplementedError(u'STEP: Given that Automation Practice website is open')


@when(u'user types the "Blouse" word on search')
def step_when_user_types_the_clothing_name_on_search(context):
    raise NotImplementedError(u'STEP: When user types the "Blouse" on search')


@then(u'the product is found after search')
def step_then_teh_product_is_found_after_search(context):
    raise NotImplementedError(u'STEP: Then the product is found after search')
```

##### 1.4. Page Object Pattern

Now, you have a basic structure using Behave, but the Steps have no code with the significant actions to cover the behaviour expected in the descriptions. To make this possible, all the interactions with HTML pages might be implemented using Selenium web driver, coded in Python. So, it is recommended a design pattern such as [Page Objects](https://martinfowler.com/bliki/PageObject.html) to manage, reuse and store all the locators extracted from a functionality in web or mobile page/screen.

Additionally, considering that you will have many app pages to interact in your scenarios, it is very important to let them organised, distiguished by folders and subfolders as well.

In this case, create a file names ending with `*_page.py` and put them into a folder containing the APP NAME (or a macro app module) > FUNCTIONALITY NAME (or feature name) > PYTHON PAGE OBJECT, like this sample:

```
    features
    └─── pages
        └─── demo_automation_practice_website
            │   home_page.py
            │   modal_cart_page.py
            │   shopping_cart_summary_page.py
                ...
   
```

At the '/features/pages/' folder, create a new page object class that inherits the BasePage module (`from driver_wrappers.selenium.page_wrapper import BasePage`):

```python
from driver_wrappers.selenium.page_wrapper import BasePage
from selenium.webdriver.common.by import By


class HomePage(BasePage):
    # ... declare the locators and Selenium methods here
```

Through BasePage, you can take all advantages from default Selenium web driver (to click, send keys, etc.) and also consume dozen of wrapped methods customised from the most common component actions identified in the application (type text, select a dropdown option, set a datepicker and many other actions):

```python
    self.wait_for_element(by, location, with_text, title, is_visible, is_not_visible, is_clickable, is_selected, is_frame, is_alert, is_presented, typing_secs, handle_timeout)

    self.get_element_by(by_type, element_location)

    self.get_element_text(by_type, element_location, is_visible)

    self.get_value_on_attr(attr_name, by_type, element_location, is_visible)

    self.type_text(input_text, by_type, element_location, letter_by_letter, word_by_word, paste_string, clear_field, is_clickable)

    self.click_on(by_type, element_location, is_visible)

    self.click_by_js(by_type, element_location, is_visible)

    self.perform_click_action(by_type, element_location)

    self.select_dropdown_item(str_option, str_autocomplete, root_by_type, root_selector, xpath_for_root_option, xpath_with_an_option_set)

    self.upload_with_drag_and_drop(path_to_upload, by_type, element_location_to_drop)

    self.pick_a_calendar_date(custom_date)

    self.pick_offset_slider_and_drag_it(position_value_expected, discretization, is_start, is_end, by_type, root_element_location)

    # ... and many others
```

Considering this, extract the element locators inspecting the application's page opened in a browser and place them into the variables from your Page class. But, you will need to import `from selenium.webdriver.common.by import By` into the HomePage, to define a kind of locator for a web element the web driver should be able interpret (By.XPATH, By.CSS_SELECTOR, By.ID, etc.):

```python
from driver_wrappers.selenium import BasePage
from selenium.webdriver.common.by import By


class HomePage(BasePage):
    loc_text_search = (By.ID, "search_query_top")
    loc_button_search = (By.CSS_SELECTOR, '#searchbox button[name="submit_search"]')
    loc_label_product_unit_price = (
        By.CSS_SELECTOR,
        '#center_column ul li div span.product-price[itemprop="price"]',
    )

    def type_input_search(self, value_expected):
        self.type_text(value_expected, *self.loc_text_search)
        return self

    def click_on_search_button(self):
        self.click_on(*self.loc_button_search, is_visible=True)
        return self

    def wait_until_product_name_is_visible(self, product_name=""):
        loc_product_name = self.set_product_name_label(product_name)
        self.wait_for_element(*loc_product_name, is_visible=True)
        return self
```

The locator declared with a tuple (`(By.<TYPE>, "<location string>")`) can be called directly using asterisk before a `self.loc_name`.

Sometimes, the XPATH strings could be longer if has no ID in the HTML elements to be referred. But always try to keep it as simple as possible. As an alternative, the good practice is consider a XPATH or CSS_SELECTOR containing at least the element identifier such as `//*[@id="<elem_id_name>"]` or `[id="<elem_id_name>"]`, respectively. This will ensure tests with a better performance and maintainability, otherwise, you would need to generate longer XPATH strings containing functions to search the content in the DOM tree. Finally, if you are having complications like this last case, notify the development team to introduce an **ID** or **data-testid** in the required HTML element.

###### 1.4.a) Assertions

To create validation methods for the steps when is necessary (mainly in the `@Then` step), you should use the existing assert methods already invoked by _BasePage_. So, you are able to call them directly into the page used by a scenario. Just define the asserts like these:

- `self.assert_that("<FOUND STRING IN PAGE>").is_equals_to("<EXPECTED STRING>", "<OPTIONAL DESCRIPTION>")`
- `self.assert_that("<FOUND STRING IN PAGE>").contains_the("<EXPECTED STRING>", "<OPTIONAL DESCRIPTION>")`
- `self.assert_that("<FOUND STRING IN PAGE>").is_different_from("<EXPECTED STRING>", "<OPTIONAL DESCRIPTION>")`
- `self.assert_that(<FOUND NUMBER IN PAGE>).is_greater_than(b_value=<NUMBER>, "<OPTIONAL DESCRIPTION>")`
- `self.assert_that(<FOUND NUMBER IN PAGE>).is_less_than(b_value=<NUMBER>, "<OPTIONAL DESCRIPTION>")`
- `self.assert_that(<FOUND NUMBER IN PAGE>).is_between_the(expected_min=<NUMBER>, expected_max=<NUMBER>, "<OPTIONAL DESCRIPTION>")`
- `self.assert_that().is_in_pdf("<PDF FILE PATH OR URL>", "<EXPECTED STRING>", "<OPTIONAL DESCRIPTION>")`

Then, you should have a page with an implementation like this:

```python
class SearchResultsPage(BasePage):

    loc_text_search = (By.ID, "search_query_top")
    loc_button_search = (By.CSS_SELECTOR, '#searchbox button[name="submit_search"]')
    loc_label_product_unit_price = (
        By.CSS_SELECTOR,
        '#center_column ul li div span.product-price[itemprop="price"]',
    )

    def type_input_search(self, value_expected):
        self.type_text(value_expected, *self.loc_text_search)
        return self

    def click_on_search_button(self):
        self.click_on(*self.loc_button_search, is_visible=True)
        return self

    def wait_until_product_name_is_visible(self, product_name=""):
        loc_product_name = self.set_product_name_label(product_name)
        self.wait_for_element(*loc_product_name, is_visible=True)
        return self

    def validate_label_product_name(self, value_expected):
        loc_product_name = self.set_product_name_label(value_expected)
        self.scroll_into_view(*loc_product_name)
        product_name_found = self.get_element_text(*loc_product_name)
        self.assert_that(product_name_found).is_equals_to(value_expected)
        return self

    def validate_label_product_unit_price(self, value_expected):
        product_unit_price_found = self.get_element_text(*self.loc_label_product_unit_price)
        self.assert_that(product_unit_price_found).is_equals_to(value_expected)
        return self
```

##### 1.5. Step Implementation

Having all the pages needed already implemented, you need to call the methods to satisfy the scenario behaviour, as well the validations.

```python
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


@then("the product is found after search")
def step_then_teh_product_is_found_after_search(context):
    (
        home_page.wait_until_product_name_is_visible(context.clothing).validate_label_product_name(
            context.clothing
        )
    )
```

And your first test case scenario is ready to be executed for the first time!

## SELECT THE SCENARIOS TO BE EXECUTED

Regardless if you are using the debug mode to execute tests or triggering them via CI server, you should set the tags accordingly declaring with or without `@`, but separating them by comma and without spaces. See these examples:

You can combine TAGS like these examples:

- e.g. 1) ISOLATED SCENARIO: `demo-find-product`

- e.g. 2) COMBINING SCENARIOS: `demo-total-purchase,demo-find-product`

- e.g. 3) CALLING ENTIRE FEATURES: `demo-web-apw`

If you leave the parameter related to tags empty, all the features from the environment selected will be executed regardless if is set by properties or by command line.

## FURTHER INFORMATION ABOUT CI/CD FILES

If you need to manage or maintain the CI/CD files for PyonUIT, just keep in mind about the following structure:

### 1. Provisioning the test environment via Docker

The `Dockerfile` is the first interface tier between PYON and a CI Server. This file is responsible to configure the virtualization process in a node where the PYON runs. Basically, Python and Java should be installed with some boot parameters and a user for a container. This is the minimum needed to make PYON capable to trigger tests in a CI server such as Jenkins.
  
### 2. Handling containers via Docker-Compose

To run the container targeting the `behave_runner.py` and injecting required environment variables used for **LambdaTest** authentication or another tool used to execute the PYON, in this case, you can hadle it via `docker-compose.yml`.

### 3. Customising the build settings in a Jenkinsfile and Groovy

First of all, in the `Jenkinsfile` you all you need to run the tests in a Jenkins pipeline providing the build parameters, scheduling, CLI commands, etc. into then `test_pipeline.groovy`. In turn, the Groovy file `test_pipeline.groovy` aims to concentrate all the details related to a build strategy, as explained below.

#### 3.1. Automatic scheduling

A way to set fixed scheduled triggers for PYON is through a parametrized crontab that makes possible to define the app environment and branch for execution.

```groovy
    def schedule_triggers_by_branch() {
        if (env.BRANCH_NAME == 'master') {
            // STAGING: At minute 0 past hour 12 weekly from Monday through Friday
            return [parameterizedCron('''
                    0 12 * * 1-5 % PYON_ENVIRONMENT=staging
                    ''')]
        }
        return []
    }
```

#### 3.2. Set the parameters for build

You can trigger the tests manually using Jenkins, according the the parameters involved to customise the PYON build. You should see those parameters in 'Jenkins > UI Tests > master > Build with Parameters'.

```groovy
    properties([
        pipelineTriggers(schedule_triggers_by_branch()),
        parameters([
            choice(
                name: 'PYON_ENVIRONMENT',
                choices: 'staging\ndev\nproduction',
                description: '(*) Environment to execute the tests (default = staging). Find the app URLs in properties file \
                                --> <span style="color: blue"><b>Options: staging, dev, production</b>',
                ),
            choice(
                name: 'PYON_TARGET', 
                choices: 'lt\nlocal\nbs', 
                description: '(*) Platform to execute the tests (in browsers: default = local): LT - LambdaTest; BS - BrowserStack; CBT - CrossBrowserTesting \
                                --> <b>Options: local, lt, bs, cbt</b><br/><br/><hr>', 
                ),
            string(
                name: 'PYON_TAGS', 
                defaultValue: '', 
                description: '(*) Feature(s) / Scenario(s) to be executed (separate tags by comma and without spaces)', 
                ),
                ...
```

#### 3.3. Set the credentials to store and access sensitive data

As you know, some passwords and personal data cannot be exposed or accessed easily. Those datas should be encrypted and decrypted by a reliable and safer mechanism. For PYON, that mechanism is by managing the credentials through Jenkins. There are many ways to set credentials, but as the PYON consumes lots of different sensitive variables, then the strategy chosen is access a secret file uploaded and encrypted in 'Jenkins > Credentials > System > Global credentials' (you need to have permission to this page in Jenkins).

```groovy
    withCredentials([file(credentialsId: 'pyon-secret-data', variable: 'PYON_SECRET_FILE')]) {
        sh """
            rm -f $WORKSPACE/pyon_secret_data.properties
            cp $PYON_SECRET_FILE $WORKSPACE
        """
```

The variable `PYON_SECRET_FILE` is encrypted and the file is copied into the current building workspace in execution, containing the following variables:

```properties
    [app-auth]
    PYON_SECRET_APP_USER_NAME = ...
    PYON_SECRET_APP_PASS = ...

    [app-configcat]
    PYON_SECRET_CONFIGCAT_SDK_KEY_FF_DEV = ...
    PYON_SECRET_CONFIGCAT_SDK_KEY_FF_STAGING = ...
    PYON_SECRET_CONFIGCAT_SDK_KEY_FF_PRODUCTION = ...
```

For another safe cases such as authentication in LambdaTest plugin at Jenkins, those credentials already contains a token instead a password, you can access this information via configFileProvider.

#### 3.4. Call the PYON through Docker-Compose command

After having the environment variables settled, it is time to run the test code. Using a bash script encapsulated in `docker-compose`, the PYON can be executed with the requirements updated and reading all the parameters passed by args (recognised by CLI):

```bash
    docker-compose run --rm web \
    bash -c " \
        cp env_settings.properties.local env_settings.properties && \
        python update.py && \
        python behave_runner.py --target ${params.PYON_TARGET} \
                                --environment ${params.PYON_ENVIRONMENT} \
                                --mode ${params.PYON_MODE} \
                                --os '${params.PYON_OS}' \
                                --os_version '${params.PYON_OS_VERSION}' \
                                --device_name '${params.PYON_DEVICE}' \
                                --browser ${params.PYON_BROWSER} \
                                --browser_version '${params.PYON_BROWSER_VERSION}' \
                                --orientation '${params.PYON_ORIENTATION}' \
                                --resolution '${params.PYON_RESOLUTION}' \
                                --tags '${params.PYON_TAGS}' \
                                --exclude '${params.PYON_EXCLUDED_TAG}'
```

#### 3.5. Slack notification

After PYON finishes running the tests, a Slack notification is sent with the current result status (success or failure).

```groovy
    on_failure: {slack_notify(helper, "failure")},
    on_success: {slack_notify(helper, "success")}
```

Besides that, the function `slack_notify()` is responsible to identify the correct Slack channel to report and compile the message with different and specific information related to the current build executed in "master" branch, such as: _upstream project from app where the tests ran, URLs from build, Allure Report URL, LambdaTest video URL, etc._

#### 3.6. Post build actions

After the executions, the PYON presents all the results using [Allure Reports plugin](https://plugins.jenkins.io/allure-jenkins-plugin/). The results are generated into the directory for archiving.

```groovy
    allure_results = "allure-results-${params.PYON_ENVIRONMENT}"
    script {
        allure([
            includeProperties: false, jdk: '', properties: [], reportBuildPolicy: 'ALWAYS',
            results: [[path: allure_results]]
        ])
    }
    publishHTML([
        reportName: 'AllureTestingReport', reportDir: allure_results, reportFiles: 'index.html',
        reportTitles: '', allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false
        ]
    )

    archive "allure-results/**"
```
