type Props = { steps: boolean, setSteps: (v: boolean) => void };

export default function StepsCheckbox({ steps, setSteps }: Props) {
  return (
    <div className="flex items-center gap-2">
      <input
        type="checkbox"
        checked={steps}
        onChange={() => setSteps(!steps)}
        id="steps"
      />
      <label htmlFor="steps">Show Processing Steps</label>
    </div>
  );
}
