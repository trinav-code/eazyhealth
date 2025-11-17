/**
 * API client for EazyHealth AI backend
 */
import type {
  ExplainRequest,
  ExplainerResponse,
  BriefingListResponse,
  BriefingDetail,
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

async function fetchApi<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;

  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new ApiError(
        response.status,
        errorData.detail || `HTTP ${response.status}: ${response.statusText}`
      );
    }

    return await response.json();
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new Error(`Network error: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

export const api = {
  /**
   * Generate an explainer for a health query/article
   */
  async explain(request: ExplainRequest): Promise<ExplainerResponse> {
    return fetchApi<ExplainerResponse>('/explain', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  },

  /**
   * Get list of briefings with pagination
   */
  async getBriefings(params?: {
    limit?: number;
    offset?: number;
    source_type?: string;
  }): Promise<BriefingListResponse> {
    const searchParams = new URLSearchParams();
    if (params?.limit) searchParams.set('limit', params.limit.toString());
    if (params?.offset) searchParams.set('offset', params.offset.toString());
    if (params?.source_type) searchParams.set('source_type', params.source_type);

    const query = searchParams.toString();
    const endpoint = `/briefings${query ? `?${query}` : ''}`;

    return fetchApi<BriefingListResponse>(endpoint);
  },

  /**
   * Get a specific briefing by slug
   */
  async getBriefing(slug: string): Promise<BriefingDetail> {
    return fetchApi<BriefingDetail>(`/briefings/${slug}`);
  },

  /**
   * Generate a new briefing (for testing/demo)
   */
  async generateBriefing(params: {
    source_type: 'data_analysis' | 'article_summary';
    topic?: string;
    use_mock_data?: boolean;
    reading_level?: string;
  }): Promise<{ created: boolean; briefing: any }> {
    return fetchApi('/briefings/generate', {
      method: 'POST',
      body: JSON.stringify(params),
    });
  },
};

export { ApiError };
