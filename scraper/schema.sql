CREATE TABLE properties (
  address TEXT,
  city TEXT,
  zip VARCHAR(10),
  state VARCHAR(2),
  status TEXT,
  price MONEY,
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
