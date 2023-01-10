import datetime

def get_greeting():
  now = datetime.datetime.now()
  hour = now.hour

  if hour < 12:
    return "Goedemorgen"
  elif hour < 17:
    return "Goedemiddag"
  else:
    return "Goedeavond"

greeting = get_greeting()
