'use client'

import { useCoinDetection } from "../hooks/useCoinDetection";
import FileInput from "../components/FileInput";
import AreaCircularityInputs from "../components/AreaCircularityInputs";
import StepsCheckbox from "../components/StepsCheckbox";
import SubmitButton from "../components/SubmitButton";
import ResultDisplay from "../components/ResultDisplay";

export default function HomePage() {
  const {
    file, setFile,
    minArea, setMinArea,
    circularity, setCircularity,
    steps, setSteps,
    loading,
    result,
    error,
    handleSubmit
  } = useCoinDetection();

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    handleSubmit();
  };

  return (
    <main className="flex flex-col items-center p-4 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Coin Detection</h1>
      <form className="w-full space-y-4 bg-gray-50 p-4 rounded-xl shadow" onSubmit={onSubmit}>
        <FileInput onChange={setFile} />
        <AreaCircularityInputs minArea={minArea} setMinArea={setMinArea} circularity={circularity} setCircularity={setCircularity} />
        <StepsCheckbox steps={steps} setSteps={setSteps} />
        <SubmitButton loading={loading} />
      </form>
      {error && <div className="text-red-600 mt-4">{error}</div>}
      <ResultDisplay result={result} steps={steps} />
    </main>
  );
}
