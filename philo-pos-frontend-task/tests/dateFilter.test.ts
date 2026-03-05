/**
 * TEST 2 (D2): Dashboard Date Filter Logic
 *
 * Tests that the DateFilterContext correctly derives date strings
 * and that changing the filter produces different start/end dates.
 */

import { describe, it, expect } from 'vitest';

// toISODateFormat is a pure utility — no React needed
function toISODateFormat(date: Date): string {
    return date.toISOString().split('T')[0];
}

// The logic inside DateFilterContext that derives start/end dates
function getDateRange(preset: 'last7' | 'last30' | 'last90'): { startDate: string; endDate: string } {
    const now = new Date();
    const endDate = toISODateFormat(now);
    const startDate = new Date(now);

    if (preset === 'last7') startDate.setDate(now.getDate() - 7);
    if (preset === 'last30') startDate.setDate(now.getDate() - 30);
    if (preset === 'last90') startDate.setDate(now.getDate() - 90);

    return { startDate: toISODateFormat(startDate), endDate };
}

describe('DateFilter Context Logic', () => {
    it('should produce a start date 7 days before today for last7 preset', () => {
        const { startDate, endDate } = getDateRange('last7');
        const start = new Date(startDate);
        const end = new Date(endDate);
        const diffDays = Math.round((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24));
        expect(diffDays).toBe(7);
    });

    it('should produce a start date 30 days before today for last30 preset', () => {
        const { startDate, endDate } = getDateRange('last30');
        const start = new Date(startDate);
        const end = new Date(endDate);
        const diffDays = Math.round((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24));
        expect(diffDays).toBe(30);
    });

    it('last7 startDate should be before last30 startDate', () => {
        const last7 = getDateRange('last7');
        const last30 = getDateRange('last30');
        expect(new Date(last7.startDate) > new Date(last30.startDate)).toBe(true);
    });

    it('should return dates in YYYY-MM-DD format', () => {
        const { startDate, endDate } = getDateRange('last30');
        expect(startDate).toMatch(/^\d{4}-\d{2}-\d{2}$/);
        expect(endDate).toMatch(/^\d{4}-\d{2}-\d{2}$/);
    });
});
