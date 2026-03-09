import React, { useState } from 'react';
import './index.css'
import { FileUpload } from './components/FileUpload';
import { KPICard } from './components/KPICard';
import { AIPanel } from './components/AIPanel';
import { uploadFiles, fetchInsights } from './services/apiService';
import {
    BarChart3,
    TrendingUp,
    Activity,
    Wallet,
    ActivitySquare
} from 'lucide-react';

function App() {
    const [hasData, setHasData] = useState(false);
    const [isProcessing, setIsProcessing] = useState(false);
    const [kpis, setKpis] = useState<any[]>([]);
    const [insights, setInsights] = useState<any>(null);

    const handleFilesSelected = async (files: File[]) => {
        setIsProcessing(true);
        try {
            // 1. Upload files and get latest computed KPIs
            const uploadRes = await uploadFiles(files);

            if (uploadRes.kpis_computed) {
                // Map raw KPIs to card format
                const computed = uploadRes.kpis_computed;
                const mappedKpis = [
                    { 
                        title: "Current Ratio", 
                        value: `${computed["Current Ratio"]}x`, 
                        trend: { value: 0.2, isPositive: true }, 
                        icon: <Wallet className="w-4 h-4" /> 
                    },
                    { 
                        title: "Interest Coverage Ratio", 
                        value: `${computed["Interest Coverage Ratio"]}`, 
                        trend: { value: 0.5, isPositive: true }, 
                        icon: <Activity className="w-4 h-4" /> 
                    },
                    { 
                        title: "Price to Sales", 
                        value: `${computed["Price to Sales"]}`, 
                        trend: { value: 0.1, isPositive: false }, 
                        icon: <TrendingUp className="w-4 h-4" /> 
                    },
                    { 
                        title: "EV/EBITDA", 
                        value: `${computed["EV/EBITDA"]}`, 
                        trend: { value: 0.05, isPositive: true }, 
                        icon: <ActivitySquare className="w-4 h-4" /> 
                    },
                ];
                setKpis(mappedKpis);
            }

            // 2. Fetch AI Insights generated from the latest KPIs
            const aiRes = await fetchInsights();
            setInsights(aiRes);

            setHasData(true);
        } catch (error) {
            console.error("Error processing financial data:", error);
            alert("Failed to process financial data. Is the backend running?");
        } finally {
            setIsProcessing(false);
        }
    };

    return (
        <div className="min-h-screen bg-background text-foreground flex flex-col font-sans">

            {/* Top Navbar */}
            <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
                <div className="container flex h-16 items-center">
                    <div className="flex items-center gap-2 mr-4 font-bold tracking-tight text-xl">
                        <div className="bg-primary text-primary-foreground p-1.5 rounded-md">
                            <BarChart3 className="w-5 h-5" />
                        </div>
                        FinSight AI
                    </div>
                    <nav className="flex items-center space-x-6 text-sm font-medium">
                        <a href="#" className="transition-colors hover:text-foreground/80 text-foreground">Dashboard</a>
                        <a href="#" className="transition-colors hover:text-foreground/80 text-foreground/60">Reports</a>
                        <a href="#" className="transition-colors hover:text-foreground/80 text-foreground/60">Settings</a>
                    </nav>
                </div>
            </header>

            {/* Main Content */}
            <main className="flex-1 container py-8 px-4 md:px-8 mx-auto space-y-8">

                {/* Header Section */}
                <div className="flex flex-col space-y-2">
                    <h1 className="text-3xl font-bold tracking-tight">Financial Intelligence Dashboard</h1>
                    <p className="text-muted-foreground">Upload your statements for AI-powered analysis and KPI extraction.</p>
                </div>

                {/* Upload State vs Dashboard State */}
                {!hasData ? (
                    <div className="py-12">
                        <FileUpload onFilesSelected={handleFilesSelected} isLoading={isProcessing} />
                    </div>
                ) : (
                    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">

                        {/* KPI Grid */}
                        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                            {kpis.map((kpi, idx) => (
                                <KPICard key={idx} {...kpi} />
                            ))}
                        </div>

                        {/* AI Insights & Charts Container */}
                        <div className="grid gap-4 md:grid-cols-1">
                            <AIPanel insights={insights} isLoading={!insights} />
                        </div>

                        {/* Action buttons */}
                        <div className="flex justify-end mt-8">
                            <button
                                onClick={() => setHasData(false)}
                                className="px-4 py-2 bg-secondary text-secondary-foreground hover:bg-secondary/80 rounded-md text-sm font-medium transition-colors"
                            >
                                Upload Different Files
                            </button>
                        </div>

                    </div>
                )}
            </main>
        </div>
    );
}

export default App;
