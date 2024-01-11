import { useEffect, useState } from "react";
import Select, { SingleValue } from "react-select";

import { Make, Type, Model, YearModel, Vehicle } from "@/app/lib/definitions";
import { testVehiclesReply } from "@/app/lib/example-data";
import { API_HOST } from "@/app/lib/gethost";

import Loading from "./loading";
import GenericError from "./error";

/* The example/test version. */
function queryVehicles(
  makeUid: string,
  typeId: string,
  modelUid: string,
  year: number
): Array<Vehicle> {
  return testVehiclesReply.items.map((x) => x as Vehicle);
}

export function getVehicleTitle(vehicle: Vehicle): string {
  return `${vehicle.year_model_year_} ${vehicle.make.name} ${vehicle.model.name}`;
}

export function getVehicleOptions(vehicle: Vehicle): string {
  var optionsStr = "";
  if (vehicle.badge) {
    optionsStr += vehicle.badge + " ";
  } else if (vehicle.version) {
    optionsStr += vehicle.version + " ";
  }

  switch (vehicle.motor_type) {
    case "piston":
      // Piston type. Options will include displacement (as litres) and induction type.
      optionsStr += `${parseFloat(
        (vehicle.displacement! / 1000).toString()
      ).toFixed(1)}L ${vehicle.induction!}`;
      break;

    default:
      // No such motor type.
      throw new Error();
  }

  switch (vehicle.trans_type) {
    case "A":
      optionsStr += ` ${vehicle.num_gears} spd Automatic`;
      break;

    case "M":
      optionsStr += ` ${vehicle.num_gears} spd Manual`;
      break;
  }
  return optionsStr;
}

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
    fetch(
      `http://${API_HOST}/api/vehicles/stock?` +
        new URLSearchParams({
          mk: selectedMake.uid,
          t: selectedType.type_id,
          mdl: selectedModel.uid,
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
        text={`No vehicles found for make '${selectedMake.name}' (${selectedMake.uid}), type '${selectedType.name}' (${selectedType.type_id}), model '${selectedModel.name}' (${selectedType.name}) and year model '${selectedYearModel.year}'`}
      />
    );
  }

  return (
    <Select
      placeholder={`Select a vehicle from ${selectedYearModel.year} ${selectedMake.name} ${selectedModel.name}`}
      value={vehicle}
      options={vehicleList}
      onChange={onVehicleChanged}
      getOptionLabel={(x) => getVehicleOptions(x)}
      getOptionValue={(x) => x.vehicle_uid}
    />
  );
}
