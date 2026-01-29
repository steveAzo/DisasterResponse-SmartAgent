import spade

class BasicAgent(spade.agent.Agent):
    async def setup(self):
        print(f"Hello World! I'm agent {str(self.jid)}")

async def main():
    agent = BasicAgent("testagent@localhost", "password")
    await agent.start()
    print("Agent started successfully!")
    
    await spade.wait_until_finished(agent)

if __name__ == "__main__":
    spade.run(main())