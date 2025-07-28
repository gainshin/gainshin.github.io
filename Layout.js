import React from 'react';
import PortfolioPage from './PortfolioPage';

export default function Layout({ children }) {
    return (
        <>
            <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800&display=swap');
        html {
          scroll-behavior: smooth;
        }
        body {
          font-family: 'Inter', sans-serif;
          background-color: #f8fafc;
        }
        .text-teal {
          color: #0d9488;
        }
        .bg-teal {
          background-color: #0d9488;
        }
        .border-teal {
          border-color: #0d9488;
        }
        .ring-teal {
          --tw-ring-color: #0d9488;
        }
        .hover\:bg-teal-dark:hover {
            background-color: #0a7a6f;
        }
      `}</style>
            <div className="bg-slate-50 text-slate-800">
                <PortfolioPage />
                {children}
            </div>
        </>
    );
}