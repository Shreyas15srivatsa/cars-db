-- @authors: Shreyas Srivatsa <shreyas.srivatsa@uwaterloo.ca>, Iram Rahman <i5rahman@uwaterloo.ca>
-- @about: A simple SQL script to create the tables and load them using data from the CSVs
-- @course: ECE356 Fall 2021


SELECT '---------------------------------------------------------------------------------------' AS '';

SELECT 'Create MakeInfo' AS '';

CREATE TABLE MakeInfo (
    make_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    make_name varchar(255)
);


SELECT 'Load MakeInfo' AS '';

load data infile '/var/lib/mysql-files/Group6/make_data.csv' ignore into table MakeInfo
    fields terminated by ','
    enclosed by '"'
    lines terminated by '\n'
    ignore 1 lines
    (@make_name)
    SET make_id = NULL,
    make_name = IF(@make_name = '', NULL, UPPER(@make_name));


SELECT 'Add Index on MakeInfo' AS '';

CREATE INDEX idx_make_info on MakeInfo(make_name);


SELECT '---------------------------------------------------------------------------------------' AS '';

SELECT 'Create SellerInfo' AS '';

CREATE TABLE SellerInfo (
    sp_id int PRIMARY KEY, 
    sp_name varchar(255),
    seller_rating decimal(3,2),
    dealer_zip varchar(20),
    longitude decimal(9,6),
    latitude decimal(8,6), 
    city varchar(40),
    franchise_dealer bool not null default 0,
    CHECK(seller_rating >= 0.00),
    CHECK(seller_rating <= 5.00)
);


SELECT 'Load SellerInfo' AS '';

load data infile '/var/lib/mysql-files/Group6/seller_data.csv' ignore into table SellerInfo
    fields terminated by ','
    enclosed by '"'
    lines terminated by '\n'
    ignore 1 lines
    (sp_id,
    @sp_name,
    @seller_rating,
    @dealer_zip,
    @longitude,
    @latitude,
    @city,
    franchise_dealer)
    SET sp_name = IF(@sp_name = '', NULL, UPPER(@sp_name)), 
    seller_rating = IF(@seller_rating = '', NULL, @seller_rating),
    dealer_zip = IF(@dealer_zip = '', NULL, @dealer_zip),
    longitude = IF(@longitude = '', NULL, @longitude),
    latitude = IF(@latitude = '', NULL, @latitude),
    city = IF(@city = '', NULL, UPPER(@city));



SELECT '---------------------------------------------------------------------------------------' AS '';

SELECT 'Create CarInfo' AS '';

CREATE TABLE CarInfo (
    make_id int,
    model_name varchar(255),
    year smallint,
    trim_name varchar(255),
    height decimal(4,1),
    width decimal(4,1),
    length decimal(4,1),
    exterior_color varchar(255),
    interior_color varchar(255),
    body_type varchar(40),
    fuel_tank_volume decimal(3,1), 
    fuel_type varchar(40), 
    is_new bool not null default 0, 
    maximum_seating int,
    back_legroom decimal(3,1),
    front_legroom decimal(3,1),
    engine_displacement int,
    transmission varchar(20),   
    transmission_display varchar(50),
    wheel_system varchar(20),
    wheel_system_display varchar(40),
    wheelbase decimal(4,1),
    horsepower int,
    power_rpm int,
    torque_rpm int,
    torque_force int,
    PRIMARY KEY(make_id,model_name,year,trim_name),
    CHECK(height > 0),
    CHECK(width > 0),
    CHECK(length > 0),
    CHECK(engine_displacement >= 0)
);


SELECT 'Load CarInfo' AS '';

