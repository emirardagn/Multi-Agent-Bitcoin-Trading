from bitcointrading.crew import BitcoinTrading


def run():
    
    try:
        BitcoinTrading().crew().kickoff()
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


