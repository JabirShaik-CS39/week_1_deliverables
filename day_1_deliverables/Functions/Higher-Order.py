# map() applies the lambda function to every item in the list
prices_in_usd = [10, 20, 30, 40]
prices_doubled = list(map(lambda x: x * 2, prices_in_usd))
print(prices_doubled) 

# filter() keeps only the items that evaluate to True
ages = [14, 21, 16, 32, 18, 45]
adults = list(filter(lambda age: age >= 18, ages))
print(adults)  