load data infile '/var/lib/mysql-files/Group6/car_data.csv' ignore into table CarInfo
    fields terminated by ','
    enclosed by '"'
    lines terminated by '\n'
    ignore 1 lines
    (@make_name,
    @model_name,
    year,
    @trim_name,
    @height,
    @width,
    @length,
    @exterior_color,
    @interior_color,
    @body_type,
    @fuel_type,
    is_new,
    @maximum_seating,
    @back_legroom,
    @front_legroom,
    @transmission,
    @transmission_display,
    @wheel_system,
    @wheel_system_display,
    @wheelbase,
    @horsepower,
    @power_rpm,
    @torque_rpm,
    @torque_force)

    SET make_id = (SELECT make_id from MakeInfo where make_name = @make_name),
    model_name = UPPER(@model_name),
    trim_name = UPPER(@trim_name),
    height = IF(@height = '', NULL, (SELECT replace(@height , ' in','') where @height like '% in%')),
    width = IF(@width = '', NULL, (SELECT replace(@width , ' in','') where @width like '% in%')),
    length = IF(@length = '', NULL, (SELECT replace(@length , ' in','') where @length like '% in%')),
    exterior_color = IF(@exterior_color = '', NULL, UPPER(@exterior_color)),
    interior_color = IF(@interior_color = '', NULL, UPPER(@interior_color)),
    body_type = IF(@body_type = '', NULL, UPPER(@body_type)),
    fuel_type = IF(@fuel_type = '', NULL, UPPER(@fuel_type)),
    maximum_seating = IF(@maximum_seating = '', NULL, (SELECT replace(@maximum_seating , ' seats','') where @maximum_seating like '% seats%')),
    back_legroom = IF(@back_legroom = '', NULL, (SELECT replace(@back_legroom , ' in','') where @back_legroom like '% in%')),
    front_legroom = IF(@front_legroom = '', NULL, (SELECT replace(@front_legroom , ' in','') where @front_legroom like '% in%')),
    transmission = IF(@transmission = '', NULL, @transmission),
    transmission_display = IF(@transmission_display = '', NULL, UPPER(@transmission_display)),
    wheel_system = IF(@wheel_system = '', NULL, @wheel_system),
    wheel_system_display = IF(@wheel_system_display = '', NULL, UPPER(@wheel_system_display)),
    wheelbase = IF(@wheelbase = '', NULL, (SELECT replace(@wheelbase , ' in','') where @wheelbase like '% in%')),
    horsepower = IF(@horsepower = '', NULL, @horsepower),
    power_rpm = IF(@power_rpm = '', NULL, @power_rpm),
    torque_rpm = IF(@torque_rpm = '', NULL, @torque_rpm),
    torque_force = IF(@torque_force = '', NULL, @torque_force);


SELECT '---------------------------------------------------------------------------------------' AS '';

SELECT 'Create ListingInfo' AS '';

CREATE TABLE ListingInfo (
    listing_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    model_name varchar(40),
    make_id int,
    year smallint,
    trim_name varchar(255),
    vin varchar(17),
    sp_id int,
    description text,
    city_fuel_economy int,
    highway_fuel_economy int,
    listed_date date,
    mileage int,
    price int,
    savings_amount int not null default 0,
    listing_color varchar(255),
    has_accidents bool not null default 0,
    daysonmarket int,
    FOREIGN KEY(make_id, model_name, year, trim_name) REFERENCES CarInfo(make_id, model_name, year, trim_name),
    FOREIGN KEY(sp_id) REFERENCES SellerInfo(sp_id),
    CHECK(price >= 0),
    CHECK(city_fuel_economy >= 0),
    CHECK(highway_fuel_economy >= 0),
    CHECK(mileage >= 0),
    CHECK(savings_amount >= 0),
    CHECK(daysonmarket >= 0)
);

SELECT 'Load ListingInfo' AS '';

load data infile '/var/lib/mysql-files/Group6/listing_data.csv' ignore into table ListingInfo 
fields terminated by ',' 
enclosed by '"' 
lines terminated by '\n' 
ignore 1 lines 
    (@model_name,
    @make_name,
    year,
    @trim_name,
    vin,
    sp_id,
    @description,
    @city_fuel_economy,
    @highway_fuel_economy,
    @listed_date,
    @mileage,
    @price,
    @savings_amount,
    @listing_color,
    @has_accidents,
    @daysonmarket)
    
    SET listing_id = NULL,
    model_name = UPPER(@model_name),
    make_id = (SELECT make_id from MakeInfo where make_name = @make_name),
    trim_name = UPPER(@trim_name),
    description = IF(@description = '', NULL, @description),
    city_fuel_economy = IF(@city_fuel_economy = '', NULL, @city_fuel_economy),
    highway_fuel_economy = IF(@highway_fuel_economy = '', NULL, @highway_fuel_economy),
    listed_date = IF(@listed_date = '', NULL, @listed_date),
    mileage = IF(@mileage = '', NULL, @mileage),
    price = IF(@price = '', NULL, @price),
    savings_amount = IF(@savings_amount = '', NULL, @savings_amount),
    listing_color = IF(@listing_color = '', NULL, UPPER(@listing_color)),
    has_accidents = IF(@has_accidents = '', 0, @has_accidents),
    daysonmarket = IF(@daysonmarket = '', NULL, @daysonmarket);




