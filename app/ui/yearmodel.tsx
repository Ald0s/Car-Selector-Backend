import { useEffect, useState } from "react";
import Select, { SingleValue } from "react-select";

import { Make, Type, Model, YearModel } from "@/app/lib/definitions";
import { testYearModelsReply } from "@/app/lib/example-data";
import { API_HOST } from "@/app/lib/gethost";

import Loading from "./loading";
import GenericError from "./error";

/* The example/test version. */
function queryYearModels(
  makeUid: string,
  typeId: string,
  modelUid: string
): Array<YearModel> {
  return testYearModelsReply.items.map((x) => x as YearModel);
}

export default function SelectYearModel({
  selectedMake,
  selectedType,
  selectedModel,
  handleYearModelChange,
}: {
  selectedMake: Make;
  selectedType: Type;
  selectedModel: Model;
  handleYearModelChange: (obj: SingleValue<YearModel>) => void;
}) {
  const [yearModel, setYearModel] = useState<YearModel | null>(null);
  const [yearModelList, setYearModelList] = useState<Array<YearModel> | null>(
    null
  );
  const [isLoading, setLoading] = useState<boolean>(true);

  const onYearModelChanged = (obj: SingleValue<YearModel>) => {
    setYearModel(obj);
    handleYearModelChange(obj);
  };

  useEffect(() => {
    fetch(
      `http://${API_HOST}/api/vehicles/years?` +
        new URLSearchParams({
          mk: selectedMake.uid,
          t: selectedType.type_id,
          mdl: selectedModel.uid,
        })
    )
      .then((response) => response.json())
      .then((jsonData) => {
        let yearModels: Array<YearModel> = jsonData.items.map(
          (x: object) => x as YearModel
        );
        setYearModelList(yearModels);
        setLoading(false);
      });
  }, []);

  if (isLoading) {
    return (
      <Loading
        text={`Loading year models for make ${selectedMake.name}, type ${selectedType.name} and model ${selectedModel.name}`}
      />
    );
  }

  if (!yearModelList) {
    return (
      <GenericError
        text={`No year models found for make '${selectedMake.name}' (${selectedMake.uid}), type '${selectedType.name}' (${selectedType.type_id}) and model '${selectedModel.name}' (${selectedType.name})`}
      />
    );
  }

  return (
    <Select
      placeholder={`Select a year for your ${selectedMake.name} ${selectedModel.name}`}
      value={yearModel}
      options={yearModelList}
      onChange={onYearModelChanged}
      getOptionLabel={(x) => x.year.toString()}
      getOptionValue={(x) => x.year.toString()}
    />
  );
}
