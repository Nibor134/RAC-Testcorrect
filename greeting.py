import datetime

def get_greeting():
  now = datetime.datetime.now()
  hour = now.hour

  if hour < 12:
    return "Good Morning"
  elif hour < 17:
    return "Good Afternoon"
  else:
    return "Good Evening"
    
greeting = get_greeting()
print(greeting)