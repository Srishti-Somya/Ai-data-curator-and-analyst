// API service for communicating with the FastAPI backend

export interface QueryRequest {
  query: string;
  keywords: string[];
  columns_to_save: string[];
}

export interface QueryResponse {
  message: string;
  svg_file: string;
  csv_file: string;
}

export interface ProcessingStatus {
  isProcessing: boolean;
  progress: number;
  message: string;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

export class ApiService {
  private static instance: ApiService;
  
  private constructor() {}
  
  public static getInstance(): ApiService {
    if (!ApiService.instance) {
      ApiService.instance = new ApiService();
    }
    return ApiService.instance;
  }

  async processQuery(request: QueryRequest): Promise<QueryResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/process`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error processing query:', error);
      throw error;
    }
  }

  async getCsvData(): Promise<string> {
    try {
      const response = await fetch(`${API_BASE_URL}/csv`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.text();
    } catch (error) {
      console.error('Error fetching CSV data:', error);
      throw error;
    }
  }

  async getSvgData(): Promise<string> {
    try {
      const response = await fetch(`${API_BASE_URL}/svg`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.text();
    } catch (error) {
      console.error('Error fetching SVG data:', error);
      throw error;
    }
  }

  async checkServerHealth(): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE_URL}/docs`);
      return response.ok;
    } catch (error) {
      return false;
    }
  }
}

export const apiService = ApiService.getInstance(); 