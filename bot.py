ERROR:__main__:Error: Message: 
Stacktrace:
#0 0x59e6db1a101a <unknown>
#1 0x59e6dac40a70 <unknown>
#2 0x59e6dac92907 <unknown>
#3 0x59e6dac92b01 <unknown>
#4 0x59e6dace0d54 <unknown>
#5 0x59e6dacb840d <unknown>
#6 0x59e6dacde14f <unknown>
#7 0x59e6dacb81b3 <unknown>
#8 0x59e6dac8459b <unknown>
#9 0x59e6dac85971 <unknown>
#10 0x59e6db1661eb <unknown>
#11 0x59e6db169f39 <unknown>
#12 0x59e6db14d2c9 <unknown>
#13 0x59e6db16aae8 <unknown>
#14 0x59e6db131baf <unknown>
#15 0x59e6db18e0a8 <unknown>
#16 0x59e6db18e286 <unknown>
#17 0x59e6db19fff6 <unknown>
#18 0x7677fd8b61f5 <unknown>
Stacktrace: Traceback (most recent call last):
  File "/opt/render/project/src/bot.py", line 84, in run_selenium
    search_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Search for a bot')]")))
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/selenium/webdriver/support/wait.py", line 138, in until
    raise TimeoutException(message, screen, stacktrace)
selenium.common.exceptions.TimeoutException: Message: 
Stacktrace:
#0 0x59e6db1a101a <unknown>
#1 0x59e6dac40a70 <unknown>
#2 0x59e6dac92907 <unknown>
#3 0x59e6dac92b01 <unknown>
#4 0x59e6dace0d54 <unknown>
#5 0x59e6dacb840d <unknown>
#6 0x59e6dacde14f <unknown>
#7 0x59e6dacb81b3 <unknown>
#8 0x59e6dac8459b <unknown>
#9 0x59e6dac85971 <unknown>
#10 0x59e6db1661eb <unknown>
#11 0x59e6db169f39 <unknown>
#12 0x59e6db14d2c9 <unknown>
#13 0x59e6db16aae8 <unknown>
#14 0x59e6db131baf <unknown>
#15 0x59e6db18e0a8 <unknown>
#16 0x59e6db18e286 <unknown>
#17 0x59e6db19fff6 <unknown>
#18 0x7677fd8b61f5 <unknown>
