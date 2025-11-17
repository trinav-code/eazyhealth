/**
 * TypeScript type definitions for EazyHealth AI
 */

export type ReadingLevel = 'grade3' | 'grade6' | 'grade8' | 'high_school' | 'college';

export interface ExplainerSection {
  heading: string;
  content: string;
}

export interface Source {
  url: string;
  title: string;
  excerpt?: string;
}

export interface ExplainerResponse {
  title: string;
  sections: ExplainerSection[];
  sources: Source[];
  disclaimer: string;
}

export interface ExplainRequest {
  query?: string;
  url?: string;
  raw_text?: string;
  reading_level: ReadingLevel;
}

export interface BriefingListItem {
  id: number;
  title: string;
  slug: string;
  summary: string;
  source_type: string;
  tags: string[];
  reading_level: string;
  created_at: string;
}

export interface BriefingDetail {
  id: number;
  title: string;
  slug: string;
  summary: string;
  body: string;
  source_type: string;
  source_urls: string[];
  source_metadata: Record<string, any>;
  tags: string[];
  charts: Array<Record<string, any>>;
  reading_level: string;
  created_at: string;
  disclaimer: string;
}

export interface BriefingListResponse {
  items: BriefingListItem[];
  total: number;
}

export const READING_LEVEL_LABELS: Record<ReadingLevel, string> = {
  grade3: '3rd Grade (Age 8-9)',
  grade6: '6th Grade (Age 11-12)',
  grade8: '8th Grade (Age 13-14)',
  high_school: 'High School (Age 15-18)',
  college: 'College Level (18+)',
};

export const READING_LEVEL_DESCRIPTIONS: Record<ReadingLevel, string> = {
  grade3: 'Very simple words and short sentences',
  grade6: 'Simple language, easy to understand',
  grade8: 'Clear and straightforward',
  high_school: 'Standard vocabulary with some medical terms',
  college: 'Advanced vocabulary and medical terminology',
};
