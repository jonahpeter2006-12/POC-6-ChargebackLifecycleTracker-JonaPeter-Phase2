import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Infocreon Internship - Chargeback Lifecycle",
  description:
    "PoC-6 Chargeback Lifecycle Intelligence - an interactive payment dispute analytics dashboard developed by Jona Peter for the Infocreon Internship.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full antialiased">
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}