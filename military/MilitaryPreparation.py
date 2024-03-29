from sc2.constants import PYLON, GATEWAY, CYBERNETICSCORE, STALKER, STARGATE, VOIDRAY

from model.ModuleModel import ModuleModel


# MilitaryPreparation management
class MilitaryPreparation(ModuleModel):
    def __init__(self):
        super().__init__()
        self.MAX_WORKERS = 65
        
    async def condition(self, bot):
        pass
        
    async def run(self, bot):
        await self.offensive_force_buildings(bot)
        await self.build_offensive_force(bot)

# Build offensive force buildings (GATEWAY, CYBERNETICSCORE, STARGATE sc2.constants)
    async def offensive_force_buildings(self, bot):
        if bot.units(PYLON).ready.exists:
            # Get a random pylon
            pylon = bot.units(PYLON).ready.random
            # Build a Cybernetics Core
            if bot.units(GATEWAY).ready.exists and not bot.units(CYBERNETICSCORE):
                if bot.can_afford(CYBERNETICSCORE) and not bot.already_pending(CYBERNETICSCORE):
                    await bot.build(CYBERNETICSCORE, near=pylon)
            # Build a Gateway
            elif len(bot.units(GATEWAY)) < (bot.get_time_iteration()/2):
                if bot.can_afford(GATEWAY) and not bot.already_pending(GATEWAY):
                    await bot.build(GATEWAY, near=pylon)
            # Build a Stargate
            if bot.units(CYBERNETICSCORE).ready.exists:
                if len(bot.units(STARGATE)) < bot.get_time_iteration():
                    if bot.can_afford(STARGATE) and not bot.already_pending(STARGATE):
                        await bot.build(STARGATE, near=pylon)

    # Build offensive army (STALKER, VOIDRAY sc2.constants)
    async def build_offensive_force(self, bot):
        # Gateway
        for gateway in bot.units(GATEWAY).ready:
            # Train stalker
            if not bot.units(STALKER).amount > bot.units(VOIDRAY).amount:
                if bot.can_afford(STALKER) and bot.supply_left > 0:
                    await bot.do(gateway.train(STALKER))
        # Stargate
        for stargate in bot.units(STARGATE).ready:
            # Train voidray
            if bot.can_afford(VOIDRAY) and bot.supply_left > 0:
                await bot.do(stargate.train(VOIDRAY))
