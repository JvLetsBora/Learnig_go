import redis
import time
import redis.commands.search.aggregation as aggregations
import redis.commands.search.reducers as reducers
from redis.commands.json.path import Path
from redis.commands.search.field import NumericField, TagField, TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query


class redis_interface():
    def __init__(self, urls_host="localhost") -> None:
        self.engnie = redis.Redis(
        host=urls_host, 
        port=6379, 
        db=0, 
        decode_responses=True,
        )

        self.index = {}
    
    def index_create(self, tag_name, schema):
         self.index[tag_name] = self.engnie.ft(f"idx:{tag_name}")
         print("Gerou o indexador: ",tag_name)
         
         # Essa operação depênde da conexão com o server, ela deve ser executada apenas uma vez.
         self.index[tag_name].create_index(
            schema,
            definition=IndexDefinition(prefix=[f"{tag_name}:"], index_type=IndexType.JSON),
            )
    
    def set_value(self,value, key):
        self.engnie.json().set(f"{key}", Path.root_path(), value)

    def set_values(self, tag_name, values):
        for bid, value in enumerate(values):
            self.engnie.json().set(f"{tag_name}:{bid}", Path.root_path(), value)
    
    def get_value(self, tag_name, query="*") -> dict:
        res = self.index[tag_name].search(Query(f"{query}"))
        return res


    
# r = redis.Redis(
# host="redis", 
# port=6379, 
# db=0, 
# decode_responses=True,
# )



remedios = [
    {
    "brand": "Velorim",
    "model": "Dipirona 30 unidades",
    "description": "Não há mais nem um",
    "urgencia":"media"
    },
    {
        "brand": "Velorim",
        "model": "Dipirona 30 unidades",
        "description": "Não há mais nem um",
         "urgencia":"alta"
    },
    {
        "brand": "Velorim",
        "model": "Dipirona 30 unidades",
        "description": "Não há mais nem um",
         "urgencia":"media"
    }
]

bicycles = [
    {
        "brand": "Bicyk",
        "model": "Hillcraft",
        "price": 1200,
        "description": (
            "Kids want to ride with as little weight as possible."
            " Especially on an incline! They may be at the age "
            'when a 27.5" wheel bike is just too clumsy coming '
            'off a 24" bike. The Hillcraft 26 is just the solution'
            " they need!"
        ),
        "condition": "used",
    },
    {
        "brand": "Nord",
        "model": "Chook air 5",
        "price": 815,
        "description": (
            "The Chook Air 5  gives kids aged six years and older "
            "a durable and uberlight mountain bike for their first"
            " experience on tracks and easy cruising through forests"
            " and fields. The lower  top tube makes it easy to mount"
            " and dismount in any situation, giving your kids greater"
            " safety on the trails."
        ),
        "condition": "used",
    },
    {
        "brand": "Eva",
        "model": "Eva 291",
        "price": 3400,
        "description": (
            "The sister company to Nord, Eva launched in 2005 as the"
            " first and only women-dedicated bicycle brand. Designed"
            " by women for women, allEva bikes are optimized for the"
            " feminine physique using analytics from a body metrics"
            " database. If you like 29ers, try the Eva 291. It's a "
            "brand new bike for 2022.. This full-suspension, "
            "cross-country ride has been designed for velocity. The"
            " 291 has 100mm of front and rear travel, a superlight "
            "aluminum frame and fast-rolling 29-inch wheels. Yippee!"
        ),
        "condition": "used",
    },
    {
        "brand": "Noka Bikes",
        "model": "Kahuna",
        "price": 3200,
        "description": (
            "Whether you want to try your hand at XC racing or are "
            "looking for a lively trail bike that's just as inspiring"
            " on the climbs as it is over rougher ground, the Wilder"
            " is one heck of a bike built specifically for short women."
            " Both the frames and components have been tweaked to "
            "include a women's saddle, different bars and unique "
            "colourway."
        ),
        "condition": "used",
    },
    {
        "brand": "Breakout",
        "model": "XBN 2.1 Alloy",
        "price": 810,
        "description": (
            "The XBN 2.1 Alloy is our entry-level road bike but that's"
            " not to say that it's a basic machine. With an internal "
            "weld aluminium frame, a full carbon fork, and the slick-shifting"
            " Claris gears from Shimano's, this is a bike which doesn't"
            " break the bank and delivers craved performance."
        ),
        "condition": "new",
    },
    {
        "brand": "ScramBikes",
        "model": "WattBike",
        "price": 2300,
        "description": (
            "The WattBike is the best e-bike for people who still feel young"
            " at heart. It has a Bafang 1000W mid-drive system and a 48V"
            " 17.5AH Samsung Lithium-Ion battery, allowing you to ride for"
            " more than 60 miles on one charge. It's great for tackling hilly"
            " terrain or if you just fancy a more leisurely ride. With three"
            " working modes, you can choose between E-bike, assisted bicycle,"
            " and normal bike modes."
        ),
        "condition": "new",
    },
    {
        "brand": "Peaknetic",
        "model": "Secto",
        "price": 430,
        "description": (
            "If you struggle with stiff fingers or a kinked neck or back after"
            " a few minutes on the road, this lightweight, aluminum bike"
            " alleviates those issues and allows you to enjoy the ride. From"
            " the ergonomic grips to the lumbar-supporting seat position, the"
            " Roll Low-Entry offers incredible comfort. The rear-inclined seat"
            " tube facilitates stability by allowing you to put a foot on the"
            " ground to balance at a stop, and the low step-over frame makes it"
            " accessible for all ability and mobility levels. The saddle is"
            " very soft, with a wide back to support your hip joints and a"
            " cutout in the center to redistribute that pressure. Rim brakes"
            " deliver satisfactory braking control, and the wide tires provide"
            " a smooth, stable ride on paved roads and gravel. Rack and fender"
            " mounts facilitate setting up the Roll Low-Entry as your preferred"
            " commuter, and the BMX-like handlebar offers space for mounting a"
            " flashlight, bell, or phone holder."
        ),
        "condition": "new",
    },
    {
        "brand": "nHill",
        "model": "Summit",
        "price": 1200,
        "description": (
            "This budget mountain bike from nHill performs well both on bike"
            " paths and on the trail. The fork with 100mm of travel absorbs"
            " rough terrain. Fat Kenda Booster tires give you grip in corners"
            " and on wet trails. The Shimano Tourney drivetrain offered enough"
            " gears for finding a comfortable pace to ride uphill, and the"
            " Tektro hydraulic disc brakes break smoothly. Whether you want an"
            " affordable bike that you can take to work, but also take trail in"
            " mountains on the weekends or you're just after a stable,"
            " comfortable ride for the bike path, the Summit gives a good value"
            " for money."
        ),
        "condition": "new",
    },
    {
        "model": "ThrillCycle",
        "brand": "BikeShind",
        "price": 815,
        "description": (
            "An artsy,  retro-inspired bicycle that's as functional as it is"
            " pretty: The ThrillCycle steel frame offers a smooth ride. A"
            " 9-speed drivetrain has enough gears for coasting in the city, but"
            " we wouldn't suggest taking it to the mountains. Fenders protect"
            " you from mud, and a rear basket lets you transport groceries,"
            " flowers and books. The ThrillCycle comes with a limited lifetime"
            " warranty, so this little guy will last you long past graduation."
        ),
        "condition": "refurbished",
    },
]

