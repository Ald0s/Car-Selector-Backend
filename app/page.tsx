"use client";

import { useState } from "react";
import { SingleValue } from "react-select";

import { Make, Type, Model, YearModel, Vehicle } from "@/app/lib/definitions";

import SelectMake from "@/app/ui/make";
import SelectType from "@/app/ui/type";
import SelectModel from "@/app/ui/model";
import SelectYearModel from "@/app/ui/yearmodel";
import SelectVehicle from "@/app/ui/vehicle";

export default function VehiclePicker() {
  const [selectedMake, setSelectedMake] = useState<Make | null>(null);
  const [selectedType, setSelectedType] = useState<Type | null>(null);
  const [selectedModel, setSelectedModel] = useState<Model | null>(null);
  const [selectedYearModel, setSelectedYearModel] = useState<YearModel | null>(
    null
  );
  const [selectedVehicle, setSelectedVehicle] = useState<Vehicle | null>(null);

  // Local handlers for change will nullify all proceeding data points in the cascade when updated.
  const handleMakeChange = (obj: SingleValue<Make>) => {
    setSelectedMake(obj);

    setSelectedType(null);
    setSelectedModel(null);
    setSelectedYearModel(null);
    setSelectedVehicle(null);
  };

  const handleTypeChange = (obj: SingleValue<Type>) => {
    setSelectedType(obj);

    setSelectedModel(null);
    setSelectedYearModel(null);
    setSelectedVehicle(null);
  };

  const handleModelChange = (obj: SingleValue<Model>) => {
    setSelectedModel(obj);

    setSelectedYearModel(null);
    setSelectedVehicle(null);
  };

  const handleYearModelChange = (obj: SingleValue<YearModel>) => {
    setSelectedYearModel(obj);

    setSelectedVehicle(null);
  };

  const handleVehicleChange = (obj: SingleValue<Vehicle>) => {
    setSelectedVehicle(obj);
  };

  return (
    <main className="flex min-h-screen flex-col items-center p-24 space-y-10">
      <h1 className="font-bold text-4xl">Car Selector</h1>

      <div className="flex flex-col w-5/12 space-y-5">
        {/* Always create the make selection. */}
        <SelectMake handleMakeChange={handleMakeChange} />

        {/* Create type selection ONLY if make is selected. */}
        {selectedMake && (
          <SelectType
            selectedMake={selectedMake}
            handleTypeChange={handleTypeChange}
          />
        )}

        {/* Create model selection ONLY if make & type are selected. */}
        {selectedMake && selectedType && (
          <SelectModel
            selectedMake={selectedMake}
            selectedType={selectedType}
            handleModelChange={handleModelChange}
          />
        )}

        {/* Create year model selection ONLY if make, type and model are selected */}
        {selectedMake && selectedType && selectedModel && (
          <SelectYearModel
            selectedMake={selectedMake}
            selectedType={selectedType}
            selectedModel={selectedModel}
            handleYearModelChange={handleYearModelChange}
          />
        )}

        {/* Create vehicle selection ONLY if make, type, model and year model are selected */}
        {selectedMake && selectedType && selectedModel && selectedYearModel && (
          <SelectVehicle
            selectedMake={selectedMake}
            selectedType={selectedType}
            selectedModel={selectedModel}
            selectedYearModel={selectedYearModel}
            handleVehicleChange={handleVehicleChange}
          />
        )}
      </div>
    </main>
  );
}
