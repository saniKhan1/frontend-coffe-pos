import { describe, it, expect } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { DateFilterProvider, useDateFilter } from '../src/context/DateFilterContext';
import React from 'react';

describe('DateFilter Context (Dashboard Logic)', () => {
    it('should update dates based on presets', () => {
        const wrapper = ({ children }: { children: React.ReactNode }) => <DateFilterProvider>{children}</DateFilterProvider>;
        const { result } = renderHook(() => useDateFilter(), { wrapper });

        act(() => {
            // Set to 7 days
            result.current.setPreset(7);
        });

        const start = new Date(result.current.startDate);
        const end = new Date(result.current.endDate);

        // The difference should be roughly 7 days in milliseconds
        const diffTime = Math.abs(end.getTime() - start.getTime());
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

        expect(diffDays).toBe(7);
    });
});
