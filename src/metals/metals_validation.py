def validate_metals_response(data: list[dict]) -> None:
    # Validate the whole API response
    if not isinstance(data, list):
        raise TypeError("API response must be a list.")

    if not data:
        raise ValueError("API response is empty.")

    required_fields = [
        "currency",
        "exchangeRate",
        "name",
        "price",
        "symbol",
        "updatedAt",
    ]

    # Validate each metal response
    for metal in data:
        if not isinstance(metal, dict):
            raise TypeError("Each metal response must be a dictionary.")

        # Check required fields
        for field in required_fields:
            if field not in metal:
                raise ValueError(
                    f"Missing required field '{field}' "
                    f"for metal {metal.get('symbol', 'UNKNOWN')}."
                )

        # Validate price
        if not isinstance(metal["price"], (int, float)):
            raise TypeError(
                f"Price for {metal['symbol']} must be numeric."
            )

        if metal["price"] <= 0:
            raise ValueError(
                f"Price for {metal['symbol']} must be greater than 0."
            )

        # Validate exchange rate
        if not isinstance(metal["exchangeRate"], (int, float)):
            raise TypeError(
                f"Exchange rate for {metal['symbol']} must be numeric."
            )

        if metal["exchangeRate"] <= 0:
            raise ValueError(
                f"Exchange rate for {metal['symbol']} must be greater than 0."
            )