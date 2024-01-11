export type Make = {
  uid: string;
  name: string;
};

export type Type = {
  type_id: string;
  name: string;
  description: string;
};

export type Model = {
  uid: string;
  make_uid: string;
  name: string;
  type: Type;
};

export type YearModel = {
  make_uid: string;
  model_uid: string;
  year: number;
};

export type Vehicle = {
  vehicle_uid: string;

  badge: string | null;
  version: string | null;

  motor_type: string;
  displacement: number | null;
  induction: string | null;
  fuel_type: string | null;

  power: number | null;
  elec_type: string | null;

  trans_type: string | null;
  num_gears: number | null;

  make: Make;
  model: Model;
  year_model_year_: number;
};
