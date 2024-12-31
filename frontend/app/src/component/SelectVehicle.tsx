import { useEffect, useState } from "react";
import Select, { SingleValue } from "react-select";

import { Make, Type, Model, YearModel, Vehicle } from "../lib/Types";
import getHost from "../lib/GetHost";

import Loading from "./Loading";
import GenericError from "./Error";

export default function SelectVehicle({
  selectedMake,
  selectedType,
  selectedModel,
  selectedYearModel,
  handleVehicleChange,
}: {
  selectedMake: Make;
  selectedType: Type;
  selectedModel: Model;
  selectedYearModel: YearModel;
  handleVehicleChange: (obj: SingleValue<Vehicle>) => void;
}) {
  const [vehicle, setVehicle] = useState<Vehicle | null>(null);
  const [vehicleList, setVehicleList] = useState<Array<Vehicle> | null>(null);
  const [isLoading, setLoading] = useState<boolean>(true);

  const onVehicleChanged = (obj: SingleValue<Vehicle>) => {
    setVehicle(obj);
    handleVehicleChange(obj);
  };

  useEffect(() => {
    let host: string = getHost();
    fetch(
      `${host}/api/vehicles/stock?` +
        new URLSearchParams({
          mk: selectedMake.id,
          t: selectedType.id,
          mdl: selectedModel.id,
          y: selectedYearModel.year.toString(),
        })
    )
      .then((response) => response.json())
      .then((jsonData) => {
        let vehicles: Array<Vehicle> = jsonData.items.map(
          (x: object) => x as Vehicle
        );
        setVehicleList(vehicles);
        setLoading(false);
      });
  }, []);

  if (isLoading) {
    return (
      <Loading
        text={`Loading vehicles for make ${selectedMake.name}, type ${selectedType.name}, model ${selectedModel.name} and year model ${selectedYearModel.year}`}
      />
    );
  }

  if (!vehicleList) {
    return (
      <GenericError
        text={`No vehicles found for make '${selectedMake.name}' (${selectedMake.id}), type '${selectedType.name}' (${selectedType.id}), model '${selectedModel.name}' (${selectedType.name}) and year model '${selectedYearModel.year}'`}
      />
    );
  }

  return (
    <Select
      placeholder={`Select a vehicle from ${selectedYearModel.year} ${selectedMake.name} ${selectedModel.name}`}
      value={vehicle}
      options={vehicleList}
      onChange={onVehicleChanged}
      getOptionLabel={(x) => x.yearModelSpec}
      getOptionValue={(x) => x.id}
    />
  );
}
