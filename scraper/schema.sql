CREATE TABLE properties (
  address TEXT,
  city TEXT,
  zip VARCHAR(10),
  state VARCHAR(2),
  status TEXT,
  price MONEY,
  bathrooms REAL,
  full_bathrooms SMALLINT,
  half_bathrooms SMALLINT,
  three_fourths_bathrooms SMALLINT,
  one_fourths_bathrooms SMALLINT,
  stories SMALLINT,
  bedrooms SMALLINT,
  parcel_number INTEGER,
  year_built VARCHAR(4),
  zoning TEXT,
  lot_size TEXT,
  structure_size TEXT,
  interior_living_size TEXT,
  parking_spaces SMALLINT,
  garage_spaces SMALLINT,
  covered_spaces SMALLINT,
  fireplace_count SMALLINT,
  home_type TEXT,
  architectural_style TEXT,
  basement BOOLEAN,
  hoa BOOLEAN,
  hoa_fee TEXT,
  laundry TEXT,
  foundation TEXT,
  senior_community BOOLEAN,
  property_condition TEXT,
  PRIMARY KEY (address, city, zip, state)
);

CREATE TABLE tax_history (
  year VARCHAR(4),
  assessment MONEY,
  taxes MONEY,
  address TEXT,
  city TEXT,
  zip VARCHAR(10),
  state VARCHAR(2),
  PRIMARY KEY (address, city, zip, state, year),
  FOREIGN KEY (address, city, zip, state) REFERENCES properties(address, city, zip, state)
);

CREATE TABLE price_history (
  date DATE,
  event TEXT,
  price MONEY,
  address TEXT,
  city TEXT,
  zip VARCHAR(10),
  state VARCHAR(2),
  PRIMARY KEY (address, city, zip, state, date),
  FOREIGN KEY (address, city, zip, state) REFERENCES properties(address, city, zip, state)
);

CREATE TABLE accessibility_features (
  feature TEXT,
  address TEXT,
  city TEXT,
  zip VARCHAR(10),
  state VARCHAR(2),
  PRIMARY KEY (address, city, zip, state, feature),
  FOREIGN KEY (address, city, zip, state) REFERENCES properties(address, city, zip, state)
);

CREATE TABLE additional_structures (
  structure TEXT,
  address TEXT,
  city TEXT,
  zip VARCHAR(10),
  state VARCHAR(2),
  PRIMARY KEY (address, city, zip, state, structure),
  FOREIGN KEY (address, city, zip, state) REFERENCES properties(address, city, zip, state)
);

CREATE TABLE amenities (
  amenity TEXT,
  address TEXT,
  city TEXT,
  zip VARCHAR(10),
  state VARCHAR(2),
  PRIMARY KEY (address, city, zip, state, amenity),
  FOREIGN KEY (address, city, zip, state) REFERENCES properties(address, city, zip, state)
);

CREATE TABLE bathroom_features (
  feature TEXT,
  address TEXT,
  city TEXT,
  zip VARCHAR(10),
  state VARCHAR(2),
  PRIMARY KEY (address, city, zip, state, feature),
  FOREIGN KEY (address, city, zip, state) REFERENCES properties(address, city, zip, state)
);

CREATE TABLE bedroom_features (
  feature TEXT,
  address TEXT,
  city TEXT,
  zip VARCHAR(10),
  state VARCHAR(2),
  PRIMARY KEY (address, city, zip, state, feature),
  FOREIGN KEY (address, city, zip, state) REFERENCES properties(address, city, zip, state)
);

CREATE TABLE construction_materials (
  material TEXT,
  address TEXT,
  city TEXT,
  zip VARCHAR(10),
  state VARCHAR(2),
  PRIMARY KEY (address, city, zip, state, material),
  FOREIGN KEY (address, city, zip, state) REFERENCES properties(address, city, zip, state)
);

CREATE TABLE cooling (
  type TEXT,
  address TEXT,
  city TEXT,
  zip VARCHAR(10),
  state VARCHAR(2),
  PRIMARY KEY (address, city, zip, state, type),
  FOREIGN KEY (address, city, zip, state) REFERENCES properties(address, city, zip, state)
);

CREATE TABLE dining_features (
  feature TEXT,
  address TEXT,
  city TEXT,
  zip VARCHAR(10),
  state VARCHAR(2),
  PRIMARY KEY (address, city, zip, state, feature),
  FOREIGN KEY (address, city, zip, state) REFERENCES properties(address, city, zip, state)
);

CREATE TABLE exterior_features (
  feature TEXT,
  address TEXT,
  city TEXT,
  zip VARCHAR(10),
  state VARCHAR(2),
  PRIMARY KEY (address, city, zip, state, feature),
  FOREIGN KEY (address, city, zip, state) REFERENCES properties(address, city, zip, state)
);

CREATE TABLE family_features (
  feature TEXT,
  address TEXT,
  city TEXT,
  zip VARCHAR(10),
  state VARCHAR(2),
  PRIMARY KEY (address, city, zip, state, feature),
  FOREIGN KEY (address, city, zip, state) REFERENCES properties(address, city, zip, state)
);

CREATE TABLE fencing (
  type TEXT,
  address TEXT,
  city TEXT,
  zip VARCHAR(10),
  state VARCHAR(2),
  PRIMARY KEY (address, city, zip, state, type),
  FOREIGN KEY (address, city, zip, state) REFERENCES properties(address, city, zip, state)
);

CREATE TABLE fireplace_features (
  feature TEXT,
  address TEXT,
  city TEXT,
  zip VARCHAR(10),
  state VARCHAR(2),
  PRIMARY KEY (address, city, zip, state, feature),
  FOREIGN KEY (address, city, zip, state) REFERENCES properties(address, city, zip, state)
);

