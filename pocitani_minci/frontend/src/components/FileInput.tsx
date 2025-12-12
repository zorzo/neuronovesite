import React, { useRef, useState } from "react";

type Props = { onChange: (file: File | null) => void };

export default function FileInput({ onChange }: Props) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [fileName, setFileName] = useState<string>("");

  const handleClick = () => inputRef.current?.click();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0] || null;
    setFileName(file ? file.name : "");
    onChange(file);
  };

  return (
    <div className="flex flex-col gap-2">
      <button
        type="button"
        className="px-4 py-2 bg-blue-600 text-white rounded-lg shadow hover:bg-blue-700 transition-all"
        onClick={handleClick}
      >
        {fileName ? "Change Image" : "Select Image"}
      </button>
      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        className="hidden"
        onChange={handleChange}
      />
      <div className="text-sm text-gray-600 min-h-[1.5rem]">
        {fileName ? <>Selected: <span className="font-medium">{fileName}</span></> : "No image selected"}
      </div>
    </div>
  );
}
