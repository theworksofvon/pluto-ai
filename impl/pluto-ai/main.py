import asyncio
from agents import aggregator, twitter_poster
from agency.agency import Agency


async def main():

    agency = Agency([aggregator,twitter_poster])

    resp = await agency.run(starting_prompt="What are all of the actions you can currently do ?")

    print(f"Response from Agency: {resp}")

if __name__ == "__main__":
    asyncio.run(main())
