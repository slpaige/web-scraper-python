def select_dates(potential_dates):
    names = {item["name"] for item in potential_dates
             if int(item["age"]) > 30 and item["city"] == "Berlin"
             and "art" in item["hobbies"]}

    return ", ".join(names)
