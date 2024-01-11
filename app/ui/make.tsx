import { useEffect, useState } from "react";
import Select, { SingleValue } from "react-select";

import { Make } from "@/app/lib/definitions";
import { testMakesReply } from "@/app/lib/example-data";
import { API_HOST } from "@/app/lib/gethost";

import Loading from "./loading";
import GenericError from "./error";

/* The example/test version. */
function queryMakes(): Array<Make> {
  return testMakesReply.items.map((x) => x as Make);
}

export default function SelectMake({
  handleMakeChange,
}: {
  handleMakeChange: (obj: SingleValue<Make>) => void;
}) {
  const [make, setMake] = useState<Make | null>(null);
  const [makeList, setMakeList] = useState<Array<Make> | null>(null);
  const [isLoading, setLoading] = useState<boolean>(true);

  const onMakeChanged = (obj: SingleValue<Make>) => {
    setMake(obj);
    handleMakeChange(obj);
  };

  useEffect(() => {
    // TODO: this is fetch()
    console.log(window.location.host);
    fetch(`http://${API_HOST}/api/vehicles/makes`)
      .then((response) => response.json())
      .then((jsonData) => {
        let makes: Array<Make> = jsonData.items.map((x: object) => x as Make);
        setMakeList(makes);
        setLoading(false);
      });
  }, []);

  if (isLoading) {
    return <Loading text={"Loading makes ..."} />;
  }

  if (!makeList) {
    return <GenericError text={"No makes found!"} />;
  }

  return (
    <Select
      placeholder="Select a Make..."
      value={make}
      options={makeList}
      onChange={onMakeChanged}
      getOptionLabel={(x) => x.name}
      getOptionValue={(x) => x.uid}
    />
  );
}
