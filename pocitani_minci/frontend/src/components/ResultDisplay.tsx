import Image from "next/image";

type Props = { result: any, steps: boolean };

export default function ResultDisplay({ result, steps }: Props) {
  if (!result) return null;
  return (
    <div className="w-full mt-6">
      <div className="mb-2 font-semibold">Result:</div>
      <div>Coins detected: <b>{result.coin_count}</b></div>
      {result.annotated_image && (
        <div className="my-4">
          <div className="mb-1">Annotated Image:</div>
          <Image
            src={result.annotated_image}
            alt="Annotated"
            width={600}
            height={400}
            className="max-w-full border rounded"
            style={{ height: 'auto' }}
          />
        </div>
      )}
      {steps && result.processing_steps && (
        <div className="my-4">
          <div className="mb-2">Processing Steps:</div>
          <div className="grid grid-cols-2 gap-2">
            {Object.entries(result.processing_steps).map(([step, img]) => (
              <div key={step}>
                <div className="text-xs text-gray-600 mb-1">{step}</div>
                <Image
                  src={img as string}
                  alt={step}
                  width={400}
                  height={300}
                  className="w-full border rounded"
                  style={{ height: 'auto' }}
                />
              </div>
            ))}
          </div>
          {result.final_result && (
            <div className="mt-4">
              <div className="text-xs text-gray-600 mb-1">Final Result:</div>
              <Image
                src={result.final_result}
                alt="Final Result"
                width={600}
                height={400}
                className="w-full border rounded"
                style={{ height: 'auto' }}
              />
            </div>
          )}
        </div>
      )}
      {result.coins && result.coins.length > 0 && (
        <div className="my-4">
          <div className="font-semibold">Coin Data:</div>
          <ul className="text-sm">
            {result.coins.map((coin: any) => (
              <li key={coin.id}>
                #{coin.id}: center=({coin.center_x.toFixed(1)},{coin.center_y.toFixed(1)}), radius={coin.radius.toFixed(1)}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
