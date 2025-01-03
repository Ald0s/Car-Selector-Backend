import { useEffect, useState } from "react";
import Select, { SingleValue } from "react-select";

import { Make, Type, Model } from "../lib/Types";
import getHost from "../lib/GetHost";

import Loading from "./Loading";
import GenericError from "./Error";

export default function SelectModel({
  selectedMake,
  selectedType,
  handleModelChange,
}: {
  selectedMake: Make;
  selectedType: Type;
  handleModelChange: (obj: SingleValue<Model>) => void;
}) {
  const [model, setModel] = useState<Model | null>(null);
  const [modelList, setModelList] = useState<Array<Model> | null>(null);
  const [isLoading, setLoading] = useState<boolean>(true);
  console.log(model);
  const onModelChanged = (obj: SingleValue<Model>) => {
    setModel(obj);
    handleModelChange(obj);
  };

  useEffect(() => {
    let host: string = getHost();
    fetch(
      `${host}/api/vehicles/models?` +
        new URLSearchParams({
          mk: selectedMake.id,
          t: selectedType.id,
        })
    )
      .then((response) => response.json())
      .then((jsonData) => {
        let models: Array<Model> = jsonData.items.map(
          (x: object) => x as Model
        );
        setModelList(models);
        setLoading(false);
      });
  }, []);

  if (isLoading) {
    return (
      <Loading
        text={`Loading models for make ${selectedMake.name} and type ${selectedType.name}`}
      />
    );
  }

  if (!modelList) {
    return (
      <GenericError
        text={`No models found for make '${selectedMake.name}' (${selectedMake.id}) and type '${selectedType.name}' (${selectedType.id})`}
      />
    );
  }

  return (
    <Select
      placeholder={`Select a ${selectedType.name} model from ${selectedMake.name}`}
      value={model}
      options={modelList}
      onChange={onModelChanged}
      getOptionLabel={(x) => x.name}
      getOptionValue={(x) => x.id}
    />
  );
}
