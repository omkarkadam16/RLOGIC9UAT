*** Settings ***
Library           SeleniumLibrary
Suite Setup       Open Browser To Login Page
Suite Teardown    Close Browser

*** Variables ***
${URL}            https://win-8tcj8ivog5i:7265/
${BROWSER}        Chrome
${EMAIL}          demo123@gmail.com
${PASSWORD}       Demo@123

*** Test Cases ***
Login With Valid Credentials
    [Documentation]    Open the site and log in with valid credentials.
    Input Text         id:EmailId         ${EMAIL}
    Input Text         id:Password        ${PASSWORD}
    Click Element      id:loginButton
    Sleep              2s
    Page Should Not Contain Element    id:loginButton

*** Keywords ***
Open Browser To Login Page
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Timeout    10s

Close Browser
    Close Browser
