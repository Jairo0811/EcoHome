export type ResourceMetric = 'ENERGY_KWH' | 'WATER_L' | 'GAS_M3';
export type ResourceReading = { total: number; previousTotal: number; changePercent: number | null; limit: number | null; progressPercent: number | null };
export type ResourceSummary = { range: 'day' | 'week' | 'month'; days: number; resources: Record<ResourceMetric, ResourceReading> };
export type ResourceHistory = { metric: ResourceMetric; days: number; history: Array<{ date: string; total: number }> };
