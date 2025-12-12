import { detectCoins } from "@/services/coinDetection";
import { useState } from "react";

export function useCoinDetection(defaultArea = 1000, defaultCirc = 0.7) {
  const [file, setFile] = useState<File | null>(null);
  const [minArea, setMinArea] = useState(defaultArea);
  const [circularity, setCircularity] = useState(defaultCirc);
  const [steps, setSteps] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (f: File | null) => {
    setFile(f);
    setResult(null);
    setError(null);
  };

  const handleSubmit = async () => {
    if (!file) {
      setError("Please select an image.");
      return;
    }
    setLoading(true);
    setResult(null);
    setError(null);
    try {
      const res = await detectCoins(file, minArea, circularity, steps);
      setResult(res.data);
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Request failed");
    } finally {
      setLoading(false);
    }
  };

  return {
    file, setFile: handleFileChange,
    minArea, setMinArea,
    circularity, setCircularity,
    steps, setSteps,
    loading,
    result,
    error,
    handleSubmit
  };
}
