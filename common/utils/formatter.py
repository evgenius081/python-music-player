def number_to_mins_and_secs(value):
    minutes, seconds = divmod(int(value), 60)
    return f"{minutes:2d}:{seconds:02d}"

