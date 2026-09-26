from exchange.pipeline import run_exchange_pipeline
from metals.pipeline import run_metals_pipeline


def main() -> None:
    run_exchange_pipeline()
    run_metals_pipeline()


if __name__ == "__main__":
    main()

