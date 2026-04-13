import React from 'react';
import { cn } from '../utils/utils';

interface KPICardProps {
    title: string;
    value: string | number;
    trend?: {
        value: number;
        isPositive: boolean;
    };
    icon?: React.ReactNode;
    description?: string;
    className?: string;
}

export function KPICard({ title, value, trend, icon, description, className }: KPICardProps) {
    return (
        <div className={cn("p-6 rounded-xl border bg-card text-card-foreground shadow-sm flex flex-col hover:shadow-md transition-shadow", className)}>
            <div className="flex justify-between items-start mb-4">
                <h3 className="text-sm font-medium text-muted-foreground">{title}</h3>
                {icon && <div className="text-muted-foreground">{icon}</div>}
            </div>

            <div className="flex items-baseline gap-2">
                <h2 className="text-3xl font-bold tracking-tight">{value || 'N/A'}</h2>

                {trend && (
                    <span
                        className={cn(
                            "text-xs font-semibold px-2 py-0.5 rounded-full flex items-center",
                            trend.isPositive ? "text-emerald-500 bg-emerald-500/10" : "text-destructive bg-destructive/10"
                        )}
                    >
                        {trend.isPositive ? '+' : ''}{trend.value}%
                    </span>
                )}
            </div>

            {description && (
                <p className="text-xs text-muted-foreground mt-3">{description}</p>
            )}
        </div>
    );
}
