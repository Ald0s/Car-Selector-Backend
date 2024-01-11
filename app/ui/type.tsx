import { useEffect, useState } from "react";
import Select, { SingleValue } from "react-select";

import { Make, Type } from "@/app/lib/definitions";
import { testTypesReply } from "@/app/lib/example-data";
import { API_HOST } from "@/app/lib/gethost";

import Loading from "./loading";
import GenericError from "./error";

/* The example/test version. */
function queryTypes(makeUid: string): Array<Type> {
  return testTypesReply.items.map((x) => x as Type);
}

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
    fetch(
      `http://${API_HOST}/api/vehicles/types?` +
        new URLSearchParams({
          mk: selectedMake.uid,
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
        text={`No types found for make '${selectedMake.name}' (${selectedMake.uid})`}
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
      getOptionValue={(x) => x.type_id}
    />
  );
}
