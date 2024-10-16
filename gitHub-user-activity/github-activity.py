import argparse

import requests  # type: ignore

parser = argparse.ArgumentParser(description="GitHub Activity")
parser.add_argument("username", help="Your GitHub username")


args = parser.parse_args()


url: str = f"https://api.github.com/users/{args.username}/events"


def main() -> None:
    print(f"Querying information for user {args.username} on GitHub...")

    try:
        response = requests.get(url)
        response.raise_for_status()
        if events := response.json():
            print(f"Eventos recientes del usuario {args.username}:\n")
            for i, event in enumerate(events[:5], 1):
                event_type = event.get("type", "Event type not available")
                repo = event.get("repo", {}).get("name", "Repository not available")
                date = event.get("created_at", "Date not available")
                print(f"{i}. Type: {event_type}\n Repository: {repo}\n Date: {date}\n")
        else:
            print(f"The user {args.username} has no recent events.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the user events: {e}")


if __name__ == "__main__":
    main()
