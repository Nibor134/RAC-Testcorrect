import datetime

def show_time_in_dutch():
  # Get the current time and date
  current_time = datetime.datetime.now()
  
  # Create a dictionary that maps English day names to Dutch day names
  day_names = {
    "Monday": "Maandag",
    "Tuesday": "Dinsdag",
    "Wednesday": "Woensdag",
    "Thursday": "Donderdag",
    "Friday": "Vrijdag",
    "Saturday": "Zaterdag",
    "Sunday": "Zondag"
  }
  
  # Get the current day name in English
  day_name = current_time.strftime("%A")
  
  # Get the corresponding Dutch day name from the dictionary
  dutch_day_name = day_names[day_name]
  
  # Print the current time and date in Dutch
  return (f"Het is nu {dutch_day_name}, {current_time.strftime('%H:%M:%S')}")
   
# Test the function

