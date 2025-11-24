import pandas as pd

data = [
    ["Afghanistan", "Asia", 652230, 25500100, 20343000000],
    ["Albania", "Europe", 28748, 2831741, 12960000000],
    ["Algeria", "Africa", 2381741, 37100000, 188681000000],
    ["Andorra", "Europe", 468, 78115, 3712000000],
    ["Angola", "Africa", 1246700, 20609294, 100990000000],
]
world = pd.DataFrame(
    data, columns=["name", "continent", "area", "population", "gdp"]
).astype(
    {
        "name": "object",
        "continent": "object",
        "area": "Int64",
        "population": "Int64",
        "gdp": "Int64",
    }
)


# Need to find area >= 3,000,000 or population >= 25,000,000.
# Need to format result in name, population, area order.
def big_countries(world: pd.DataFrame) -> pd.DataFrame:

    world = world.drop(["continent", "gdp"], axis=1)
    big_countries = world[
        (world["area"] >= 3000000) | (world["population"] >= 25000000)
    ]

    return big_countries[["name", "population", "area"]]