SELECT '---------------------------------------------------------------------------------------' AS '';

SELECT 'Create CarNonElectrics' AS '';

CREATE TABLE CarNonElectrics (
    make_id int,
    model_name varchar(255),
    year smallint,
    trim_name varchar(255),
    engine_type varchar(50),
    fuel_tank_volume decimal(3,1), 
    engine_displacement int,
    PRIMARY KEY(make_id,model_name,year,trim_name),
    CHECK(engine_displacement >= 0)
);

ALTER TABLE
    CarNonElectrics
ADD
    FOREIGN KEY(make_id,model_name,year,trim_name) REFERENCES CarInfo(make_id,model_name,year,trim_name);

load data infile '/var/lib/mysql-files/Group6/car_non_electric_data.csv' ignore into table CarNonElectrics
    fields terminated by ','
    enclosed by '"'
    lines terminated by '\n'
    ignore 1 lines
    (@make_name,
    @model_name,
    year,
    @trim_name,
    @engine_type,
    @fuel_tank_volume,
    @engine_displacement)

    SET make_id = (SELECT make_id from MakeInfo where make_name = @make_name),
    model_name = UPPER(@model_name),
    trim_name = UPPER(@trim_name),
    engine_type = IF(@engine_type = '', NULL, UPPER(@engine_type)),
    fuel_tank_volume = IF(@fuel_tank_volume = '', NULL, (SELECT replace(@fuel_tank_volume , ' gal','') where @fuel_tank_volume like '% gal%')),
    engine_displacement = IF(@engine_displacement = '', NULL, @engine_displacement);



SELECT '---------------------------------------------------------------------------------------' AS '';

SELECT 'Create CarPickupTrucks' AS '';

CREATE TABLE CarPickupTrucks (
    make_id int,
    model_name varchar(255),
    year smallint,
    trim_name varchar(255),
    bed_length decimal(4,1),
    PRIMARY KEY(make_id,model_name,year,trim_name)
);

ALTER TABLE
    CarPickupTrucks
ADD
    FOREIGN KEY(make_id,model_name,year,trim_name) REFERENCES CarInfo(make_id,model_name,year,trim_name);

load data infile '/var/lib/mysql-files/Group6/car_pickup_truck_data.csv' ignore into table CarPickupTrucks
    fields terminated by ','
    enclosed by '"'
    lines terminated by '\n'
    ignore 1 lines
    (@make_name,
    @model_name,
    year,
    @trim_name,
    @bed_length)

    SET make_id = (SELECT make_id from MakeInfo where make_name = @make_name),
    model_name = UPPER(@model_name),
    trim_name = UPPER(@trim_name),
    bed_length = IF(@bed_length = '', NULL, (SELECT replace(@bed_length , ' in','') where @bed_length like '% in%'));


SELECT '---------------------------------------------------------------------------------------' AS '';

SELECT 'Create Indexes' AS '';


CREATE INDEX idx_price on ListingInfo(price);
CREATE INDEX idx_mileage on ListingInfo(mileage);
CREATE INDEX idx_vin on ListingInfo(vin);
CREATE INDEX idx_cfe on ListingInfo(city_fuel_economy);
CREATE INDEX idx_hfe on ListingInfo(highway_fuel_economy);
CREATE INDEX idx_savings on ListingInfo(savings_amount);
CREATE INDEX idx_seller_name on SellerInfo(sp_name, sp_id);
CREATE INDEX idx_seller_rating on SellerInfo(seller_rating, sp_id);
