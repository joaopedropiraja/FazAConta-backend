"""
This is a simple demo file to show you how to use beanie and how
it can help us represent our data in a structured and searchable way.
"""

from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from beanie import Document, WriteRules, init_beanie, BackLink, Link
from motor.motor_asyncio import AsyncIOMotorClient


# We should probably come up with a better name than 'collection'
# given its actual meaning within the context of MongoDB, but for
# now this is ok.
#
# A Collection is a group of documents that are linked together.
# One could imagine a DR1 collection, a DR2 collection, etc. These
# collections could be marked as Public or Private, and are a potentially
# easy way to manage data releases and access.
class Collection(Document):
    name: str
    description: str

    class Settings:
        is_root = True


# Sub-classes of Collection are used to manage the actual 'collections',
# in this case a generic collection of maps. An instance of a map collection would
# be something like DailyLATMaps, DailySATMaps, etc. and can be as coarse-
# grained or fine-grained as we want.
class MapCollection(Collection):
    maps: BackLink["Map"] = Field(original_field="collections")


# As well as 'real' data, we can store things like software packages in
# the database. These can be linked to by other documents.
class SoftwarePackage(Document):
    name: str
    version: str

    class Settings:
        is_root = True


# The map maker is a specific software package that we really care about.
# Each map maker release should be catalogued in the software, and maps
# created by it tagged.
class MapMaker(SoftwarePackage):
    python_version: str
    maps: list[BackLink["Map"]] = Field(original_field="map_maker")


# The top-level map document. This is the metadata for the underlying
# data product. Note that it contains links to which map maker was used,
# as well as any map collections.
class Map(Document):
    name: str
    description: str
    xpix: int
    ypix: int
    map_maker: Link[MapMaker]
    collections: list[Link[MapCollection]]


class BaseDocument(Document):
    id: UUID = Field(default_factory=uuid4)


class UserDocument(BaseDocument):
    name: str
    # nickname: str
    # password: str
    # phone_number: str

    class Settings:
        name = "users"


class MemberDocument(BaseDocument):
    user: Link[UserDocument]
    balance: float

    class Settings:
        name = "members"


class GroupDocument(BaseDocument):
    title: str
    members: list[Link[MemberDocument]]

    class Settings:
        name = "groups"


async def get_client():
    client = AsyncIOMotorClient(
        "mongodb://localhost:27017", uuidRepresentation="standard"
    )

    await init_beanie(
        database=client.db_name,
        document_models=[
            GroupDocument,
            UserDocument,
            MemberDocument,
        ],
    )

    return client


async def initialize():
    """
    Create some data in the database for future searching.
    """

    await get_client()

    user = UserDocument(name="João")
    await user.insert()

    member = MemberDocument(user=user, balance=0.0)
    # await member.insert()

    group = GroupDocument(title="Bebidas", members=[member])
    await group.insert(link_rule=WriteRules.WRITE)

    # doc = await GroupDocument.get(
    #     "3ffce8f8-13c0-47e8-9099-79871ae0df5d", fetch_links=True
    # )
    # if doc is None:
    #     return

    # doc.members[0].user.name = "Gabi"
    # await doc.save(link_rule=WriteRules.WRITE)
    # print(doc)
    # # Create an example collection.
    # core_collection = MapCollection(
    #     name="Core Collection", description="This is the core collection of maps"
    # )

    # await core_collection.insert()

    # # The maps we are about to generate will be made with version
    # # one of the map maker.
    # map_maker = MapMaker(name="Map Maker", version="1.0", python_version="3.9")

    # await map_maker.insert()

    # # Create five new maps
    # maps = [
    #     Map(
    #         name=f"Map {map_id}",
    #         description=f"This is map {map_id}",
    #         xpix=1000,
    #         ypix=1000,
    #         map_maker=map_maker,
    #         collections=[core_collection],
    #     )
    #     for map_id in range(5)
    # ]

    # await Map.insert_many(maps)

    # # Ok, now rev map maper version by creating a new entry.
    # new_map_maker = MapMaker(name="Map Maker", version="1.1", python_version="3.10")

    # await new_map_maker.insert()

    # # Create some new maps!
    # new_maps = [
    #     Map(
    #         name=f"New Map {map_id}",
    #         description=f"This is map {map_id}",
    #         xpix=1000,
    #         ypix=1000,
    #         map_maker=new_map_maker,
    #         collections=[core_collection],
    #     )
    #     for map_id in range(5, 10)
    # ]

    # await Map.insert_many(new_maps)


async def get_maps():
    """
    This query function shows various ways we can select and slice
    linked data. In this case, we are creating a query that selects
    maps that were generated by a specific version of the map maker.
    An example use case for this is marking maps generated by a buggy
    software version as invalid.
    """

    await get_client()

    # # Query all maps
    # maps = await Map.find().to_list()

    # print("-- Begin all maps --")
    # for map in maps:
    #     map_maker = await map.map_maker.fetch()
    #     print(map.name + " map maker version: " + map_maker.version)
    # print("-- End all maps --")

    # # Query the backward links.
    # map_maker = await MapMaker.find_one(MapMaker.version == "1.1", fetch_links=True)

    # print("-- Begin backward links --")
    # for map in map_maker.maps:
    #     print(map.name)
    # print("-- End backward links --")

    # # Query the forward links
    # maps = await Map.find(Map.map_maker.version == "1.1", fetch_links=True).to_list()

    # print("-- Begin forward links --")
    # for map in maps:
    #     print(map.name)
    # print("-- End forward links --")


if __name__ == "__main__":
    import asyncio

    asyncio.run(initialize())
    asyncio.run(get_maps())
