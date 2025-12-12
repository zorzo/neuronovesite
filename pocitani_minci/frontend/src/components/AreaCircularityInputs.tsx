type Props = {
  minArea: number,
  setMinArea: (n: number) => void,
  circularity: number,
  setCircularity: (n: number) => void,
};

export default function AreaCircularityInputs({ minArea, setMinArea, circularity, setCircularity }: Props) {
  return (
    <div className="flex gap-2 items-center">
      <label>Min Area:</label>
      <input
        type="number"
        min={50}
        max={10000}
        value={minArea}
        onChange={e => setMinArea(Number(e.target.value))}
        className="border rounded px-2 py-1 w-20"
      />
      <label>Circularity:</label>
      <input
        type="number"
        step="0.01"
        min={0.1}
        max={1}
        value={circularity}
        onChange={e => setCircularity(Number(e.target.value))}
        className="border rounded px-2 py-1 w-20"
      />
    </div>
  );
}