schema = (
    TextField("$.brand", as_name="brand"),
    TextField("$.model", as_name="model"),
    TextField("$.description", as_name="description"),
    NumericField("$.price", as_name="price"),
    TagField("$.condition", as_name="condition"),
)


r = redis_interface(urls_host="redis")

r.index_create("bicycle",schema)
r.index_create("remedios",(
    TextField("$.brand", as_name="brand"),
    TextField("$.model", as_name="model"),
    TextField("$.description", as_name="description"),
    TextField("$.urgencia", as_name="urgencia"),
))

r.set_values(tag_name="bicycle", values=bicycles)
r.set_values(tag_name="remedios", values=remedios)

print("Meu DBUG: ",r.get_value(tag_name="remedios", query="@urgencia:media"))

# index = r.ft("idx:bicycle")

# print("Gerou o index: ",index)

# # Essa operação depênde da conexão com o server, ela deve ser executada apenas uma vez
# index.create_index(
#     schema,
#     definition=IndexDefinition(prefix=["bicycle:"], index_type=IndexType.JSON),
# )



# for bid, bicycle in enumerate(bicycles):
#     r.json().set(f"bicycle:{bid}", Path.root_path(), bicycle)


# res = index.search(Query("*"))
# #print("Documents found:", res.total)


# res = index.search(Query("@model:Jigger"))
# #print(res)

# res = index.search(
#     Query("@model:Jigger").return_field("$.price", as_field="price")
# )
# #print(res)

# # Há como se fazer quarys por qual quer palavra do texto, usando operador [] há como criar um range,
# #E o decorador @ indica uma chave
# res = index.search(Query("@price:[0 1000]"))
# #print(res)

# res = index.search(
#     Query(
#         "@description:%analitics%"
#     ).dialect(  # Note the typo in the word "analytics"
#         2
#     )
# )
# #print(res)


# # res = index.search(Query("mountain").with_scores())
# # for sr in res.docs:
# #     print(f"{sr.id}: score={sr.score}")


# req = aggregations.AggregateRequest("*").group_by(
#     "@condition", reducers.count().alias("count")
# )
# res = index.aggregate(req).rows
# print(res)


