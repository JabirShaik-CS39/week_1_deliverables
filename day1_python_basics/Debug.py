#6. debugging using print/logging

##using print

def add(a,b):
    print("a =", a) #this is debugging using print statement
    print("b =", b)
    print("expected  a + b =", a+b)
    return a-b #this is intentional

result = add(10,5)
print(result) #expected is 15 , but will get 5

##using logging


import logging
logging.basicConfig(level=logging.DEBUG)  #if level is not provided ; then default will be warning
def divide(a,b):
    logging.info(f"a = {a} , b = {b}")
    
    if b == 0:
        logging.error("cannot didive with zero")
        return None
    else:
        result = a / b
        logging.info(f"{a} / {b} = {result}")
        return result

result = divide(10,0)
print(result)

logging.debug("Debug: checking variables")
logging.info("Info: program started")
logging.warning("Warning: low disk space")
logging.error("Error: file missing")
logging.critical("Critical: system failure")

#7. understanding errors & stack traces  
### the below error is intentional only to understand the stack trace``
logging.basicConfig(level=logging.ERROR)

try:
    10 / 0
except Exception as e:
    logging.error("Error occurred", exc_info=True) #exc_info=True will print the stack trace