type Props = { loading: boolean };

export default function SubmitButton({ loading }: Props) {
  return (
    <button
      type="submit"
      className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      disabled={loading}
    >
      {loading ? "Processing..." : "Detect Coins"}
    </button>
  );
}