CREATE TABLE flooring (
  type TEXT,
  address TEXT,
  city TEXT,
  zip VARCHAR(10),
  state VARCHAR(2),
  PRIMARY KEY (address, city, zip, state, type),
  FOREIGN KEY (address, city, zip, state) REFERENCES properties(address, city, zip, state)
);

CREATE TABLE gas (
  type TEXT,
  address TEXT,
  city TEXT,
  zip VARCHAR(10),
  state VARCHAR(2),
  PRIMARY KEY (address, city, zip, state, type),
  FOREIGN KEY (address, city, zip, state) REFERENCES properties(address, city, zip, state)
);

CREATE TABLE heating (
  type TEXT,
  address TEXT,
  city TEXT,
  zip VARCHAR(10),
  state VARCHAR(2),
  PRIMARY KEY (address, city, zip, state, type),
  FOREIGN KEY (address, city, zip, state) REFERENCES properties(address, city, zip, state)
);

CREATE TABLE included_appliances (
  appliance TEXT,
  address TEXT,
  city TEXT,
  zip VARCHAR(10),
  state VARCHAR(2),
  PRIMARY KEY (address, city, zip, state, appliance),
  FOREIGN KEY (address, city, zip, state) REFERENCES properties(address, city, zip, state)
);

CREATE TABLE interior_features (
  feature TEXT,
  address TEXT,
  city TEXT,
  zip VARCHAR(10),
  state VARCHAR(2),
  PRIMARY KEY (address, city, zip, state, feature),
  FOREIGN KEY (address, city, zip, state) REFERENCES properties(address, city, zip, state)
);

CREATE TABLE kitchen_features (
  feature TEXT,
  address TEXT,
  city TEXT,
  zip VARCHAR(10),
  state VARCHAR(2),
  PRIMARY KEY (address, city, zip, state, feature),
  FOREIGN KEY (address, city, zip, state) REFERENCES properties(address, city, zip, state)
);

CREATE TABLE lot_features (
  feature TEXT,
  address TEXT,
  city TEXT,
  zip VARCHAR(10),
  state VARCHAR(2),
  PRIMARY KEY (address, city, zip, state, feature),
  FOREIGN KEY (address, city, zip, state) REFERENCES properties(address, city, zip, state)
);

CREATE TABLE parking (
  type TEXT,
  address TEXT,
  city TEXT,
  zip VARCHAR(10),
  state VARCHAR(2),
  PRIMARY KEY (address, city, zip, state, type),
  FOREIGN KEY (address, city, zip, state) REFERENCES properties(address, city, zip, state)
);

CREATE TABLE patio_porch_details (
  detail TEXT,
  address TEXT,
  city TEXT,
  zip VARCHAR(10),
  state VARCHAR(2),
  PRIMARY KEY (address, city, zip, state, detail),
  FOREIGN KEY (address, city, zip, state) REFERENCES properties(address, city, zip, state)
);

CREATE TABLE pool_features (
  feature TEXT,
  address TEXT,
  city TEXT,
  zip VARCHAR(10),
  state VARCHAR(2),
  PRIMARY KEY (address, city, zip, state, feature),
  FOREIGN KEY (address, city, zip, state) REFERENCES properties(address, city, zip, state)
);

CREATE TABLE property_subtype (
  type TEXT,
  address TEXT,
  city TEXT,
  zip VARCHAR(10),
  state VARCHAR(2),
  PRIMARY KEY (address, city, zip, state, type),
  FOREIGN KEY (address, city, zip, state) REFERENCES properties(address, city, zip, state)
);

CREATE TABLE roof (
  type TEXT,
  address TEXT,
  city TEXT,
  zip VARCHAR(10),
  state VARCHAR(2),
  PRIMARY KEY (address, city, zip, state, type),
  FOREIGN KEY (address, city, zip, state) REFERENCES properties(address, city, zip, state)
);

CREATE TABLE services (
  service TEXT,
  address TEXT,
  city TEXT,
  zip VARCHAR(10),
  state VARCHAR(2),
  PRIMARY KEY (address, city, zip, state, service),
  FOREIGN KEY (address, city, zip, state) REFERENCES properties(address, city, zip, state)
);

CREATE TABLE sewer (
  type TEXT,
  address TEXT,
  city TEXT,
  zip VARCHAR(10),
  state VARCHAR(2),
  PRIMARY KEY (address, city, zip, state, type),
  FOREIGN KEY (address, city, zip, state) REFERENCES properties(address, city, zip, state)
);

CREATE TABLE spa_features (
  feature TEXT,
  address TEXT,
  city TEXT,
  zip VARCHAR(10),
  state VARCHAR(2),
  PRIMARY KEY (address, city, zip, state, feature),
  FOREIGN KEY (address, city, zip, state) REFERENCES properties(address, city, zip, state)
);

CREATE TABLE utilities (
  utility TEXT,
  address TEXT,
  city TEXT,
  zip VARCHAR(10),
  state VARCHAR(2),
  PRIMARY KEY (address, city, zip, state, utility),
  FOREIGN KEY (address, city, zip, state) REFERENCES properties(address, city, zip, state)
);

CREATE TABLE view_description (
  description TEXT,
  address TEXT,
  city TEXT,
  zip VARCHAR(10),
  state VARCHAR(2),
  PRIMARY KEY (address, city, zip, state, description),
  FOREIGN KEY (address, city, zip, state) REFERENCES properties(address, city, zip, state)
);

