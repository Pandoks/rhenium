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
