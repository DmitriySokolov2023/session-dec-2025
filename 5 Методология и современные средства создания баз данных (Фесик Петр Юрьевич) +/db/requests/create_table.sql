
CREATE TABLE clients (
  id BIGSERIAL PRIMARY KEY,
  is_company BOOLEAN  NOT NULL DEFAULT FALSE,
  name VARCHAR(150) NOT NULL,
  phone VARCHAR(20),
  email  VARCHAR(120),
  comment  VARCHAR(300),
  CONSTRAINT clients_phone_uq UNIQUE (phone),
  CONSTRAINT clients_email_uq UNIQUE (email),
  CONSTRAINT clients_name_chk CHECK (name <> '')
);


CREATE TABLE cars (
  id BIGSERIAL PRIMARY KEY,
  client_id  BIGINT NOT NULL REFERENCES clients(id) ON UPDATE CASCADE,
  make VARCHAR(50)  NOT NULL,
  model  VARCHAR(50)  NOT NULL,
  vin  VARCHAR(17)  NOT NULL,
  license_plate  VARCHAR(15)  NOT NULL,
  year INT,
  mileage  INT,
  CONSTRAINT cars_vin_uq  UNIQUE (vin),
  CONSTRAINT cars_plate_uq  UNIQUE (license_plate),
  CONSTRAINT cars_year_chk  CHECK (year IS NULL OR year BETWEEN 1950 AND 2100),
  CONSTRAINT cars_mileage_chk CHECK (mileage IS NULL OR mileage >= 0),

  CONSTRAINT cars_id_client_uq  UNIQUE (id, client_id)
);


CREATE TABLE roles (
  id  BIGSERIAL PRIMARY KEY,
  name  VARCHAR(40)  NOT NULL,
  description VARCHAR(200),
  CONSTRAINT roles_name_uq UNIQUE (name)
);


CREATE TABLE employees (
  id BIGSERIAL PRIMARY KEY,
  role_id  BIGINT NOT NULL REFERENCES roles(id) ON UPDATE CASCADE,
  full_name  VARCHAR(120) NOT NULL,
  phone  VARCHAR(20),
  email  VARCHAR(120),
  active BOOLEAN  NOT NULL DEFAULT TRUE,
  CONSTRAINT employees_name_chk CHECK (full_name <> ''),
  CONSTRAINT employees_email_uq UNIQUE (email)
);


CREATE TABLE users (
  id  BIGSERIAL PRIMARY KEY,
  employee_id BIGINT NOT NULL UNIQUE
   REFERENCES employees(id) ON DELETE CASCADE,
  username  VARCHAR(50)  NOT NULL UNIQUE,
  password  VARCHAR(255) NOT NULL,
  active  BOOLEAN  NOT NULL DEFAULT TRUE
);


CREATE TABLE services (
  id  BIGSERIAL PRIMARY KEY,
  name  VARCHAR(100) NOT NULL,
  unit  VARCHAR(20)  NOT NULL DEFAULT 'шт',
  base_price  NUMERIC(10,2) NOT NULL,
  description VARCHAR(300),
  CONSTRAINT services_name_uq  UNIQUE (name),
  CONSTRAINT services_price_chk CHECK (base_price >= 0)
);


CREATE TABLE parts (
  id  BIGSERIAL PRIMARY KEY,
  part_number VARCHAR(50),
  name  VARCHAR(120) NOT NULL,
  unit  VARCHAR(20)  NOT NULL DEFAULT 'шт',
  price NUMERIC(10,2) NOT NULL,
  stock_qty INT NOT NULL DEFAULT 0,
  CONSTRAINT parts_part_number_uq UNIQUE (part_number),
  CONSTRAINT parts_price_chk  CHECK (price >= 0),
  CONSTRAINT parts_stock_chk  CHECK (stock_qty >= 0)
);


CREATE TABLE orders (
  id BIGSERIAL PRIMARY KEY,
  client_id  BIGINT NOT NULL,
  car_id BIGINT NOT NULL,
  manager_id BIGINT REFERENCES employees(id) ON UPDATE CASCADE,
  opened_at  DATE NOT NULL,
  closed_at  DATE,
  status VARCHAR(15) NOT NULL,
  comment  VARCHAR(300),


  CONSTRAINT orders_client_fk FOREIGN KEY (client_id)
  REFERENCES clients(id) ON UPDATE CASCADE,

  CONSTRAINT orders_car_client_fk FOREIGN KEY (car_id, client_id)
  REFERENCES cars(id, client_id) ON UPDATE CASCADE,

  CONSTRAINT orders_status_chk CHECK (status IN ('новый','в_работе','выполнен','оплачен','отменён'))
);


CREATE INDEX idx_orders_client ON orders(client_id);
CREATE INDEX idx_orders_car  ON orders(car_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_opened ON orders(opened_at);

CREATE TABLE service_items (
  id  BIGSERIAL PRIMARY KEY,
  order_id  BIGINT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  service_id  BIGINT NOT NULL REFERENCES services(id),
  employee_id BIGINT REFERENCES employees(id), 
  quantity  NUMERIC(10,2) NOT NULL DEFAULT 1,
  unit_price  NUMERIC(10,2) NOT NULL,
  line_total  NUMERIC(12,2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
  CONSTRAINT service_items_qty_chk CHECK (quantity > 0),
  CONSTRAINT service_items_price_chk CHECK (unit_price >= 0)
);

CREATE INDEX idx_service_items_order ON service_items(order_id);
CREATE INDEX idx_service_items_worker  ON service_items(employee_id);
CREATE INDEX idx_service_items_service ON service_items(service_id);

CREATE TABLE material_items (
  id  BIGSERIAL PRIMARY KEY,
  service_item_id BIGINT NOT NULL REFERENCES service_items(id) ON DELETE CASCADE,
  part_id BIGINT NOT NULL REFERENCES parts(id),
  quantity  NUMERIC(10,2) NOT NULL,
  unit_price  NUMERIC(10,2) NOT NULL,
  line_total  NUMERIC(12,2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
  CONSTRAINT material_items_qty_chk CHECK (quantity > 0),
  CONSTRAINT material_items_price_chk CHECK (unit_price >= 0)
);

CREATE INDEX idx_material_items_service_item ON material_items(service_item_id);
CREATE INDEX idx_material_items_part ON material_items(part_id);
