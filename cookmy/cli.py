import argparse


def parse_args(args=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Search for recipes by ingredients.")
    parser.add_argument(
        "-i",
        "--ingredients",
        type=str,
        nargs="+",
        required=True,
        help="List of ingredients to search for, separated by commas (e.g., 'chicken, rice')",
    )
    parser.add_argument(
        "-n",
        "--number",
        type=int,
        default=5,
        help="Number of recipes to return (default: 5).",
    )
    return parser.parse_args(args)
