"""
@authors: Shreyas Srivatsa <shreyas.srivatsa@uwaterloo.ca>, Iram Rahman <i5rahman@uwaterloo.ca>
@about: A simple python script that uses Pandas to sanitize and generate our own CSVs for the 10 Gig Cars dataset
@course: ECE356 Fall 2021
"""
import pandas as pd


def generate_trim_info():
    """Helper to generate the trim info"""
    # 8 attributes - seller
    data = pd.read_csv("used_cars_data.csv", nrows=1000000, sep=',', index_col=False, dtype='unicode',
                       usecols=['trimId', 'trim_name']).drop_duplicates(subset='trimId', keep='first').reset_index()
    data2 = data[['trimId', 'trim_name']]

    # remove those that have trimId as null
    data2 = data2[data2['trimId'].notna()]

    data2['trimId'] = data2['trimId'].str.strip(r't(\d)*').astype(int)

    # round off data
    data2.to_csv('trim_data.csv', index=False)
    print("Done trim info")


def generate_make_info():
    """Helper to generate the make info"""
    # 8 attributes - seller
    data = pd.read_csv("used_cars_data.csv", nrows=3000000, sep=',', index_col=False, dtype='unicode',
                       usecols=['make_name']).drop_duplicates(subset='make_name', keep='first').reset_index()
    data2 = data[['make_name']]

    # remove those that have trimId as null
    data2 = data2[data2['make_name'].notna()]

    # round off data
    data2.to_csv('make_data.csv', index=False)
    print("Done make info")


def generate_seller_info():
    """Helper to generate the seller info"""
    # 8 attributes - seller
    data = pd.read_csv("used_cars_data.csv", nrows=1000000, sep=',', index_col=False, dtype='unicode',
                       usecols=['sp_id', 'sp_name', 'seller_rating', 'dealer_zip', 'longitude', 'latitude', 'city',
                                'franchise_dealer']).drop_duplicates(subset='sp_id', keep='first').reset_index()
    data2 = data[['sp_id', 'sp_name', 'seller_rating', 'dealer_zip', 'longitude', 'latitude', 'city',
                  'franchise_dealer']]

    # remove those that have sp_id as null
    data2 = data2[data2['sp_id'].notna()]

    # some of the sp_ids have a decimal. Why you ask? I ask the same.
    data2['sp_id'] = data2['sp_id'].astype(float).astype(int)
    data2 = data2.drop_duplicates(subset='sp_id', keep='first')

    # convert True/False to their SQL representation
    data2['franchise_dealer'] = data2['franchise_dealer'].str.replace('True', '1')
    data2['franchise_dealer'] = data2['franchise_dealer'].str.replace('False', '0')
    data2['franchise_dealer'] = data2['franchise_dealer'].fillna('0')

    # round off data
    data2['seller_rating'] = data2['seller_rating'].apply(lambda x: round(float(x), 2))
    data2.to_csv('seller_data.csv', index=False)
    print("Done seller info")


def generate_listing_info():
    """Helper to generate the listing info"""
    # 14 attributes - listing
    data = pd.read_csv("used_cars_data.csv", nrows=500000, sep=',', keep_default_na=False, index_col=False,
                       dtype='unicode',
                       usecols=['model_name', 'make_name', 'year', 'vin', 'description',
                                'city_fuel_economy', 'sp_id',
                                'highway_fuel_economy', 'listed_date', 'mileage', 'price', 'savings_amount',
                                'listing_color', 'has_accidents', 'daysonmarket', 'trim_name']).drop_duplicates(
        keep='first').reset_index()
    data2 = data[['model_name', 'make_name', 'year', 'trim_name', 'vin', 'sp_id', 'description', 'city_fuel_economy',
                  'highway_fuel_economy', 'listed_date', 'mileage', 'price', 'savings_amount', 'listing_color',
                  'has_accidents', 'daysonmarket']]

    # remove those that have sp_id as null
    data2 = data2[data2['sp_id'].notna()]

    # we want to default to 'Base' for the trim_name in case it's missing
    # it's used in the FK
    data2['trim_name'] = data2['trim_name'].str.replace(r'^\s*$', 'Base', regex=True)
    data2['trim_name'] = data2['trim_name'].fillna('Base')

    # convert True/False to their SQL representation
    data2['has_accidents'] = data2['has_accidents'].str.replace('True', '1')
    data2['has_accidents'] = data2['has_accidents'].str.replace('False', '0')
    data2['has_accidents'] = data2['has_accidents'].fillna('0')

    data2.to_csv('listing_data.csv', index=False)
    print("Done listing info")


def read_data():
    """Helper to read the csv for car data"""
    data = pd.read_csv("used_cars_data.csv", nrows=1000000, sep=',', index_col=False, dtype='unicode',
                       usecols=['model_name', 'make_name', 'year', 'height', 'width', 'length', 'torque', 'horsepower',
                                'exterior_color', 'interior_color', 'body_type',
                                'fuel_type', 'is_new', 'maximum_seating',
                                'back_legroom', 'front_legroom', 'transmission', 'transmission_display',
                                'wheel_system', 'wheel_system_display', 'wheelbase', 'power',
                                'trim_name', 'engine_type', 'fuel_tank_volume', 'engine_displacement',
                                'bed_length']).drop_duplicates(
        keep='first').reset_index()

    return data[['make_name', 'model_name', 'year', 'trim_name', 'height', 'width', 'length', 'torque',
                 'exterior_color', 'interior_color', 'body_type',
                 'fuel_type', 'is_new', 'maximum_seating',
                 'back_legroom', 'front_legroom', 'transmission', 'transmission_display',
                 'wheel_system', 'wheel_system_display', 'wheelbase', 'power', 'horsepower', 'engine_type',
                 'fuel_tank_volume', 'engine_displacement', 'bed_length']]


