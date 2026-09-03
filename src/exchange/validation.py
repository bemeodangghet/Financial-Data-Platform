def validate_exchange_response(data: dict) -> None:
  

    if not isinstance(data, dict):
        raise TypeError("API response must be a dictionary.")

    if "base_code" not in data:
        raise ValueError("Missing 'base_code' field.")

    if "rates" not in data:
        raise ValueError("Missing 'rates' field.")

    if not isinstance(data["rates"], dict):
        raise ValueError("'rates' must be a dictionary.")

    if not data["rates"]:
        raise ValueError("'rates' dictionary is empty.")