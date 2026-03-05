import React, { createContext, useContext, useState, ReactNode } from 'react';
import { subDays } from 'date-fns';
import { toISODateFormat } from '../lib/utils';

interface DateFilterContextType {
    startDate: string;
    endDate: string;
    setStartDate: (date: string) => void;
    setEndDate: (date: string) => void;
    setPreset: (days: number) => void;
}

const DateFilterContext = createContext<DateFilterContextType | undefined>(undefined);

export function DateFilterProvider({ children }: { children: ReactNode }) {
    // Default to last 30 days based on API requirements
    const defaultEnd = new Date();
    const defaultStart = subDays(defaultEnd, 30);

    const [startDate, setStartDate] = useState(toISODateFormat(defaultStart));
    const [endDate, setEndDate] = useState(toISODateFormat(defaultEnd));

    const setPreset = (days: number) => {
        const end = new Date();
        const start = subDays(end, days);
        setEndDate(toISODateFormat(end));
        setStartDate(toISODateFormat(start));
    };

    return (
        <DateFilterContext.Provider value={{ startDate, endDate, setStartDate, setEndDate, setPreset }}>
            {children}
        </DateFilterContext.Provider>
    );
}

export function useDateFilter() {
    const context = useContext(DateFilterContext);
    if (context === undefined) {
        throw new Error('useDateFilter must be used within a DateFilterProvider');
    }
    return context;
}
