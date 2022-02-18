from enum import Enum
import entity as ent
from db import DB


class DBAction(Enum):
    MostPopularCars = 1
    MostPopularCarBrands = 2
    CheapestCars = 3
    HighestRatedSellers = 4
    TopDeals = 5
    ReturnToHomeScreen = 6
    ExitProgram = 7


functionalities = {
    "1": ("Top 5 Most Popular Cars", ent.ListingInfo, DBAction.MostPopularCars),
    "2": (
        "Top 5 Most Popular Cars Brands",
        ent.ListingInfo,
        DBAction.MostPopularCarBrands,
    ),
    "3": ("Top 5 Cheapest Cars", ent.ListingInfo, DBAction.CheapestCars),
    "4": ("Top 5 Highest Rated Sellers", None, DBAction.HighestRatedSellers),
    "5": ("Top 5 deals", None, DBAction.TopDeals),
    "6": ("Return to Home Screen", None, DBAction.ReturnToHomeScreen),
    "7": ("Exit Program", None, DBAction.ExitProgram),
}


def printRecords(records: list) -> None:
    print("\nResult:\n")
    for i, r in enumerate(records):
        print(i, r)
        if i == 0:
            print("------------------------------------------------------------")
    print(f"\nShowing all {len(records)-1} records.\n")


def loop(db: DB) -> None:
    while True:
        prompt_msg = "\n".join([f"{k}: {v[0]}" for k, v in functionalities.items()])
        opt_num = input(f"\nChoose option below:\n{prompt_msg}\n\n")

        if opt_num not in functionalities.keys():
            print("ERROR: Invalid option. Try again.")
            continue

        functionality = functionalities[opt_num]
        entity = functionality[1]

        if int(opt_num) == DBAction.MostPopularCars.value:
            cols = ["make_name", "model_name", "year", "trim_name", "no_of_listings"]
            query = """
            SELECT make_name, model_name, year, trim_name, COUNT(*) AS popular_cars 
            FROM ListingInfo INNER JOIN MakeInfo USING (make_id) 
            GROUP BY make_name, model_name, year, trim_name 
            ORDER BY popular_cars 
            DESC LIMIT 5;
            """
            res = db.runPredefinedReadQuery(cols, query)
            printRecords(res)
        elif int(opt_num) == DBAction.MostPopularCarBrands.value:
            cols = ["make_name", "no_of_listings"]
            query = """
            SELECT make_name, COUNT(make_name) AS popularity 
            FROM ListingInfo INNER JOIN MakeInfo USING (make_id) 
            GROUP BY make_name 
            ORDER BY popularity DESC 
            LIMIT 5;
            """
            res = db.runPredefinedReadQuery(cols, query)
            printRecords(res)
        elif int(opt_num) == DBAction.CheapestCars.value:
            cols = ["make_name", "model_name", "year", "trim_name", "price"]
            query = """
            SELECT make_name, model_name, year, trim_name, min(price) AS cheapest 
            FROM ListingInfo INNER JOIN MakeInfo USING (make_id) 
            GROUP BY listing_id 
            HAVING cheapest != 0 
            ORDER BY cheapest 
            LIMIT 5;
            """
            res = db.runPredefinedReadQuery(cols, query)
            printRecords(res)
        elif int(opt_num) == DBAction.HighestRatedSellers.value:
            cols = ["seller_name", "rating", "dealer_zip", "city"]
            query = """
            SELECT sp_name, max(seller_rating) AS rating, dealer_zip, city 
            FROM SellerInfo 
            GROUP BY sp_id 
            ORDER BY rating 
            DESC LIMIT 5;
            """
            res = db.runPredefinedReadQuery(cols, query)
            printRecords(res)
        elif int(opt_num) == DBAction.TopDeals.value:
            cols = ["make_name", "model_name", "year", "trim_name", "max_savings"]
            query = """
            SELECT make_name, model_name, year, trim_name, max(savings_amount) AS max_savings 
            FROM ListingInfo INNER JOIN MakeInfo USING (make_id) 
            GROUP BY listing_id 
            ORDER BY max_savings DESC 
            LIMIT 5;
            """
            res = db.runPredefinedReadQuery(cols, query)
            printRecords(res)
        elif int(opt_num) == DBAction.ReturnToHomeScreen.value:
            print("\nReturning to Homescreen.\n")
            break
        else:  # Exit
            db.cursor.close()
            db.cnx.close()
            raise SystemExit("\nProgram exited by user. Goodbye!")
