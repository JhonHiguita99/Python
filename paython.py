from anticaptchaofficial.recaptchav2proxyless import *
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import os

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

url = "https://www.google.com/recaptcha/api2/demo"
page = driver.get(url)

time.sleep(10)

sitekey = driver.find_element(By.XPATH, '//*[@id="recaptcha-demo"]').get_attribute('outerHTML')
sitekey_clean = sitekey.split('" data-callback')[0].split('data-sitekey="')[1]
print(sitekey_clean)

solver = recaptchaV2Proxyless()
solver.set_verbose(1)
solver.set_key("615f427a4171fd8e45fade84c82cd848")
solver.set_website_url(url)
solver.set_website_key(sitekey_clean)

g_response = solver.solve_and_return_solution()
if g_response != 0:
    print("g_response: " + str(g_response))
else:
    print("task finished with error " + str(solver.error_code))

# Mostrar el elemento del captcha (si estaba oculto)
driver.execute_script('var element = document.getElementById("g-recaptcha-response"); element.style.display="";')

# Asignar la respuesta al elemento
driver.execute_script(
    'document.getElementById("g-recaptcha-response").innerHTML = arguments[0];',
    g_response
)

# Ocultar el elemento nuevamente
driver.execute_script('var element = document.getElementById("g-recaptcha-response"); element.style.display="none";')

# Hacer clic en el botón de envío
driver.find_element(By.XPATH, '//*[@id="recaptcha-demo-submit"]').click()

# Esperar 20 segundos
time.sleep(20)