import { useEffect, useState } from "react";
import Select, { SingleValue } from "react-select";

import { Make } from "../lib/Types";
import getHost from "../lib/GetHost";

import Loading from "./Loading";
import GenericError from "./Error";

/**
 * A component for displaying a make- this will display the make's logo.
 */
function MakeOption({
  makeId,
  makeName
}: {
  makeId: string,
  makeName: string
}) {
  let host: string = getHost();
  let imageSrc: string = `${host}/api/logo/${makeId}`;
  return (
    <div className="flex items-center">
        <span className="min-w-10">
          <img className="block w-9" src={imageSrc} alt="make-image" />
        </span>
        <span>{makeName}</span>
      </div>
  )
}

export default function SelectMake({
  handleMakeChange,
}: {
  handleMakeChange: (obj: SingleValue<Make>) => void;
}) {
  const [make, setMake] = useState<Make | null>(null);
  const [makeList, setMakeList] = useState<Array<Make> | null>();
  const [isLoading, setLoading] = useState<boolean>(true);

  const onMakeChanged = (obj: SingleValue<Make>) => {
    setMake(obj);
    handleMakeChange(obj);
  };

  useEffect(() => {
    let host: string = getHost();
    fetch(`${host}/api/vehicles/makes`)
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
      getOptionValue={(x) => x.id}
      formatOptionLabel={(x) => (
        <MakeOption makeId={x.id} makeName={x.name} />
      )}
    />
  );
}