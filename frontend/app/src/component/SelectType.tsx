import { useEffect, useState } from "react";
import Select, { SingleValue } from "react-select";

import { Make, Type } from "../lib/Types";
import getHost from "../lib/GetHost";

import Loading from "./Loading";
import GenericError from "./Error";

export default function SelectType({
  selectedMake,
  handleTypeChange,
}: {
  selectedMake: Make;
  handleTypeChange: (obj: SingleValue<Type>) => void;
}) {
  const [type_, setType] = useState<Type | null>(null);
  const [typeList, setTypeList] = useState<Array<Type> | null>(null);
  const [isLoading, setLoading] = useState<boolean>(true);

  const onTypeChanged = (obj: SingleValue<Type>) => {
    setType(obj);
    handleTypeChange(obj);
  };

  useEffect(() => {
    let host: string = getHost();
    fetch(
      `${host}/api/vehicles/types?` +
        new URLSearchParams({
          mk: selectedMake.id,
        })
    )
      .then((response) => response.json())
      .then((jsonData) => {
        let types: Array<Type> = jsonData.items.map((x: object) => x as Type);
        setTypeList(types);
        setLoading(false);
      });
  }, []);

  if (isLoading) {
    return <Loading text={`Loading types for make ${selectedMake.name}`} />;
  }

  if (!typeList) {
    return (
      <GenericError
        text={`No types found for make '${selectedMake.name}' (${selectedMake.id})`}
      />
    );
  }

  return (
    <Select
      placeholder={`Select a type of ${selectedMake.name}`}
      value={type_}
      options={typeList}
      onChange={onTypeChanged}
      getOptionLabel={(x) => x.name}
      getOptionValue={(x) => x.id}
    />
  );
}
