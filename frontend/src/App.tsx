import { useState } from "react";
import { BarChart3, Wallet } from "lucide-react";
import { uploadFiles, fetchInsights } from "./services/apiService";
import {FileUpload} from "./components/FileUpload";
import {KPICard} from "./components/KPICard";
import {AIPanel} from "./components/AIPanel";

interface KPI {
    title: string;
    value: string | number;
    trend?: {
        value: number;
        isPositive: boolean;
    };
    icon?: React.ReactNode;
}

interface Insights {
    executiveSummary: string;
    riskLevel: 'Low' | 'Medium' | 'High';
    recommendations: string[];
    healthStatus: string;
}

function App() {
    const [hasData, setHasData] = useState(false);
    const [isProcessing, setIsProcessing] = useState(false);
    const [kpis, setKpis] = useState<KPI[]>([]);
    const [insights, setInsights] = useState<Insights | null>(null);

    const handleFilesSelected = async (files: File[]) => {
        setIsProcessing(true);

        try {
            const uploadRes = await uploadFiles(files);

            if (uploadRes.kpis_computed) {
                const computed = uploadRes.kpis_computed;

                const mappedKpis: KPI[] = Object.entries(computed).map(([key, value]) => ({
                    title: key,
                    value: value !== null && value !== undefined ? `${value}x` : 'N/A',
                    trend: { value: 0, isPositive: true },
                    icon: <Wallet className="w-4 h-4" />
                }));

                setKpis(mappedKpis);
            }

            setHasData(true);

            fetchInsights()
                .then((aiRes) => setInsights(aiRes))
                .catch((err) => console.error(err));

        } catch (error) {
            console.error("Error processing financial data:", error);
        } finally {
            setIsProcessing(false);
        }
    };

    return (
        <div className="min-h-screen bg-background text-foreground flex flex-col font-sans">

            {/* Navbar */}
            <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur">
                <div className="container flex h-16 items-center">
                    <div className="flex items-center gap-2 font-bold text-xl">
                        <div className="bg-primary text-primary-foreground p-1.5 rounded-md">
                            <BarChart3 className="w-5 h-5" />
                        </div>
                        FinSight AI
                    </div>
                </div>
            </header>

            {/* Main */}
            <main className="flex-1 container py-8 px-4 mx-auto space-y-8">

                {!hasData ? (
                    <FileUpload onFilesSelected={handleFilesSelected} isLoading={isProcessing} />
                ) : (
                    <div className="space-y-8">

                        {/* KPI Grid */}
                        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                            {kpis.map((kpi, idx) => (
                                <KPICard key={idx} {...kpi} />
                            ))}
                        </div>

                        {/* AI Panel */}
                        <AIPanel insights={insights} isLoading={!insights} />

                        <div className="flex justify-end">
                            <button
                                onClick={() => setHasData(false)}
                                className="px-4 py-2 bg-secondary rounded-md"
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