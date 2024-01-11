import type { Metadata } from "next";

import "@/app/ui/globals.css";

export const metadata: Metadata = {
  title: "Car Selector Backend",
  description:
    "An example for selecting vehicles based on cascading data points.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
