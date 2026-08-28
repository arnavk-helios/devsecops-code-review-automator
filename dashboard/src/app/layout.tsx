import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'DevSecOps Command Center',
  description: 'Multi-Agent PR Review Dashboard',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-gray-50 antialiased min-h-screen">
        {children}
      </body>
    </html>
  );
}