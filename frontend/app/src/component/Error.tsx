export default function GenericError({ text }: { text: string }) {
  return (
    <h3 className="font-semibold text-2xl text-center self-center text-red-600">
      {text}
    </h3>
  );
}