def generate_car_info():
    """Helper to generate the car info"""
    # 25 attributes - car
    data2 = read_data()

    # sanitize data
    # we want to default to 'Base' for the trim_name in case it's missing
    # note that we cannot leave it as NULL since trim_name is used in the PK
    data2['trim_name'] = data2['trim_name'].str.replace(r'^\s*$', 'Base', regex=True)
    data2['trim_name'] = data2['trim_name'].fillna('Base')

    # remove '--'
    data2['back_legroom'] = data2['back_legroom'].str.replace('--', '')
    data2['front_legroom'] = data2['front_legroom'].str.replace('--', '')
    data2['fuel_tank_volume'] = data2['fuel_tank_volume'].str.replace('--', '')
    data2['height'] = data2['height'].str.replace('--', '')
    data2['width'] = data2['width'].str.replace('--', '')
    data2['wheelbase'] = data2['wheelbase'].str.replace('--', '')
    data2['maximum_seating'] = data2['maximum_seating'].str.replace('--', '')

    data2["power"] = data2["power"].str.replace(",", "").astype("str")
    data2["power"] = data2["power"].apply(lambda x: [int(i) for i in x.split() if i.isdigit()])
    data2["power"] = [x if len(x) == 2 else [0, 0] for x in data2["power"]]
    data2["power_rpm"] = [x[1] for x in data2["power"]]

    data2["torque"] = data2["torque"].str.replace(",", "").astype("str")
    data2["torque"] = data2["torque"].apply(lambda x: [int(i) for i in x.split() if i.isdigit()])
    data2["torque"] = [x if len(x) == 2 else [0, 0] for x in data2["torque"]]
    data2["torque_rpm"] = [x[1] for x in data2["torque"]]
    data2["torque_force"] = [x[0] for x in data2["torque"]]

    data2["torque_rpm"] = data2["torque_rpm"].astype(int)
    data2["torque_force"] = data2["torque_force"].astype(int)
    data2["power_rpm"] = data2["power_rpm"].astype(int)

    # convert True/False to their SQL representation
    data2['is_new'] = data2['is_new'].str.replace('True', '1')
    data2['is_new'] = data2['is_new'].str.replace('False', '0')
    data2['is_new'] = data2['is_new'].fillna('0')

    data2.drop('torque', axis=1, inplace=True)
    data2.drop('power', axis=1, inplace=True)

    data2.to_csv('tmp_car_data.csv', index=False)


def generate_non_electric_info():
    """Helper to generate the non-electric car info"""
    data = pd.read_csv("tmp_car_data.csv", nrows=1000000, sep=',', index_col=False, dtype='unicode',
                       usecols=['make_name', 'model_name', 'year', 'trim_name', 'engine_displacement', 'engine_type',
                                'fuel_tank_volume', 'fuel_type']).drop_duplicates(keep='first').reset_index()
    data2 = data[
        ['make_name', 'model_name', 'year', 'trim_name', 'engine_type', 'fuel_tank_volume', 'engine_displacement',
         'fuel_type']]

    data2 = data2[data2['fuel_type'] != 'Electric']

    data2.drop('fuel_type', axis=1, inplace=True)

    data2.to_csv('car_non_electric_data.csv', index=False)
    print("Done non-electric car info")


def generate_pickup_truck_info():
    """Helper to generate the pickup truck info"""
    data = pd.read_csv("tmp_car_data.csv", nrows=1000000, sep=',', index_col=False, dtype='unicode',
                       usecols=['make_name', 'model_name', 'year', 'trim_name', 'bed_length',
                                'body_type']).drop_duplicates(keep='first').reset_index()
    data2 = data[['make_name', 'model_name', 'year', 'trim_name', 'bed_length', 'body_type']]

    data2 = data2[data2['body_type'] == 'Pickup Truck']

    data2.drop('body_type', axis=1, inplace=True)

    data2.to_csv('car_pickup_truck_data.csv', index=False)
    print("Done car pickup truck info")


def generate_final_car_info():
    data = pd.read_csv("tmp_car_data.csv", nrows=1000000, sep=',', index_col=False, dtype='unicode',
                       usecols=['make_name', 'model_name', 'year', 'trim_name', 'height', 'width', 'length',
                                'exterior_color', 'interior_color', 'body_type',
                                'fuel_type', 'is_new', 'maximum_seating',
                                'back_legroom', 'front_legroom', 'transmission', 'transmission_display',
                                'wheel_system', 'wheel_system_display', 'wheelbase', 'horsepower', 'power_rpm',
                                'torque_rpm', 'torque_force']).drop_duplicates(
        keep='first').reset_index()

    data2 = data[['make_name', 'model_name', 'year', 'trim_name', 'height', 'width', 'length',
                  'exterior_color', 'interior_color', 'body_type',
                  'fuel_type', 'is_new', 'maximum_seating',
                  'back_legroom', 'front_legroom', 'transmission', 'transmission_display',
                  'wheel_system', 'wheel_system_display', 'wheelbase', 'horsepower', 'power_rpm', 'torque_rpm',
                  'torque_force']]

    data2.to_csv('car_data.csv', index=False)
    print("Done car info")


if __name__ == '__main__':
    # generate_trim_info()
    generate_make_info()
    generate_seller_info()
    generate_listing_info()
    generate_car_info()
    generate_non_electric_info()
    generate_final_car_info()
    generate_pickup_truck_info()
