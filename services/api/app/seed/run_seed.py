import asyncio

from app.db.session import async_session
from app.models import FoodItem
from app.seed.kenyan_foods import KENYAN_FOODS_SEED

async def seed_kenyan_foods() -> None:
    async with async_session() as db:
        for row in KENYAN_FOODS_SEED:
            db.add(FoodItem(**row))
        await db.commit()
    print(f"seeded {len(KENYAN_FOODS_SEED)} food items")

if __name__ == "__main__":
    asyncio.run(seed_kenyan_foods())