export type Make = {
  id: string;
  name: string;
};

export type Type = {
  id: string;
  name: string;
  description: string;
};

export type Model = {
  id: string;
  vehicleMakeId: string;
  name: string;
  typeId: Type;
};

export type YearModel = {
  id: string;
  vehicleMakeId: string;
  vehicleModelId: string;
  year: number;
};

export type Vehicle = {
  id: string;
  vehicleYearModelId: string;
  motorType: string;
  title: string;
  yearModelSpec: string;

  badge: string | null;
  version: string | null;
  displacement: number | null;
  induction: string | null;
  fuelType: string | null;

  power: number | null;
  elecType: string | null;

  transmissionType: string | null;
  numGears: number | null;
};
