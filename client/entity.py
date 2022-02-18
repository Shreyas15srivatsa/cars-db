# abstract class
class Entity:

    # query_opts = {
    #     "limit": int
    # }
    def __init__(self) -> None:
        self.data = {}

    def setAttribute(self, column: str, value: any) -> None:
        self.data[column] = value

    def toString(self):
        res = "++++++++++++++++++++++++++++++++++++++++++++\n"
        for k, v in self.data.items():
            res += f"{k}: {v}\n"
        res += "++++++++++++++++++++++++++++++++++++++++++++\n"
        return res

    def repOk(self):
        pass


class ListingInfo(Entity):
    # 0=fixed value; 1=range, 2=gt .Relevant for CREATE
    # <attribute> : (<type>, <type>)
    # for range, 1 (min) must be followed by 0 (max)
    search_parameters = {
        "make_name": (0, str),
        "model_name": (0, str),
        "year": (0, int),
        "trim_name": (0, str),
        "vin": (0, str),
        "sp_name": (0, str),
        "threshold_seller_rating": (2, str),
        "min_city_fuel_economy": (1, int),
        "max_city_fuel_economy": (0, int),
        "min_highway_fuel_economy": (1, int),
        "max_highway_fuel_economy": (0, int),
        "min_mileage": (1, int),
        "max_mileage": (0, int),
        "min_price": (1, int),
        "max_price": (0, int),
        "threshold_savings_amount": (2, int),
        "listing_color": (0, str),
        "has_accidents": (0, bool),
        "daysonmarket": (0, int),
    }
    # 1= req; 0=opt
    creation_parameters = {
        "sp_id": (1, int),
        "vin": (1, str),
        "make_name": (1, str),
        "model_name": (1, str),
        "year": (1, int),
        "trim_name": (1, str),
        "price": (1, int),
        "description": (0, str),
        "city_fuel_economy": (0, int),
        "highway_fuel_economy": (0, int),
        "mileage": (0, int),
        "savings_amount": (0, int),
        "listing_color": (0, str),
        "has_accidents": (0, bool),
    }
    # val[0] is unused
    # seller_id is used to obtain listing_id first. Then these params are used
    update_parameters = {
        "model_name": (0, str),
        "make_name": (0, str),
        "year": (0, int),
        "trim_name": (0, str),
        "vin": (0, str),
        "description": (0, str),
        "city_fuel_economy": (0, int),
        "highway_fuel_economy": (0, int),
        "mileage": (0, int),
        "price": (0, int),
        "savings_amount": (0, int),
        "listing_color": (0, str),
        "has_accidents": (0, bool),
    }

    deletion_parameters = {"sp_id": (1, int), "listing_id": (1, int)}


class SellerInfo(Entity):
    # 1= won't be updated. Used for lookup only; 0= can be updated. Relevant for CREATE
    update_parameters = {
        "sp_name": (0, str),
        "dealer_zip": (0, str),
        "franchise_dealer": (0, bool),  # bool or int?
    }
